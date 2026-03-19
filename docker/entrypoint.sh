#!/usr/bin/env bash
set -euo pipefail

# --- Environment variables ---
# TF_API_TOKEN     - Scalr API token (mapped to SCALR_TOKEN for Scalr CLI)
# SCALR_HOSTNAME   - e.g. sunward.scalr.io
# WORKSPACE_ID     - Scalr workspace ID
# TF_SOURCE        - path to terraform source inside /workspace/source (default: .)
# OUTPUT_FORMAT    - drawio (default), png, or both
# OUTPUT_PATH      - output directory (default: docs/architecture)
# RUN_STATUS_FILTER - applied (post-apply) or planned (PR speculative)
# DIAGRAM_FILTER   - terravision --filter value (default: network, set to "none" to disable)

# Scalr CLI reads SCALR_TOKEN and SCALR_HOSTNAME from env vars directly
export SCALR_TOKEN="${TF_API_TOKEN:?TF_API_TOKEN is required}"
export SCALR_HOSTNAME="${SCALR_HOSTNAME:?SCALR_HOSTNAME is required}"
WORKSPACE_ID="${WORKSPACE_ID:?WORKSPACE_ID is required}"
TF_SOURCE="${TF_SOURCE:-.}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-drawio}"
OUTPUT_PATH="${OUTPUT_PATH:-docs/architecture}"
RUN_STATUS_FILTER="${RUN_STATUS_FILTER:-applied}"
DIAGRAM_FILTER="${DIAGRAM_FILTER:-network}"

SOURCE_DIR="/workspace/source/${TF_SOURCE}"
OUTPUT_DIR="/workspace/source/${OUTPUT_PATH}"

echo "==> Fetching latest '${RUN_STATUS_FILTER}' run for workspace ${WORKSPACE_ID}"
RUN_JSON=$(scalr get-runs \
    -filter-workspace="${WORKSPACE_ID}" \
    -filter-status="${RUN_STATUS_FILTER}" 2>/dev/null || true)

if [ -z "$RUN_JSON" ] || [ "$RUN_JSON" = "null" ] || [ "$RUN_JSON" = "[]" ]; then
    echo "ERROR: No runs found with status '${RUN_STATUS_FILTER}' for workspace ${WORKSPACE_ID}"
    exit 1
fi

# Extract the plan ID from the first (most recent) run
PLAN_ID=$(echo "$RUN_JSON" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if isinstance(data, list) and len(data) > 0:
    plan = data[0].get('plan', {})
    print(plan.get('id', ''))
")

if [ -z "$PLAN_ID" ]; then
    echo "ERROR: Could not extract plan ID from Scalr response"
    exit 1
fi
echo "    Plan ID: ${PLAN_ID}"

echo "==> Fetching plan JSON for plan ${PLAN_ID}"
scalr get-json-output -plan="${PLAN_ID}" > /tmp/plan.json 2>/dev/null || {
    echo "WARNING: Could not export plan JSON, proceeding without it"
    rm -f /tmp/plan.json
}

# Always fetch state from Scalr (used as fallback if graph generation fails
# or if plan has no real changes)
echo "==> Fetching current state from Scalr"
STATE_VERSION_JSON=$(scalr get-current-state-version -workspace="${WORKSPACE_ID}" 2>/dev/null || true)
if [ -n "$STATE_VERSION_JSON" ] && [ "$STATE_VERSION_JSON" != "null" ]; then
    STATE_VERSION_ID=$(echo "$STATE_VERSION_JSON" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if isinstance(data, dict):
    print(data.get('id', ''))
elif isinstance(data, list) and len(data) > 0:
    print(data[0].get('id', ''))
" 2>/dev/null || true)
    if [ -n "$STATE_VERSION_ID" ]; then
        echo "    State version ID: ${STATE_VERSION_ID}"
        scalr get-state-version-download -state_version="${STATE_VERSION_ID}" > /tmp/state.json 2>/dev/null || {
            echo "WARNING: Could not download state file"
            rm -f /tmp/state.json
        }
    fi
fi

# Check if the plan has real changes (non no-op)
HAS_CHANGES="no"
if [ -f /tmp/plan.json ]; then
    HAS_CHANGES=$(python3 -c "
import json, sys
try:
    data = json.load(open('/tmp/plan.json'))
    changes = [c for c in data.get('resource_changes', [])
               if c.get('change',{}).get('actions') != ['no-op']]
    print('yes' if changes else 'no')
except Exception:
    print('no')
" 2>/dev/null || echo "no")
fi

if [ "$HAS_CHANGES" = "no" ] && [ -f /tmp/state.json ]; then
    echo "==> No pending changes — using state-only mode, skipping terraform graph"
else
    echo "==> Generating terraform graph from ${SOURCE_DIR}"
    cd "${SOURCE_DIR}"
    terraform init -backend=false -input=false -no-color > /dev/null 2>&1 || true
    terraform graph > /tmp/graph.dot 2>/dev/null || {
        echo "    terraform graph command failed"
        rm -f /tmp/graph.dot
    }

    # Fall back to existing graph.dot in source directory
    if [ ! -f /tmp/graph.dot ] && [ -f "${SOURCE_DIR}/graph.dot" ]; then
        echo "    Using existing graph.dot from source directory"
        cp "${SOURCE_DIR}/graph.dot" /tmp/graph.dot
    fi

    # If graph failed but we have state, fall back to state-only mode
    if [ ! -f /tmp/graph.dot ] && [ -f /tmp/state.json ]; then
        echo "    Graph generation failed — falling back to state-only mode"
    elif [ ! -f /tmp/graph.dot ]; then
        echo "WARNING: No graph.dot available and no state file — proceeding without either"
    fi
fi

# Build terravision command
mkdir -p "${OUTPUT_DIR}"
OUTFILE="${OUTPUT_DIR}/architecture"

TV_ARGS=(
    draw
    --source "${SOURCE_DIR}"
    --layout grid
    --outfile "${OUTFILE}"
)

# Add planfile and graphfile if available
if [ -f /tmp/plan.json ] && [ -f /tmp/graph.dot ]; then
    TV_ARGS+=(--planfile /tmp/plan.json --graphfile /tmp/graph.dot)
elif [ -f /tmp/plan.json ] && [ -f /tmp/state.json ]; then
    # State-only mode: plan + state, no graph needed
    TV_ARGS+=(--planfile /tmp/plan.json --statefile /tmp/state.json)
elif [ -f /tmp/plan.json ]; then
    echo "WARNING: Plan JSON available but no graph DOT or state — skipping --planfile"
elif [ -f /tmp/graph.dot ]; then
    echo "WARNING: Graph DOT available but no plan JSON — skipping --graphfile"
fi

# Add statefile alongside planfile+graphfile for change highlighting fallback
if [ -f /tmp/state.json ] && [ -f /tmp/graph.dot ]; then
    TV_ARGS+=(--statefile /tmp/state.json)
fi

# Add filter unless explicitly disabled
if [ -n "$DIAGRAM_FILTER" ] && [ "$DIAGRAM_FILTER" != "none" ]; then
    TV_ARGS+=(--filter "${DIAGRAM_FILTER}")
fi

# Run for each requested format
run_terravision() {
    local fmt="$1"
    echo "==> Running terravision (format: ${fmt})"
    terravision "${TV_ARGS[@]}" --format "${fmt}"
}

case "${OUTPUT_FORMAT}" in
    both)
        run_terravision drawio
        run_terravision png
        ;;
    *)
        run_terravision "${OUTPUT_FORMAT}"
        ;;
esac

echo "==> Done. Output written to ${OUTPUT_DIR}/"
ls -la "${OUTPUT_DIR}/"
