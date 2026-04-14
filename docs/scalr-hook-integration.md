# Terravision Scalr Hook Integration

## Overview

This document describes how Terravision is integrated with Scalr to automatically generate draw.io architecture diagrams after every Terraform apply, and upload them to Confluence.

## How It Works

A post-apply hook script runs inside the Scalr runner after every successful `terraform apply`. The script:

1. Installs Terravision (from the [bradms98 fork](https://github.com/bradms98/terravision)) via pip
2. Extracts plan JSON, state, and dependency graph directly from the runner's filesystem
3. Runs Terravision to generate a `.drawio` diagram
4. Creates or finds a Confluence page (named after the workspace) under a parent page
5. Uploads the diagram as an attachment and embeds a draw.io macro for inline rendering

### Why This Works Without a Custom Runner

Terravision's draw.io rendering path is pure Python (XML generation via `ElementTree`). It does not depend on the system `graphviz` binaries that the PNG/SVG path requires. The Scalr default runner already has Python 3.13 and pip, so a simple `pip install` at runtime is sufficient.

## Current Setup

### Script Location

`scripts/draw_environment.sh` in each workspace's Terraform repo (for prototyping). Eventually this will move to a centralized hooks repo.

### Scalr Configuration

- **Hook type**: After Apply (post-apply)
- **Hook value**: `./scripts/draw_environment.sh`
- **Configured via**: Scalr UI (Settings > Custom Hooks on the workspace)

### Required Scalr Variables

| Variable | Level | Sensitive | Description |
|---|---|---|---|
| `CONF_USER` | Workspace or Environment | No | Atlassian email address for API auth |
| `CONF_TOKEN` | Workspace or Environment | Yes | Atlassian API token |
| `GH_TOKEN` | Workspace or Environment | Yes | GitHub token (only needed if Terravision repo goes private) |

### Auto-Injected Scalr Variables (no setup needed)

| Variable | Description |
|---|---|
| `SCALR_WORKSPACE_ID` | Workspace being applied |
| `SCALR_WORKSPACE_NAME` | Workspace name (used as Confluence page title) |
| `SCALR_HOSTNAME` | e.g., `sunward.scalr.io` |
| `SCALR_TOKEN` | Scalr API token |
| `SCALR_RUN_CONTENT_ROOT` | Path to the Terraform config root |
| `SCALR_RUN_ID` | Current run identifier (used in log messages) |
| `SCALR_RUN_IS_DESTROY` | `1` on destroy runs — script exits early to skip diagram generation |

### Runner Filesystem (confirmed via Scalr docs)

- **Plan binary**: `/opt/data/terraform.tfplan.bin` — hard-coded path, not derived from an env var
- **Working directory in hook**: Not guaranteed to be `$SCALR_RUN_CONTENT_ROOT`. The hook script explicitly `cd`s into `$SCALR_RUN_CONTENT_ROOT` before invoking `terraform state pull` / `terraform graph`, which require access to the `.terraform/` directory and backend config
- **Persistence**: `.terraform/` and backend config persist into the post-apply hook since Terraform and hooks run in the same container

### Confluence Setup

- **Parent page**: "Automated Diagrams" (ID: `1858437137`) in the Technology space
- **Child pages**: One per workspace, named to match the workspace (e.g., `aws_dev_sandbox`)
- **Rendering**: Requires the [draw.io for Confluence](https://marketplace.atlassian.com/apps/1210933/draw-io-diagrams-for-confluence) app to be installed
- **Auth**: Currently using a personal unscoped API token with Basic auth against `gosunward.atlassian.net/wiki/rest/api/...`

## Running Locally

To generate a diagram locally (outside the Scalr runner), you need to fetch plan/state/graph data from Scalr and run Terravision manually.

### Commands

```bash
# 1. Get the latest applied run's plan ID from Scalr
scalr get-runs -filter-workspace=ws-v0p1hbrags9otvtmn -filter-status=applied \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d[0]['plan']['id'])"
# → plan-v0p282lu7kesn8c59

# 2. Download plan JSON
scalr get-json-output -plan=plan-v0p282lu7kesn8c59 > /tmp/aws_dev_sandbox_plan.json

# 3. Get current state version ID and download state
STATE_VERSION_ID=$(scalr get-current-state-version -workspace=ws-v0p1hbrags9otvtmn \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('id',''))")
scalr get-state-version-download -state_version="$STATE_VERSION_ID" > /tmp/aws_dev_sandbox_state.json

# 4. Generate terraform graph
cd ~/git/aws_dev_sandbox
terraform init -backend=false -input=false -no-color
terraform graph > /tmp/aws_dev_sandbox_graph.dot

# 5. Create output directory and run terravision
mkdir -p ~/git/aws_dev_sandbox/docs/architecture
cd ~/git/terravision
.venv/bin/terravision draw \
  --source ~/git/aws_dev_sandbox \
  --format drawio \
  --layout grid \
  --planfile /tmp/aws_dev_sandbox_plan.json \
  --graphfile /tmp/aws_dev_sandbox_graph.dot \
  --statefile /tmp/aws_dev_sandbox_state.json \
  --outfile ~/git/aws_dev_sandbox/docs/architecture/architecture
```

### In the Scalr Runner (simplified)

Inside a post-apply hook, steps 1-4 simplify to three commands because the runner already has the data:

```bash
terraform show -json /opt/data/terraform.tfplan.bin > /tmp/plan.json
terraform state pull > /tmp/state.json
terraform graph > /tmp/graph.dot
```

## Testing

### Test Workspace

- **Workspace**: `aws_dev_sandbox`
- **Branch**: `terravision_drawio`
- **Repo**: `SLFCU-Infrastructure/aws_dev_sandbox`

### How to Test

1. Trigger a Scalr run on `aws_dev_sandbox` (either via VCS push or manual run)
2. After apply completes, check the run log for hook output
3. Verify the Confluence page was created under "Automated Diagrams"
4. Open the page and confirm the draw.io diagram renders inline

### Debugging

The script outputs progress messages (`==> ...`) to the run log. Key things to watch for:

- Pre-flight diagnostics: `which terraform`, `terraform version`, `SOURCE_DIR` value, and full `ls -la /opt/data/` listing
- Stderr capture: `terraform show -json`, `terraform state pull`, and `terraform graph` each redirect stderr to `/tmp/*.err` and `cat` the file into the run log on failure (keeps stdout-to-file clean while surfacing real error messages)
- Whether `uv pip install` succeeds
- Whether Terravision produces a `.drawio` file
- Whether the Confluence API calls succeed

## Scale-Out Plan

### Phase 1: Prototype (current)

- Script lives in the `aws_dev_sandbox` repo
- Hook configured via Scalr UI on one workspace
- Uses personal Confluence credentials

### Phase 2: Centralize

- Move script to a dedicated repo (e.g., `SLFCU-Infrastructure/scalr-hooks`)
- Register in Scalr **Hooks Registry** (Registries > Hooks at the account level)
- Attach at the **environment level** so it applies to all workspaces automatically
- No per-repo or per-workspace configuration needed

### Phase 3: Production Credentials

- Create a Confluence **service account** via `admin.atlassian.com` > Directory > Service accounts (5 free, no license seat consumed)
- Grant it minimal space permissions (add/edit pages + add attachments) in the Technology space
- Create a scoped API token for the service account
- Move `CONF_USER`/`CONF_TOKEN` to environment-level Scalr variables

### Open: IaC for Hooks

The Scalr workspaces are managed via IaC (`SLFCU-Infrastructure/scalr_prod`), but the Terraform module (`zachreborn/terraform-modules//modules/scalr`) does not currently support a `hooks` block on `scalr_workspace` resources. Options:

- Add hooks support to the module (PR needed)
- Use the Hooks Registry approach instead (environment-level, separate from workspace IaC)

## Outstanding Issues

1. **End-to-end verification** — plan/state/graph extraction was silently failing; diagnostic logging and `cd "$SOURCE_DIR"` added. Awaiting next deploy to confirm the pipeline produces a diagram and uploads it to Confluence
2. **Scoped API tokens** — granular scoped personal tokens returned 401 errors via the `api.atlassian.com` gateway. Need to investigate further when setting up the service account
3. ~~**Page title derivation**~~ — resolved: now uses `SCALR_WORKSPACE_NAME` (falls back to `basename $SCALR_RUN_CONTENT_ROOT` if unset)
4. **pip install overhead** — adds ~30-60 seconds per run. Acceptable for now, but a custom runner or cached layer would eliminate this
