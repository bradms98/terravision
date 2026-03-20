#!/usr/bin/env python3
"""Generate a hand-arranged architecture.drawio for aws_prod_data.

Layout goals:
- VPC on left, S3 bucket containers in 3-column grid to the right
- Backup vaults as containers (with lock configs + policies inside)
- DataSync, analytics, and security resources grouped logically below
- Much narrower than the auto-generated horizontal sprawl
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom


def icon_style(fill_color, shape, res_icon=None):
    """Standard AWS icon style."""
    s = (
        f"sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;"
        f"strokeColor=none;dashed=0;verticalLabelPosition=bottom;"
        f"verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;"
        f"aspect=fixed;pointerEvents=1;fillColor={fill_color};shape={shape};"
    )
    if res_icon:
        s += f"resIcon={res_icon};"
    return s


BACKUP_ICON = icon_style("#3F8624", "mxgraph.aws4.resourceIcon", "mxgraph.aws4.backup")
DATASYNC_ICON = icon_style("#ED7100", "mxgraph.aws4.resourceIcon", "mxgraph.aws4.datasync")
S3_ICON = icon_style("#3F8624", "mxgraph.aws4.resourceIcon", "mxgraph.aws4.s3")
SQS_ICON = icon_style("#E7157B", "mxgraph.aws4.resourceIcon", "mxgraph.aws4.sqs")
IAM_ICON = icon_style("#DD344C", "mxgraph.aws4.resourceIcon", "mxgraph.aws4.identity_and_access_management")
GLUE_ICON = icon_style("#8C4FFF", "mxgraph.aws4.resourceIcon", "mxgraph.aws4.glue")
EVENTBRIDGE_ICON = icon_style("#E7157B", "mxgraph.aws4.resourceIcon", "mxgraph.aws4.eventbridge")
SNS_ICON = icon_style("#E7157B", "mxgraph.aws4.resourceIcon", "mxgraph.aws4.sns")
REDSHIFT_ICON = icon_style("#C925D1", "mxgraph.aws4.resourceIcon", "mxgraph.aws4.redshift")
EC2_ICON = icon_style("#ED7100", "mxgraph.aws4.resourceIcon", "mxgraph.aws4.ec2")
NAT_ICON = icon_style("#8C4FFF", "mxgraph.aws4.nat_gateway", None)
VPC_EP_ICON = icon_style("#8C4FFF", "mxgraph.aws4.endpoints", None)
EIP_ICON = icon_style("#ED7100", "mxgraph.aws4.elastic_ip_address", None)
IGW_ICON = icon_style("#8C4FFF", "mxgraph.aws4.internet_gateway", None)
INTERNET_ICON = icon_style("#232F3E", "mxgraph.aws4.internet", None)
TGW_ICON = icon_style("#8C4FFF", "mxgraph.aws4.transit_gateway_attachment", None)

# Container styles
ACCOUNT_STYLE = (
    "points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],"
    "[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];"
    "outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;"
    "fontStyle=0;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;"
    "shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_account;"
    "strokeColor=#CD2264;fillColor=none;verticalAlign=top;align=left;"
    "spacingLeft=30;fontColor=#CD2264;dashed=0;"
)

REGION_STYLE = (
    "points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],"
    "[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];"
    "outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;"
    "fontStyle=0;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;"
    "shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_region;"
    "strokeColor=#00A4A6;fillColor=none;verticalAlign=top;align=left;"
    "spacingLeft=30;fontColor=#147EBA;dashed=1;"
)

VPC_STYLE = (
    "points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],"
    "[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];"
    "outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;"
    "fontStyle=0;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;"
    "shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_vpc;"
    "strokeColor=#248814;fillColor=none;verticalAlign=top;align=left;"
    "spacingLeft=30;fontColor=#AAB7B8;dashed=0;"
)

AZ_STYLE = (
    "fillColor=none;strokeColor=#147EBA;dashed=1;verticalAlign=top;"
    "fontStyle=0;fontColor=#147EBA;whiteSpace=wrap;html=1;"
)

SUBNET_PUBLIC_STYLE = (
    "points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],"
    "[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];"
    "outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;"
    "fontStyle=0;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;"
    "shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_security_group;"
    "grStroke=0;strokeColor=#7AA116;fillColor=#F2F6E8;verticalAlign=top;"
    "align=left;spacingLeft=30;fontColor=#248814;dashed=0;"
)

SUBNET_PRIVATE_STYLE = (
    "points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],"
    "[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];"
    "outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;"
    "fontStyle=0;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;"
    "shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_security_group;"
    "grStroke=0;strokeColor=#00A4A6;fillColor=#E6F6F7;verticalAlign=top;"
    "align=left;spacingLeft=30;fontColor=#147EBA;dashed=0;"
)

SG_STYLE = (
    "points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],"
    "[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];"
    "outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;"
    "fontStyle=0;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;"
    "shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_security_group;"
    "grStroke=0;strokeColor=#DD3522;fillColor=none;verticalAlign=top;"
    "align=left;spacingLeft=30;fontColor=#DD3522;dashed=0;"
)

S3_CONTAINER_STYLE = (
    "fillColor=none;strokeColor=#3F8624;dashed=0;"
    "fontStyle=0;fontColor=#3F8624;whiteSpace=wrap;html=1;"
    "container=1;collapsible=0;recursiveResize=0;rounded=1;"
)

S3_PROP_LIST_STYLE = (
    "text;html=1;align=left;verticalAlign=top;strokeColor=none;"
    "fillColor=none;fontSize=11;fontColor=#888888;whiteSpace=wrap;"
    "overflow=hidden;"
)

BACKUP_CONTAINER_STYLE = (
    "fillColor=none;strokeColor=#E7157B;dashed=0;verticalAlign=top;"
    "fontStyle=0;fontColor=#E7157B;whiteSpace=wrap;html=1;"
    "container=1;collapsible=0;recursiveResize=0;rounded=1;"
)

GROUP_STYLE = (
    "fillColor=none;strokeColor=#5A6C86;dashed=1;verticalAlign=top;"
    "fontStyle=0;fontColor=#5A6C86;whiteSpace=wrap;html=1;"
)

SECTION_LABEL_STYLE = (
    "text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];"
    "autosize=1;strokeColor=none;fillColor=none;fontSize=14;fontStyle=1;"
    "fontColor=#666666;"
)

EDGE_STYLE = "endArrow=classic;html=1;rounded=0;"


def cell(id, value, style, parent, x, y, w, h, vertex=True):
    return {
        "id": str(id), "value": value, "style": style,
        "parent": str(parent), "x": x, "y": y, "w": w, "h": h,
        "vertex": vertex,
    }


def edge(id, style, parent, source, target):
    return {
        "id": str(id), "style": style, "parent": str(parent),
        "source": str(source), "target": str(target),
    }


def build_diagram():
    cells = []
    edges = []

    # ── Shared layout constants ────────────────────────────────────
    GAP = 15           # gap between adjacent containers / sections
    ICON_ROW_H = 140   # vertical spacing between icon rows
    SEC_GAP = 30       # gap between section label and first icon
    SEC_SPACE = 150     # gap between last icon row and next section label

    # ── VPC ────────────────────────────────────────────────────────
    # VPC endpoints: 5 per row → 7 endpoints = 2 rows
    # AZ bottoms: AZ1=515, AZ2=579.  Endpoints start at y=600.
    vpc_w, vpc_h = 702, 820
    cells.append(cell(4,
        "VPC - data_vpc<br>vpc-0c3d...acaf<br>10.212.0.0/24",
        VPC_STYLE, 3, 20, 60, vpc_w, vpc_h))

    # AZ1
    cells.append(cell(5, "Availability Zone Usw2 Az1", AZ_STYLE, 4, 20, 60, 389, 455))
    cells.append(cell(6,
        "Subnet - data_vpc-subnet-public-us-west-2b<br>subnet-0dc3...5769<br>10.212.0.192/26",
        SUBNET_PUBLIC_STYLE, 5, 20, 60, 349, 164))
    cells.append(cell(7, "NAT Gateway<br>nat-0afe...df7d", NAT_ICON, 6, 48, 60, 48, 48))
    cells.append(cell(8,
        "Subnet - data_vpc-subnet-private-us-west-2b<br>subnet-05fa...468f<br>10.212.0.64/26",
        SUBNET_PRIVATE_STYLE, 5, 20, 239, 349, 196))
    cells.append(cell(9,
        "Redshift Subnet Group<br>redshift-cluster-<br>edwdev<br>cluster-subn...-edw",
        REDSHIFT_ICON, 8, 70, 60, 48, 48))
    cells.append(cell(10,
        "EC2TransitGatewayVPC<br>Attachment<br>data_vpc<br>tgw-atta...be41",
        TGW_ICON, 8, 232, 60, 48, 48))

    # AZ2
    cells.append(cell(11, "Availability Zone Usw2 Az2", AZ_STYLE, 4, 429, 60, 253, 519))
    cells.append(cell(12,
        "Subnet - data_vpc-subnet-public-us-west-2a<br>subnet-04b1...4115<br>10.212.0.128/26",
        SUBNET_PUBLIC_STYLE, 11, 20, 60, 213, 164))
    cells.append(cell(13, "NAT Gateway<br>nat-0289...c287", NAT_ICON, 12, 48, 60, 48, 48))
    cells.append(cell(14,
        "Subnet - data_vpc-subnet-private-us-west-2a<br>subnet-05b4...a31f<br>10.212.0.0/26",
        SUBNET_PRIVATE_STYLE, 11, 20, 239, 213, 260))
    cells.append(cell(15, "Security Group", SG_STYLE, 14, 20, 60, 173, 180))
    cells.append(cell(16,
        "EC2<br>prod_datasync_agent<br>i-0c9c...4bd2",
        EC2_ICON, 15, 62, 60, 48, 48))

    # VPC Endpoints — 5 per row
    vpcep_labels = [
        "vpce-06e4...670c", "vpce-0387...e2e8", "vpce-081c...601e",
        "vpce-006c...07fe", "vpce-0ac5...969e", "vpce-0df9...0e0c",
        "vpce-0bf4...d33b",
    ]
    ep_per_row = 5
    ep_spacing = 128
    ep_y_start = 600
    ep_row_h = 110
    for i, lbl in enumerate(vpcep_labels):
        col = i % ep_per_row
        row = i // ep_per_row
        cells.append(cell(17 + i,
            f"VPC Endpoint<br>data_vpc<br>{lbl}",
            VPC_EP_ICON, 4,
            42 + col * ep_spacing, ep_y_start + row * ep_row_h, 48, 48))

    # ── Elastic IP Group (below VPC) ──────────────────────────────
    eip_y = 60 + vpc_h + GAP
    cells.append(cell(24, "Group", GROUP_STYLE, 3, 20, eip_y, 160, 148))
    cells.append(cell(25, "Elastic IP", EIP_ICON, 24, 31, 60, 48, 48))

    # ── S3 Bucket Containers (icon + property list) ───────────────
    s3_w = 310
    s3_x = 740
    s3_col_sp = s3_w + GAP   # 325
    s3_h_4 = 150              # 4 ancillary items
    s3_h_5 = 160              # 5 items
    s3_h_7 = 195              # 7 items

    s3_buckets = [
        (26, 27, 28, "data-etl-certs",           0, 0, s3_h_5, ["OwnershipControls", "BucketPolicy", "PublicAccessBlock", "ServerSideEncryption", "Versioning"]),
        (32, 33, 34, "aws-glue-assets",           0, 1, s3_h_4, ["OwnershipControls", "BucketPolicy", "PublicAccessBlock", "ServerSideEncryption"]),
        (37, 38, 39, "aws-glue-scripts",          0, 2, s3_h_4, ["OwnershipControls", "BucketPolicy", "PublicAccessBlock", "ServerSideEncryption"]),
        (42, 43, 44, "datasync-odrive",           1, 0, s3_h_4, ["OwnershipControls", "BucketPolicy", "PublicAccessBlock", "ServerSideEncryption"]),
        (47, 48, 49, "aws-prod-ml-feature-store", 1, 1, s3_h_7, ["IntelligentTiering", "LifecycleConfig", "OwnershipControls", "BucketPolicy", "PublicAccessBlock", "ServerSideEncryption", "Versioning"]),
        (55, 56, 57, "opcon-odrive",              1, 2, s3_h_4, ["OwnershipControls", "BucketPolicy", "PublicAccessBlock", "ServerSideEncryption"]),
        (60, 61, 62, "redshift-offload",          2, 0, s3_h_4, ["OwnershipControls", "BucketPolicy", "PublicAccessBlock", "ServerSideEncryption"]),
    ]

    # Row y positions (use tallest in each row)
    s3_row_y = {0: 60}
    s3_row_y[1] = s3_row_y[0] + s3_h_5 + GAP      # row 0 tallest = 160
    s3_row_y[2] = s3_row_y[1] + s3_h_7 + GAP       # row 1 tallest = 195

    for cid, icon_id, list_id, name, row, col, height, props in s3_buckets:
        cx = s3_x + col * s3_col_sp
        cy = s3_row_y[row]
        cells.append(cell(cid, "", S3_CONTAINER_STYLE, 3, cx, cy, s3_w, height))
        cells.append(cell(icon_id, f"S3 Bucket<br>{name}", S3_ICON, cid, 15, 25, 48, 48))
        prop_text = "<br>".join(f"- {p}" for p in props)
        cells.append(cell(list_id, prop_text, S3_PROP_LIST_STYLE, cid, 100, 25, 195, height - 40))

    s3_bottom = s3_row_y[2] + s3_h_4   # bottom of last S3 row

    # ── Backup Vault Containers (icon + property list) ────────────
    BACKUP_PROP_LIST_STYLE = (
        "text;html=1;align=left;verticalAlign=top;strokeColor=none;"
        "fillColor=none;fontSize=11;fontColor=#888888;whiteSpace=wrap;"
        "overflow=hidden;"
    )
    vault_w = 300
    vault_h = 130
    vault_col_sp = vault_w + GAP
    vault_y_start = s3_bottom + 40  # gap for DATA PROTECTION label

    vaults = [
        (200, 80, 84, "vault_disaster_recovery", 0, 0),
        (201, 81, 85, "vault_prod_daily",        0, 1),
        (202, 82, 86, "vault_prod_hourly",       1, 0),
        (203, 83, 87, "vault_prod_monthly",      1, 1),
    ]
    vault_props = ["LockConfiguration", "VaultPolicy"]
    vault_prop_text = "<br>".join(f"- {p}" for p in vault_props)

    for cid, icon_id, list_id, name, row, col in vaults:
        cx = s3_x + col * vault_col_sp
        cy = vault_y_start + row * (vault_h + GAP)
        cells.append(cell(cid, "", BACKUP_CONTAINER_STYLE, 3, cx, cy, vault_w, vault_h))
        cells.append(cell(icon_id, f"Backup Vault<br>{name}", BACKUP_ICON, cid, 15, 15, 48, 48))
        cells.append(cell(list_id, vault_prop_text, BACKUP_PROP_LIST_STYLE, cid, 100, 20, 185, 80))

    # Backup Plans/Selections (right of vaults, tight)
    bp_x = s3_x + 2 * vault_col_sp + 20
    bs_x = bp_x + 180
    cells.append(cell(76, "Backup Plan<br>eadbdf43-e1f6...d748", BACKUP_ICON, 3, bp_x, vault_y_start, 48, 48))
    cells.append(cell(78, "Backup Selection<br>35c773c4-9704...d95f", BACKUP_ICON, 3, bs_x, vault_y_start, 48, 48))
    cells.append(cell(77, "Backup Plan<br>7bd708a6-a409...bca3", BACKUP_ICON, 3, bp_x, vault_y_start + vault_h + GAP, 48, 48))
    cells.append(cell(79, "Backup Selection<br>89d3b285-f0ea...8c45", BACKUP_ICON, 3, bs_x, vault_y_start + vault_h + GAP, 48, 48))

    # ── Full-width sections below VPC + S3/Backup ─────────────────
    left_bottom = eip_y + 148          # EIP group bottom
    right_bottom = vault_y_start + 2 * (vault_h + GAP)
    sections_y = max(left_bottom, right_bottom) + 20

    col_x = [80, 310, 540]

    # DataSync
    ds_label_y = sections_y
    ds_y = ds_label_y + SEC_GAP
    cells.append(cell(67, "Datasync Agent<br>arn:aws:datasync:us-west...4bc3", DATASYNC_ICON, 3, col_x[0], ds_y, 48, 48))
    cells.append(cell(68, "Datasync Location S3<br>arn:aws:datasync:us-west...62da", DATASYNC_ICON, 3, col_x[1], ds_y, 48, 48))
    cells.append(cell(69, "Datasync Location Smb<br>arn:aws:datasync:us-west...0d04", DATASYNC_ICON, 3, col_x[2], ds_y, 48, 48))
    cells.append(cell(70, "datasync_task.odrive_<br>testing_to_S3_evening<br>arn:aws:datasync:us-west...1d87", DATASYNC_ICON, 3, col_x[0], ds_y + ICON_ROW_H, 48, 48))
    cells.append(cell(71, "datasync_task.odrive_<br>testing_to_S3_morning<br>arn:aws:datasync:us-west...3fd0", DATASYNC_ICON, 3, col_x[1], ds_y + ICON_ROW_H, 48, 48))

    # Analytics
    analytics_label_y = ds_y + 2 * ICON_ROW_H + SEC_SPACE - ICON_ROW_H
    analytics_y = analytics_label_y + SEC_GAP
    cells.append(cell(72, "Glue Catalog Database<br>MLFeatureStoreDatabase<br>597088036719:ml_feature_store", GLUE_ICON, 3, col_x[0], analytics_y, 48, 48))
    cells.append(cell(66, "Redshift Cluster<br>redshift-cluster-<br>edwdev<br>redshift-clus...wdev", REDSHIFT_ICON, 3, col_x[1], analytics_y, 48, 48))

    # Security
    security_label_y = analytics_y + ICON_ROW_H + 20
    security_y = security_label_y + SEC_GAP
    cells.append(cell(73, "IAMOpenidConnect<br>Provider<br>GitHub OIDC Provider<br>arn:aws:iam::597088036719:oidc-prov....com", IAM_ICON, 3, col_x[0], security_y, 48, 48))
    cells.append(cell(65, "Security Group<br>redshift_sg<br>sg-07dc...f7b8",
                       icon_style("#DD344C", "mxgraph.aws4.resourceIcon", "mxgraph.aws4.security_group"),
                       3, col_x[1], security_y, 48, 48))

    # Monitoring & Notifications
    mon_label_y = security_y + ICON_ROW_H + 20
    mon_y = mon_label_y + SEC_GAP
    cells.append(cell(93, "CloudWatch Event Rule", EVENTBRIDGE_ICON, 3, col_x[0], mon_y, 48, 48))
    cells.append(cell(95, "SNS Topic", SNS_ICON, 3, col_x[1], mon_y, 48, 48))
    cells.append(cell(74, "SQS Queue<br>https://sqs.us-west...-dlq", SQS_ICON, 3, col_x[2], mon_y, 48, 48))
    cells.append(cell(75, "SQS Queue Policy<br>https://sqs.us-west...-dlq", SQS_ICON, 3, col_x[0], mon_y + ICON_ROW_H, 48, 48))

    content_bottom = mon_y + 2 * ICON_ROW_H + 40

    # ── Account & Region (sized to fit) ───────────────────────────
    region_w = max(
        20 + vpc_w + 20,                            # VPC
        s3_x + 3 * s3_col_sp + 20,                  # S3 (3 cols)
        bs_x + 200,                                  # backup selections
    )
    region_h = content_bottom - 60 + 40
    cells.insert(0, cell(3, "Us-West-2", REGION_STYLE, 2, 20, 60, region_w, region_h))
    cells.insert(0, cell(2, "Account<br>597088036719", ACCOUNT_STYLE, 1, 30, 30, region_w + 40, region_h + 80))

    # ── Outside Account ────────────────────────────────────────────
    cells.append(cell(92, "Internet", INTERNET_ICON, 1, region_w // 2, -58, 48, 48))
    cells.append(cell(94, "Internet Gateway", IGW_ICON, 1, 350, 126, 48, 48))

    # ── Edges ──────────────────────────────────────────────────────
    edges.append(edge(96, EDGE_STYLE, 1, 94, 92))
    edges.append(edge(97, EDGE_STYLE, 1, 78, 76))
    edges.append(edge(98, EDGE_STYLE, 1, 79, 77))
    edges.append(edge(111, EDGE_STYLE, 1, 65, 66))
    edges.append(edge(107, EDGE_STYLE, 1, 13, 25))
    edges.append(edge(108, EDGE_STYLE, 1, 13, 94))
    edges.append(edge(109, EDGE_STYLE, 1, 7, 25))
    edges.append(edge(110, EDGE_STYLE, 1, 7, 94))

    # ── Section Labels ─────────────────────────────────────────────
    cells.append(cell(300, "STORAGE", SECTION_LABEL_STYLE, 3, s3_x, 35, 100, 20))
    cells.append(cell(301, "DATA PROTECTION", SECTION_LABEL_STYLE, 3, s3_x, s3_bottom + 15, 180, 20))
    cells.append(cell(302, "DATA SYNC", SECTION_LABEL_STYLE, 3, 20, ds_label_y, 120, 20))
    cells.append(cell(303, "ANALYTICS", SECTION_LABEL_STYLE, 3, 20, analytics_label_y, 120, 20))
    cells.append(cell(304, "SECURITY", SECTION_LABEL_STYLE, 3, 20, security_label_y, 100, 20))
    cells.append(cell(305, "MONITORING & NOTIFICATIONS", SECTION_LABEL_STYLE, 3, 20, mon_label_y, 280, 20))

    return cells, edges


def to_xml(cells, edges):
    root = ET.Element("mxfile", host="terravision")
    diagram = ET.SubElement(root, "diagram", id="terravision-diagram", name="Architecture")
    model = ET.SubElement(diagram, "mxGraphModel",
                          dx="1400", dy="900", grid="1", gridSize="10",
                          guides="1", tooltips="1", connect="1", arrows="1",
                          fold="1", page="1", pageScale="1",
                          pageWidth="1100", pageHeight="850",
                          math="0", shadow="0")
    root_el = ET.SubElement(model, "root")
    ET.SubElement(root_el, "mxCell", id="0")
    ET.SubElement(root_el, "mxCell", id="1", parent="0")

    for c in cells:
        attrs = {
            "id": c["id"], "value": c["value"], "style": c["style"],
            "parent": c["parent"], "vertex": "1",
        }
        el = ET.SubElement(root_el, "mxCell", **attrs)
        geo = ET.SubElement(el, "mxGeometry",
                            x=str(c["x"]), y=str(c["y"]),
                            width=str(c["w"]), height=str(c["h"]))
        geo.set("as", "geometry")

    for e in edges:
        attrs = {
            "id": e["id"], "value": "", "style": e["style"],
            "parent": e["parent"], "edge": "1",
            "source": e["source"], "target": e["target"],
        }
        el = ET.SubElement(root_el, "mxCell", **attrs)
        geo = ET.SubElement(el, "mxGeometry", relative="1")
        geo.set("as", "geometry")

    # Pretty print
    rough = ET.tostring(root, encoding="unicode")
    dom = minidom.parseString(rough)
    return dom.toprettyxml(indent="  ", encoding=None).replace(
        '<?xml version="1.0" ?>\n', '<?xml version="1.0" encoding="UTF-8"?>\n'
    )


if __name__ == "__main__":
    cells, edges = build_diagram()
    xml = to_xml(cells, edges)
    outpath = "/Users/bradengberg/git/aws_prod_data/docs/architecture/architecture-redesign.drawio"
    with open(outpath, "w") as f:
        f.write(xml)
    print(f"Written to {outpath}")
    print(f"  Cells: {len(cells)}, Edges: {len(edges)}")
