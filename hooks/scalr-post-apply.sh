#!/bin/bash
set -euo pipefail

# scalr-post-apply.sh — Scalr post-apply hook
# Generates a draw.io architecture diagram and uploads it to Confluence.
#
# Required Scalr env vars (auto-injected):
#   SCALR_WORKSPACE_ID, SCALR_HOSTNAME, SCALR_TOKEN, SCALR_RUN_CONTENT_ROOT
#
# Required Scalr workspace/environment variables (set as Shell Variables):
#   CONF_USER                 — Atlassian email for API auth
#   CONF_TOKEN                — Atlassian API token (mark as sensitive)
#   CONFLUENCE_BASE_URL       — Confluence REST API base URL
#                               (e.g. https://<tenant>.atlassian.net/wiki/rest/api)
#   CONFLUENCE_PARENT_PAGE_ID — parent page under which per-workspace pages live
#   CONFLUENCE_SPACE_KEY      — Confluence space key for new pages
#
# Optional:
#   GH_TOKEN            — GitHub token (if terravision repo goes private)
#   TERRAVISION_FILTER  — filter profile name (e.g. "network", "security").
#                         Loads filters/<name>.yaml from the terravision
#                         package. Falls back to filters/default.yaml if the
#                         named file is missing (error is logged). Set to
#                         "none" to disable filtering entirely. Unset = no
#                         filter applied.
#   LOGGING             — NONE | INFO (default) | DEBUG
#                         NONE:  errors only
#                         INFO:  progress banners + status
#                         DEBUG: INFO + verbose tool output,
#                                HTTP codes/bodies, plan/state info
#                         tqdm progress bars are always suppressed.

CONF_BASE_URL="${CONFLUENCE_BASE_URL:-}"
PARENT_PAGE_ID="${CONFLUENCE_PARENT_PAGE_ID:-}"
SOURCE_DIR="${SCALR_RUN_CONTENT_ROOT:-.}"
PAGE_TITLE="${SCALR_WORKSPACE_NAME:-$(basename "${SOURCE_DIR}")}"

# --- Logging setup ---
LOGGING="${LOGGING:-INFO}"
case "$LOGGING" in
    NONE|INFO|DEBUG) ;;
    *)
        echo "WARNING: unknown LOGGING='$LOGGING', defaulting to INFO" >&2
        LOGGING=INFO
        ;;
esac

log_info() {
    case "$LOGGING" in INFO|DEBUG) echo "$@" ;; esac
}

log_debug() {
    case "$LOGGING" in DEBUG) echo "$@" ;; esac
}

# fd 3 is the sink for verbose external-tool output (uv install, pip install,
# tofu warnings). Goes to stdout on INFO/DEBUG, /dev/null on NONE. ERROR
# lines bypass this and always print via bare `echo`.
if [ "$LOGGING" = "NONE" ]; then
    exec 3>/dev/null
else
    exec 3>&1
fi

if [ "${SCALR_RUN_IS_DESTROY:-0}" = "1" ]; then
    log_info "==> Destroy run detected (SCALR_RUN_ID=${SCALR_RUN_ID:-unknown}); skipping diagram generation"
    exit 0
fi

# Fail fast if any required var is missing, before doing expensive downloads
# and terravision install. CONF_USER is the Atlassian email (not sensitive)
# and CONF_TOKEN is the API token (sensitive). The CONFLUENCE_* vars are
# tenant/space-specific and intentionally have no defaults so this script
# stays generic and can be hosted in a public repo.
missing_vars=()
for var in CONF_USER CONF_TOKEN CONFLUENCE_BASE_URL CONFLUENCE_PARENT_PAGE_ID CONFLUENCE_SPACE_KEY; do
    if [ -z "${!var:-}" ]; then
        missing_vars+=("$var")
    fi
done
if [ ${#missing_vars[@]} -gt 0 ]; then
    echo "ERROR: required Scalr workspace/environment variable(s) unset: ${missing_vars[*]}"
    echo "       Configure these in Scalr UI -> workspace/environment variables (Shell Variables)."
    exit 1
fi

log_info "==> Installing uv and Python 3.11"
{
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
    uv venv --python 3.11 /tmp/tv-venv
} >&3 2>&3
source /tmp/tv-venv/bin/activate

log_info "==> Installing terravision"
if [ -n "${GH_TOKEN:-}" ]; then
    uv pip install "git+https://${GH_TOKEN}@github.com/bradms98/terravision.git@latest" --quiet >&3 2>&3
else
    uv pip install "git+https://github.com/bradms98/terravision.git@latest" --quiet >&3 2>&3
fi

# Pick the IaC binary: Scalr runners use OpenTofu (tofu) or Terraform.
# Prefer tofu when present since that's the current Scalr default; fall back to terraform.
if command -v tofu >/dev/null 2>&1; then
    TF_BIN=tofu
elif command -v terraform >/dev/null 2>&1; then
    TF_BIN=terraform
else
    echo "ERROR: neither tofu nor terraform found on PATH (SCALR_IAC_PLATFORM=${SCALR_IAC_PLATFORM:-unset})"
    exit 1
fi

# --- Generate plan/state/graph data ---
log_info "==> Extracting plan JSON"
log_debug "    IaC binary: $TF_BIN ($($TF_BIN version 2>&1 | head -1))"
log_debug "    SOURCE_DIR: ${SOURCE_DIR}"
if [ "$LOGGING" = "DEBUG" ]; then
    echo "    /opt/data/ contents:"
    ls -la /opt/data/ 2>&1 || echo "    /opt/data/ does not exist"
fi

cd "${SOURCE_DIR}"

if [ -f /opt/data/terraform.tfplan.bin ]; then
    "$TF_BIN" show -json /opt/data/terraform.tfplan.bin > /tmp/plan.json 2> /tmp/plan.err || {
        log_info "    WARNING: Could not extract plan JSON"
        cat /tmp/plan.err >&3
        rm -f /tmp/plan.json
    }
else
    log_debug "    No plan binary found at /opt/data/terraform.tfplan.bin"
fi

log_info "==> Pulling current state"
"$TF_BIN" state pull > /tmp/state.json 2> /tmp/state.err || {
    log_info "    WARNING: Could not pull state"
    cat /tmp/state.err >&3
    rm -f /tmp/state.json
}

log_info "==> Generating terraform graph"
"$TF_BIN" graph > /tmp/graph.dot 2> /tmp/graph.err || {
    log_info "    WARNING: terraform graph failed"
    cat /tmp/graph.err >&3
    rm -f /tmp/graph.dot
}

# --- Build terravision command ---
TV_ARGS=(
    draw
    --source "${SOURCE_DIR}"
    --layout grid
    --format drawio
    --outfile /tmp/architecture
)

if [ -f /tmp/plan.json ] && [ -f /tmp/graph.dot ]; then
    TV_ARGS+=(--planfile /tmp/plan.json --graphfile /tmp/graph.dot)
elif [ -f /tmp/plan.json ] && [ -f /tmp/state.json ]; then
    TV_ARGS+=(--planfile /tmp/plan.json --statefile /tmp/state.json)
elif [ -f /tmp/state.json ]; then
    TV_ARGS+=(--statefile /tmp/state.json)
else
    echo "ERROR: No plan, state, or graph data available"
    exit 1
fi

# Add statefile alongside plan+graph for change highlighting
if [ -f /tmp/state.json ] && [ -f /tmp/graph.dot ]; then
    TV_ARGS+=(--statefile /tmp/state.json)
fi

log_info "==> Running terravision"
# Capture terravision's verbose output (graphviz JSON dumps, resource lists)
# to a log file. tqdm progress bars are always disabled. On success, only
# surface the log when LOGGING=DEBUG. On failure, always surface it.
if ! TQDM_DISABLE=1 terravision "${TV_ARGS[@]}" > /tmp/terravision.log 2>&1; then
    echo "ERROR: terravision failed"
    sed 's/^/    /' /tmp/terravision.log
    exit 1
fi
if [ "$LOGGING" = "DEBUG" ]; then
    sed 's/^/    /' /tmp/terravision.log
fi

DRAWIO_FILE="/tmp/architecture.drawio"
if [ ! -f "${DRAWIO_FILE}" ]; then
    echo "ERROR: terravision did not produce ${DRAWIO_FILE}"
    sed 's/^/    /' /tmp/terravision.log
    exit 1
fi
log_info "    Diagram generated: $(wc -c < "${DRAWIO_FILE}") bytes"

# --- Upload to Confluence ---
log_info "==> Uploading to Confluence"

# Check if child page already exists under the parent.
# Note: the ?title= query param is ignored by /content/{id}/child/page on this
# site, so we fetch children and filter by exact title match in Python.
LOOKUP_URL="${CONF_BASE_URL}/content/${PARENT_PAGE_ID}/child/page?limit=200"
LOOKUP_HTTP=$(curl -s -o /tmp/conf_lookup.json -w "%{http_code}" \
    -u "${CONF_USER}:${CONF_TOKEN}" \
    "${LOOKUP_URL}")
log_debug "    Lookup HTTP ${LOOKUP_HTTP}"
if [ "${LOOKUP_HTTP}" != "200" ]; then
    log_info "    Lookup HTTP ${LOOKUP_HTTP}"
    sed 's/^/      /' /tmp/conf_lookup.json >&3 || true
elif [ "$LOGGING" = "DEBUG" ]; then
    sed 's/^/      /' /tmp/conf_lookup.json || true
fi
CHILD_PAGE_ID=$(PAGE_TITLE="${PAGE_TITLE}" python3 -c "
import json, os
title = os.environ['PAGE_TITLE']
try:
    data = json.load(open('/tmp/conf_lookup.json'))
    for r in data.get('results', []):
        if r.get('title') == title:
            print(r['id'])
            break
except Exception:
    pass
")

if [ -z "${CHILD_PAGE_ID}" ]; then
    log_info "    Creating new page: ${PAGE_TITLE}"
    PAYLOAD=$(PAGE_TITLE="${PAGE_TITLE}" PARENT_PAGE_ID="${PARENT_PAGE_ID}" CONFLUENCE_SPACE_KEY="${CONFLUENCE_SPACE_KEY}" python3 -c "
import json, os
print(json.dumps({
    'type': 'page',
    'title': os.environ['PAGE_TITLE'],
    'ancestors': [{'id': os.environ['PARENT_PAGE_ID']}],
    'space': {'key': os.environ['CONFLUENCE_SPACE_KEY']},
    'body': {
        'storage': {
            'value': '<p>Architecture diagram auto-generated by Terravision.</p>',
            'representation': 'storage'
        }
    }
}))
")
    CREATE_HTTP=$(curl -s -o /tmp/conf_create.json -w "%{http_code}" \
        -u "${CONF_USER}:${CONF_TOKEN}" \
        -X POST \
        -H "Content-Type: application/json" \
        "${CONF_BASE_URL}/content" \
        -d "${PAYLOAD}")
    log_debug "    Create HTTP ${CREATE_HTTP}"
    CHILD_PAGE_ID=$(python3 -c "
import json
try:
    print(json.load(open('/tmp/conf_create.json')).get('id', ''))
except Exception:
    print('')
")

    if [ -z "${CHILD_PAGE_ID}" ]; then
        echo "ERROR: Failed to create Confluence page (HTTP ${CREATE_HTTP})"
        sed 's/^/      /' /tmp/conf_create.json || true
        exit 1
    fi
    log_info "    Created page ID: ${CHILD_PAGE_ID}"
    if [ "$LOGGING" = "DEBUG" ]; then
        sed 's/^/      /' /tmp/conf_create.json || true
    fi
else
    log_info "    Found existing page: ${PAGE_TITLE} (ID: ${CHILD_PAGE_ID})"
fi

# Upload or update the drawio attachment
ATTACHMENT_ID=$(curl -s \
    -u "${CONF_USER}:${CONF_TOKEN}" \
    "${CONF_BASE_URL}/content/${CHILD_PAGE_ID}/child/attachment?filename=architecture.drawio" \
    | python3 -c "
import sys, json
data = json.load(sys.stdin)
results = data.get('results', [])
print(results[0]['id'] if results else '')
" 2>/dev/null || echo "")

if [ -z "${ATTACHMENT_ID}" ]; then
    log_info "    Uploading new attachment"
    curl -s \
        -u "${CONF_USER}:${CONF_TOKEN}" \
        -X POST \
        -H "X-Atlassian-Token: nocheck" \
        -F "file=@${DRAWIO_FILE};filename=architecture.drawio" \
        -F "comment=Auto-generated by Terravision post-apply hook" \
        "${CONF_BASE_URL}/content/${CHILD_PAGE_ID}/child/attachment" \
        > /dev/null
    log_info "    Attachment uploaded"
else
    log_info "    Updating existing attachment (${ATTACHMENT_ID})"
    curl -s \
        -u "${CONF_USER}:${CONF_TOKEN}" \
        -X POST \
        -H "X-Atlassian-Token: nocheck" \
        -F "file=@${DRAWIO_FILE};filename=architecture.drawio" \
        -F "comment=Updated by Terravision post-apply hook" \
        "${CONF_BASE_URL}/content/${CHILD_PAGE_ID}/child/attachment/${ATTACHMENT_ID}/data" \
        > /dev/null
    log_info "    Attachment updated"
fi

# Ensure the page body contains the note banner (naming the AWS account) and
# the draw.io macro. If both are already present we skip the PUT.
log_info "==> Checking page body for note banner and draw.io macro"
PAGE_JSON=$(curl -s \
    -u "${CONF_USER}:${CONF_TOKEN}" \
    "${CONF_BASE_URL}/content/${CHILD_PAGE_ID}?expand=body.storage,version")

CURRENT_BODY=$(echo "${PAGE_JSON}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data.get('body', {}).get('storage', {}).get('value', ''))
" 2>/dev/null || echo "")

CURRENT_VERSION=$(echo "${PAGE_JSON}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data.get('version', {}).get('number', 0))
" 2>/dev/null || echo "0")

# A page is considered up to date only if it has both the drawio macro and
# the note banner text naming this account. If either is missing, rebuild
# the body so edits to the banner template also roll out to existing pages.
BANNER_MARKER="programmatically generated overview of resources in the <strong>${PAGE_TITLE}</strong>"
if echo "${CURRENT_BODY}" | grep -q 'ac:name="drawio"' && \
   echo "${CURRENT_BODY}" | grep -qF "${BANNER_MARKER}"; then
    log_info "    Page body already up to date, skipping update"
else
    log_info "    Updating page body with note banner + draw.io macro"
    NEW_VERSION=$((CURRENT_VERSION + 1))

    # Build the PUT payload in Python via a quoted heredoc so the Confluence
    # XHTML (which contains double quotes) doesn't collide with shell quoting.
    PAYLOAD=$(PAGE_TITLE="${PAGE_TITLE}" NEW_VERSION="${NEW_VERSION}" python3 <<'PYEOF'
import json, os
title = os.environ['PAGE_TITLE']
version = int(os.environ['NEW_VERSION'])
body = (
    '<ac:structured-macro ac:name="note">'
    '<ac:rich-text-body>'
    '<p>This page contains a programmatically generated overview of resources in the '
    f'<strong>{title}</strong> AWS account. Any customization made to this diagram may be '
    'overwritten on the next deployment to this account.</p>'
    '</ac:rich-text-body>'
    '</ac:structured-macro>'
    '<ac:structured-macro ac:name="drawio">'
    '<ac:parameter ac:name="diagramName">architecture.drawio</ac:parameter>'
    '<ac:parameter ac:name="attachment">architecture.drawio</ac:parameter>'
    '</ac:structured-macro>'
)
print(json.dumps({
    'version': {'number': version},
    'type': 'page',
    'title': title,
    'body': {'storage': {'value': body, 'representation': 'storage'}},
}))
PYEOF
)

    curl -s \
        -u "${CONF_USER}:${CONF_TOKEN}" \
        -X PUT \
        -H "Content-Type: application/json" \
        "${CONF_BASE_URL}/content/${CHILD_PAGE_ID}" \
        -d "${PAYLOAD}" \
        > /dev/null
    log_info "    Page updated"
fi
log_info "    ${CONF_BASE_URL%/rest/api}/pages/viewpage.action?pageId=${CHILD_PAGE_ID}"

log_info "==> Done. Diagram uploaded to Confluence page: ${PAGE_TITLE}"
