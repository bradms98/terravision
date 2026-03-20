# QA Testing Guide

This document describes how to run manual QA tests against real infrastructure to validate diagram rendering. These tests complement the automated pytest suite by exercising the full Docker-based pipeline against live Scalr workspaces and verifying the visual output (drawio XML).

## Prerequisites

- Docker installed and running
- A Scalr API token exported as `SCALR_TOKEN` (or retrieved from macOS Keychain)
- A Terraform repo to test against, mounted as a Docker volume
- The `xmllint` CLI (ships with macOS) or equivalent for inspecting XML output

## Step 1: Build the Docker Image

```sh
cd /path/to/terravision
docker build -t terravision:test .
```

Verify the build completes with `Successfully tagged terravision:test`.

## Step 2: Run the Container

Mount a real Terraform repo and pass Scalr credentials:

```sh
docker run --rm \
  -e TF_API_TOKEN="$SCALR_TOKEN" \
  -e SCALR_HOSTNAME="sunward.scalr.io" \
  -e WORKSPACE_ID="ws-v0p1hbrb6r7sjbomp" \
  -e DIAGRAM_FILTER="none" \
  -v /path/to/aws_prod_data:/workspace/source \
  terravision:test
```

See the main [README](../README.md#development-testing-with-docker-scalr-entrypoint) for the full list of environment variables.

### Expected output

- The entrypoint fetches plan JSON and state from Scalr.
- If the plan has no real changes, terravision falls back to **state-only mode** (this is normal).
- Warnings about unreachable Git modules are expected inside Docker (no SSH keys mounted).
- The final line should read: `==> Done. Output written to /workspace/source/docs/architecture/`

### What to check in stdout/stderr

| Pattern | Meaning | Action if missing |
|---|---|---|
| `Fetching latest 'applied' run` | Scalr API reached | Check `TF_API_TOKEN` and `SCALR_HOSTNAME` |
| `Rendering Draw.io Architecture Diagram` | Pipeline completed | Look for Python tracebacks above |
| `Output file: ...architecture.drawio` | File written | Check volume mount path |
| `ERROR` or `Traceback` | Something broke | Investigate the error |

## Step 3: Inspect the Output

The output file is at `<mounted-repo>/docs/architecture/architecture.drawio`. This is an XML file in the mxGraph/drawio format. The following sections describe what to look for.

### S3 Bucket Containers (Issue #17)

S3 buckets and their ancillary resources (policies, encryption, versioning, etc.) should be grouped into dashed-border containers. Each container is a parent `mxCell` with a label starting with `S3 Bucket` and its children have `parent="<container-id>"`.

**How to verify:**

```sh
# Count S3 bucket container cells (dashed border, label starts with "S3 Bucket")
grep -c 'value="S3 Bucket' architecture.drawio

# List container labels
grep -o 'value="S3 Bucket[^"]*"' architecture.drawio
```

Expected results for `aws_prod_data`:
- **7 S3 bucket containers** (cells with `value="S3 Bucket..."` and `strokeColor=#5A6C86;dashed=1`)
- Each container has child cells (`parent="<container-id>"`) for ancillary resources such as:
  - `S3BucketOwnershipControls`
  - `S3 Bucket Policy`
  - `S3BucketPublicAccessBlock`
  - `S3BucketServerSideEncryptionConfiguration`
  - `S3 Bucket Versioning`
  - `S3BucketLifecycleConfiguration`
  - `S3BucketIntelligentTieringConfiguration`

**Verify parent-child relationships:**

```sh
# Find a container ID (e.g., id="30") and check its children
grep 'parent="30"' architecture.drawio
```

All ancillary S3 resource cells should reference the container cell as their parent.

### 6-Per-Row Layout (Issue #18)

Non-VPC region-level resources (e.g., Backup Plans, Backup Vaults, CloudWatch Alarms, SNS Topics) should be laid out approximately 6 per row.

**How to verify:**

Look at the x-coordinates of consecutive non-container, non-VPC resources with `parent="3"` (the region container). Resources on the same row share the same y-coordinate, and a new row starts when y increases.

```sh
# Extract x,y coordinates for region-level leaf nodes (parent="3", not containers)
grep 'parent="3" vertex="1"' architecture.drawio | \
  grep -o 'x="[0-9]*" y="[0-9]*"' | sort -t'"' -k4,4n -k2,2n
```

Expected pattern:
- Rows of 6 resources at y-offsets like 1281, 1412, 1543, 1674, etc.
- Within each row, x-coordinates increase in steps of approximately 673 (e.g., 325, 998, 1671, 2344, 3017, 3690)

A quick count: if you see 6 distinct x-values before y changes, the layout is correct.

### Regression: VPCs, Subnets, Security Groups

These structural containers should still render correctly.

```sh
# VPC containers
grep 'group_vpc' architecture.drawio | wc -l

# Subnet containers
grep 'group_subnet' architecture.drawio | wc -l

# Security group containers
grep 'group_security_group' architecture.drawio | wc -l
```

All counts should be greater than zero for the `aws_prod_data` workspace.

### Regression: Existing pytest Suite

Before and after any changes, the automated test suite should still pass:

```sh
cd /path/to/terravision
poetry run pytest tests -v
```

## Step 4: Report Template

Use this template when reporting QA results (e.g., in a PR comment or issue):

```
## QA Report - <date>

### Environment
- Branch: <branch name>
- Commit: <short SHA>
- Test workspace: ws-v0p1hbrb6r7sjbomp (aws_prod_data)

### Results

| Check | Result | Notes |
|---|---|---|
| Docker build | PASS/FAIL | |
| Container run | PASS/FAIL | Any warnings? |
| S3 bucket containers found | <count> | Expected: 7 for aws_prod_data |
| Ancillary resources inside containers | YES/NO | |
| 6-per-row layout | YES/NO | Actual items per row: <n> |
| VPC containers present | YES/NO | Count: <n> |
| Subnet containers present | YES/NO | Count: <n> |
| Security group containers present | YES/NO | Count: <n> |
| pytest suite | PASS/FAIL | Failures: <list> |

### Errors or Warnings
<paste any unexpected errors or tracebacks>

### Recommendation
SHIP / FIX_CRITICAL / NEEDS_MORE_TESTING
```

## Reference: aws_prod_data Expected Values

These values serve as a baseline for the `aws_prod_data` workspace (as of 2026-03-20). They may change if the infrastructure evolves.

| Metric | Expected |
|---|---|
| S3 bucket containers | 7 |
| S3 ancillary resource types | OwnershipControls, BucketPolicy, PublicAccessBlock, ServerSideEncryption, Versioning, LifecycleConfiguration, IntelligentTieringConfiguration |
| Region-level resources per row | 6 |
| VPC containers | >= 1 |
| Subnet containers | >= 1 |
| Security group containers | >= 1 |
| Output file | `docs/architecture/architecture.drawio` |
