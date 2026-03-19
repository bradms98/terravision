"""Native draw.io XML renderer for TerraVision.

Generates mxfile XML with nested AWS Architecture containers (Account > Region
> VPC > AZ > Subnet) using native mxgraph.aws4.* shapes, bypassing Graphviz
entirely.
"""

import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional, Tuple

import click

import modules.helpers as helpers
from modules.drawio_shapes import get_group_style, get_resource_style

# Layout constants
ICON_W, ICON_H = 48, 48           # The actual mxCell icon size
RESOURCE_GAP = 15                  # Minimum gap between resource footprints
RESOURCES_PER_ROW = 3
CONTAINER_PAD_TOP = 60
CONTAINER_PAD_SIDE = 20
CONTAINER_PAD_BOTTOM = 20
AZ_SPACING = 20
SUBNET_SPACING = 15
VPC_SPACING = 30
MIN_CONTAINER_W = 160
MIN_CONTAINER_H = 100
MAX_LABEL_LINE_LEN = 22           # max chars per line in resource labels
FONT_CHAR_W = 7                   # approximate px per character at fontSize=12
FONT_LINE_H = 16                  # approximate line height in px
LABEL_GAP = 4                     # gap between icon bottom and label top


# =============================================================================
# DrawioDocument — XML builder
# =============================================================================

class DrawioDocument:
    """Builds an mxfile XML document with auto-incrementing cell IDs."""

    def __init__(self):
        self._next_id = 2  # 0 = root, 1 = default parent
        self._cells = []  # list of (id, ET.Element) tuples

    def _new_id(self):
        cid = str(self._next_id)
        self._next_id += 1
        return cid

    def add_container(self, parent_id, label, style, x, y, w, h):
        """Add a container cell. Returns its cell ID."""
        cid = self._new_id()
        cell = ET.Element("mxCell")
        cell.set("id", cid)
        cell.set("value", label)
        cell.set("style", style)
        cell.set("parent", str(parent_id))
        cell.set("vertex", "1")
        geo = ET.SubElement(cell, "mxGeometry")
        geo.set("x", str(round(x)))
        geo.set("y", str(round(y)))
        geo.set("width", str(round(w)))
        geo.set("height", str(round(h)))
        geo.set("as", "geometry")
        self._cells.append((cid, cell))
        return cid

    def add_resource(self, parent_id, label, style, x, y, w=48, h=48):
        """Add a resource icon cell. Returns its cell ID."""
        cid = self._new_id()
        cell = ET.Element("mxCell")
        cell.set("id", cid)
        cell.set("value", label)
        cell.set("style", style)
        cell.set("parent", str(parent_id))
        cell.set("vertex", "1")
        geo = ET.SubElement(cell, "mxGeometry")
        geo.set("x", str(round(x)))
        geo.set("y", str(round(y)))
        geo.set("width", str(round(w)))
        geo.set("height", str(round(h)))
        geo.set("as", "geometry")
        self._cells.append((cid, cell))
        return cid

    def add_text(self, parent_id, text, x, y):
        """Add a plain-text label cell. Returns its cell ID."""
        cid = self._new_id()
        cell = ET.Element("mxCell")
        cell.set("id", cid)
        cell.set("value", text)
        cell.set(
            "style",
            "text;html=1;align=left;verticalAlign=middle;resizable=0;"
            "points=[];autosize=1;strokeColor=none;fillColor=none;",
        )
        cell.set("parent", str(parent_id))
        cell.set("vertex", "1")
        geo = ET.SubElement(cell, "mxGeometry")
        geo.set("x", str(round(x)))
        geo.set("y", str(round(y)))
        geo.set("width", "130")
        geo.set("height", "30")
        geo.set("as", "geometry")
        self._cells.append((cid, cell))
        return cid

    def add_edge(self, parent_id, source_id, target_id, bidirectional=False):
        """Add an edge between two cells. Returns its cell ID."""
        cid = self._new_id()
        cell = ET.Element("mxCell")
        cell.set("id", cid)
        cell.set("value", "")
        style = "endArrow=classic;html=1;rounded=0;"
        if bidirectional:
            style += "startArrow=classic;startFill=1;"
        cell.set("style", style)
        cell.set("parent", str(parent_id))
        cell.set("edge", "1")
        cell.set("source", str(source_id))
        cell.set("target", str(target_id))
        geo = ET.SubElement(cell, "mxGeometry")
        geo.set("relative", "1")
        geo.set("as", "geometry")
        self._cells.append((cid, cell))
        return cid

    def to_xml(self):
        """Serialize the complete <mxfile> document to a string."""
        mxfile = ET.Element("mxfile")
        mxfile.set("host", "terravision")
        diagram = ET.SubElement(mxfile, "diagram")
        diagram.set("id", "terravision-diagram")
        diagram.set("name", "Architecture")
        model = ET.SubElement(diagram, "mxGraphModel")
        model.set("dx", "1400")
        model.set("dy", "900")
        model.set("grid", "1")
        model.set("gridSize", "10")
        model.set("guides", "1")
        model.set("tooltips", "1")
        model.set("connect", "1")
        model.set("arrows", "1")
        model.set("fold", "1")
        model.set("page", "1")
        model.set("pageScale", "1")
        model.set("pageWidth", "1100")
        model.set("pageHeight", "850")
        model.set("math", "0")
        model.set("shadow", "0")
        root = ET.SubElement(model, "root")
        # Mandatory root cells
        c0 = ET.SubElement(root, "mxCell")
        c0.set("id", "0")
        c1 = ET.SubElement(root, "mxCell")
        c1.set("id", "1")
        c1.set("parent", "0")
        # User cells
        for _, cell_elem in self._cells:
            root.append(cell_elem)
        ET.indent(mxfile, space="  ")
        return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(
            mxfile, encoding="unicode"
        )


# =============================================================================
# LayoutNode — tracks hierarchy for size / position computation
# =============================================================================

def _estimate_label_footprint(label):
    """Estimate the pixel footprint of a resource icon + its label.

    Returns (width, height) covering the icon and the text below it.
    The icon is centered above the label; the footprint width is the
    wider of icon vs label text.
    """
    lines = label.split("<br>") if label else []
    if not lines:
        return ICON_W, ICON_H
    max_line_len = max(len(line) for line in lines)
    label_w = max_line_len * FONT_CHAR_W
    label_h = len(lines) * FONT_LINE_H
    footprint_w = max(ICON_W, label_w)
    footprint_h = ICON_H + LABEL_GAP + label_h
    return footprint_w, footprint_h


class LayoutNode:
    """A node in the layout tree used to compute sizes and positions."""

    def __init__(self, key, resource_type, label, is_group=False):
        self.key = key
        self.resource_type = resource_type
        self.label = label
        self.is_group = is_group
        self.children = []       # child LayoutNodes (groups)
        self.resources = []      # (resource_key, resource_type, label) tuples
        self.resource_positions = []  # populated during layout: (key, type, label, x, y)
        self.w = 0
        self.h = 0
        self.x = 0
        self.y = 0
        self.cell_id = None


# =============================================================================
# Main entry point
# =============================================================================

def render_drawio(tfdata, outfile, source, layout):
    """Generate a native draw.io XML file from tfdata.

    Args:
        tfdata: Terraform data dictionary with graphdict, meta_data, etc.
        outfile: Output filename (without extension)
        source: Source path for attribution
        layout: Layout mode (ignored — we always produce nested containers)
    """
    from modules.drawing import (
        _deduplicate_az_subnets,
        _inject_region_account_hierarchy,
        _load_provider_constants,
        _load_provider_resources,
        _sort_subnet_order,
    )
    from modules.provider_detector import get_primary_provider_or_default

    provider = get_primary_provider_or_default(tfdata)
    _load_provider_resources(provider)
    constants = _load_provider_constants(tfdata)
    GROUP_NODES = constants["GROUP_NODES"]
    EDGE_NODES = constants["EDGE_NODES"]
    OUTER_NODES = constants["OUTER_NODES"]

    # Prepare hierarchy
    _deduplicate_az_subnets(tfdata)
    _sort_subnet_order(tfdata)
    _inject_region_account_hierarchy(tfdata)

    graphdict = tfdata.get("graphdict", {})

    # ------------------------------------------------------------------
    # Phase 1: Build layout tree
    # ------------------------------------------------------------------
    built_nodes = {}  # resource_key -> LayoutNode

    def _safe_resource_type(key):
        """Extract resource type, handling keys with dots inside brackets."""
        # Strip bracket content before splitting (e.g. this["10.253.0.0/24"])
        import re
        clean = re.sub(r'\[.*?\]', '', key)
        return helpers.get_no_module_name(clean).split(".")[0]

    def _wrap_line(text, max_len=MAX_LABEL_LINE_LEN):
        """Wrap a long line at word boundaries using <br> tags."""
        if len(text) <= max_len:
            return text
        # Try splitting on common separators: spaces, underscores, hyphens
        words = text.replace("_", "_ ").replace("-", "- ").split(" ")
        lines = []
        current = ""
        for word in words:
            if current and len(current) + len(word) > max_len:
                lines.append(current.rstrip())
                current = word
            else:
                current += word
        if current:
            lines.append(current.rstrip())
        return "<br>".join(lines)

    def _build_label(resource_key, is_group=False):
        """Build a plain-text label for draw.io (no Graphviz markup)."""
        resource_type = _safe_resource_type(resource_key)
        type_label = helpers.pretty_name(resource_key, show_title=False, is_group=True)
        name_tag = helpers.get_name_tag(resource_key, tfdata)
        cidr = helpers.get_cidr_label(resource_key, tfdata)
        resource_id = helpers.get_resource_id(resource_key, tfdata)

        if is_group:
            # For containers, use a compact single-line label
            parts = [type_label]
            if name_tag:
                parts[0] = f"{type_label} - {name_tag}"
            if cidr:
                parts.append(cidr)
            return "<br>".join(parts)
        else:
            # Resource icons: label goes below the icon, wrap long lines
            parts = [_wrap_line(type_label)]
            if name_tag:
                parts.append(_wrap_line(name_tag))
            if resource_id:
                parts.append(resource_id)
            return "<br>".join(parts)

    assigned_resources = set()  # resource keys already placed in a container

    # Build set of VPC module prefixes for cross-VPC filtering
    def _get_module_prefix(key):
        """Extract top-level module prefix, e.g. 'module.vpc' from 'module.vpc.aws_foo.x'."""
        if "module." not in key:
            return ""
        parts = key.split(".")
        for i, p in enumerate(parts):
            if p == "module" and i + 1 < len(parts):
                return f"module.{parts[i + 1]}"
        return ""

    vpc_module_prefixes = set()
    vpc_all_names = set()  # all VPC identity strings (module names + Name tags)
    vpc_prefix_to_name = {}  # e.g. {"module.test_vpc": "test_vpc"}
    # Maps each VPC module prefix to ALL its identity strings
    vpc_prefix_identities = {}  # e.g. {"module.vpc": {"vpc", "transit_vpc"}}
    for k in graphdict:
        if _safe_resource_type(k) == "aws_vpc":
            pfx = _get_module_prefix(k)
            if pfx:
                vpc_module_prefixes.add(pfx)
                ids = set()
                mod_name = pfx.split(".", 1)[1] if "." in pfx else ""
                if mod_name:
                    ids.add(mod_name)
                    vpc_prefix_to_name[pfx] = mod_name
                name_tag = helpers.get_name_tag(k, tfdata)
                if name_tag:
                    ids.add(name_tag)
                    ids.add(name_tag.lower().replace("-", "_"))
                vpc_prefix_identities[pfx] = ids
                vpc_all_names |= ids

    # Resource types to hide (too granular for architecture diagrams)
    HIDE_TYPES = {
        "aws_route_table_association",
        "aws_route",
        "aws_route_table",
        "aws_ec2_transit_gateway_route",
        "aws_ec2_transit_gateway_route_table",
        "aws_ram_resource_share",
        "aws_ram_resource_association",
        "aws_ram_principal_association",
        "aws_networkmanager_core_network_policy_attachment",
    }

    def _targets_different_vpc(resource_key, current_vpc_identities):
        """Check if a resource key's bracket content references a different VPC.

        For example, key '...this["transit_vpc"][transit_vpc]~1' targets transit_vpc.
        If current VPC identities are {'test_vpc'}, this returns True.

        Args:
            resource_key: The full graphdict key to check.
            current_vpc_identities: Set of all identity strings for the current VPC
                (module name, Name tag, normalized variants).
        """
        if not current_vpc_identities or not vpc_all_names:
            return False
        import re
        bracket_contents = re.findall(r'\["?([^"\]]+)"?\]', resource_key)
        for content in bracket_contents:
            # Check if bracket content matches a known VPC identity that isn't ours
            if content in vpc_all_names and content not in current_vpc_identities:
                return True
        return False

    def _collect_descendant_resources(node):
        """Return set of all resource keys assigned to node and its descendants."""
        keys = {rkey for rkey, _, _ in node.resources}
        for child in node.children:
            keys |= _collect_descendant_resources(child)
        return keys

    def _resolve_route_table(assoc_key):
        """Follow a route_table_association's connections to find its route_table.

        Returns (route_table_key, resource_type) or None.
        """
        for conn in graphdict.get(assoc_key, []):
            conn_type = _safe_resource_type(conn)
            if conn_type == "aws_route_table":
                return conn
        return None

    def _build_tree(resource_key, vpc_ids=None):
        """Recursively build a LayoutNode tree from graphdict.

        Children (groups) are built first so their resources are claimed before
        the parent tries to add the same resources at its own level.

        Args:
            resource_key: The graphdict key to build from.
            vpc_ids: Set of identity strings for the VPC ancestor, used for
                cross-VPC filtering (e.g. {'vpc', 'transit_vpc'}).
        """
        if resource_key in built_nodes:
            return built_nodes[resource_key]

        resource_type = _safe_resource_type(resource_key)
        is_group = resource_type in GROUP_NODES
        label = _build_label(resource_key, is_group=is_group)
        node = LayoutNode(resource_key, resource_type, label, is_group=is_group)
        built_nodes[resource_key] = node

        # If this is a VPC node, set the vpc identity set for all descendants
        if resource_type == "aws_vpc":
            pfx = _get_module_prefix(resource_key)
            vpc_ids = vpc_prefix_identities.get(pfx, vpc_ids)

        children = graphdict.get(resource_key, [])

        # Pass 1: build child groups first (recursively) so they claim resources
        for child_key in children:
            child_type = _safe_resource_type(child_key)
            if child_type in GROUP_NODES:
                child_node = _build_tree(child_key, vpc_ids=vpc_ids)
                node.children.append(child_node)

        # Collect all resource keys already assigned to descendants
        descendant_keys = set()
        for child in node.children:
            descendant_keys |= _collect_descendant_resources(child)

        # Pass 2: add resources that weren't already claimed by a descendant
        seen_rt_in_subnet = set()  # track route tables already added to this container
        for child_key in children:
            child_type = _safe_resource_type(child_key)
            if child_type in GROUP_NODES:
                continue
            if child_type in tfdata.get("hidden", []):
                continue
            if child_key in assigned_resources:
                continue
            if child_key in descendant_keys:
                continue

            # --- Route table association → promote to route table icon ---
            if child_type == "aws_route_table_association":
                rt_key = _resolve_route_table(child_key)
                if rt_key and rt_key not in assigned_resources and rt_key not in seen_rt_in_subnet:
                    # Only promote if the route table belongs to the same VPC scope
                    rt_prefix = _get_module_prefix(rt_key)
                    container_vpc_prefix = _get_module_prefix(resource_key)
                    if not rt_prefix or not container_vpc_prefix or rt_prefix == container_vpc_prefix or rt_prefix not in vpc_module_prefixes:
                        rlabel = _build_label(rt_key, is_group=False)
                        node.resources.append((rt_key, "aws_route_table", rlabel))
                        assigned_resources.add(rt_key)
                        seen_rt_in_subnet.add(rt_key)
                continue  # always skip the association itself

            # --- Hide overly-granular types ---
            if child_type in HIDE_TYPES:
                continue

            # --- At VPC level, skip route tables (already promoted into subnets) ---
            if resource_type == "aws_vpc" and child_type == "aws_route_table":
                continue

            # --- Cross-VPC filter ---
            # At VPC level: skip resources whose module prefix matches a DIFFERENT VPC.
            if resource_type == "aws_vpc":
                this_vpc_prefix = _get_module_prefix(resource_key)
                child_prefix = _get_module_prefix(child_key)
                if (
                    child_prefix
                    and this_vpc_prefix
                    and child_prefix != this_vpc_prefix
                    and child_prefix in vpc_module_prefixes
                ):
                    continue

            # At any level below a VPC: skip resources whose bracket content
            # references a different VPC (e.g. this["transit_vpc"] in test_vpc tree)
            if vpc_ids and _targets_different_vpc(child_key, vpc_ids):
                continue

            # At subnet/AZ level: skip resources from a different VPC's module
            if resource_type in ("aws_subnet", "aws_az", "tv_aws_az") and vpc_ids:
                child_prefix = _get_module_prefix(child_key)
                # Find the current VPC's module prefix from its identities
                current_vpc_pfx = ""
                for pfx, ids in vpc_prefix_identities.items():
                    if ids == vpc_ids:
                        current_vpc_pfx = pfx
                        break
                if (
                    child_prefix
                    and current_vpc_pfx
                    and child_prefix != current_vpc_pfx
                    and child_prefix in vpc_module_prefixes
                ):
                    continue

            rlabel = _build_label(child_key, is_group=False)
            node.resources.append((child_key, child_type, rlabel))
            assigned_resources.add(child_key)

        return node

    # Find the root of the hierarchy (account node injected by _inject_region_account_hierarchy)
    root_key = None
    for key in graphdict:
        rtype = _safe_resource_type(key)
        if rtype == "aws_account":
            root_key = key
            break

    if root_key is None:
        for key in graphdict:
            rtype = _safe_resource_type(key)
            if rtype == "aws_vpc":
                root_key = key
                break

    if root_key is None:
        click.echo(click.style("No AWS account or VPC found in graphdict.", fg="red"))
        return

    root = _build_tree(root_key)

    # Collect "outer" resources (users, internet, etc.) and edge resources
    outer_resources = []
    edge_resources = []
    for resource_key in graphdict:
        rtype = _safe_resource_type(resource_key)
        if rtype in OUTER_NODES and resource_key not in built_nodes:
            rlabel = _build_label(resource_key, is_group=False)
            outer_resources.append((resource_key, rtype, rlabel))
            built_nodes[resource_key] = LayoutNode(resource_key, rtype, rlabel)
        elif any(rtype.startswith(e) for e in EDGE_NODES) and resource_key not in built_nodes:
            rlabel = _build_label(resource_key, is_group=False)
            edge_resources.append((resource_key, rtype, rlabel))
            built_nodes[resource_key] = LayoutNode(resource_key, rtype, rlabel)

    # Collect orphan resources — graphdict keys that aren't children of any group
    # and weren't picked up above (e.g. TGW, standalone resources).
    # Place them inside the VPC they connect to, or at region level.
    all_group_children = set()
    for k, children in graphdict.items():
        rtype = _safe_resource_type(k)
        if rtype in GROUP_NODES:
            all_group_children.update(children)

    def _find_parent_vpc(resource_key):
        """Find the VPC LayoutNode that this resource connects to."""
        for conn in graphdict.get(resource_key, []):
            # Check if any connection target is inside a VPC
            if conn in assigned_resources:
                # Walk up the tree to find the VPC
                for node_key, node in built_nodes.items():
                    if not node.is_group:
                        continue
                    if node.resource_type == "aws_vpc":
                        desc = _collect_descendant_resources(node)
                        if conn in desc:
                            return node
        return None

    # Find the region node to use as fallback parent for orphans
    region_node = None
    for child in root.children:
        if child.resource_type == "tv_aws_region":
            region_node = child
            break

    for resource_key in graphdict:
        rtype = _safe_resource_type(resource_key)
        if rtype in GROUP_NODES:
            continue
        if resource_key in assigned_resources or resource_key in built_nodes:
            continue
        if rtype in OUTER_NODES:
            continue
        if any(rtype.startswith(e) for e in EDGE_NODES):
            continue
        if rtype in HIDE_TYPES:
            continue

        rlabel = _build_label(resource_key, is_group=False)

        # Try to place in connected VPC
        vpc_node = _find_parent_vpc(resource_key)
        if vpc_node:
            vpc_node.resources.append((resource_key, rtype, rlabel))
        elif region_node:
            region_node.resources.append((resource_key, rtype, rlabel))
        else:
            root.resources.append((resource_key, rtype, rlabel))

        assigned_resources.add(resource_key)
        built_nodes[resource_key] = LayoutNode(resource_key, rtype, rlabel)

    # ------------------------------------------------------------------
    # Phase 2: Compute sizes bottom-up
    # ------------------------------------------------------------------

    def _compute_size(node):
        """Compute width/height for a LayoutNode based on children and resources."""
        if not node.is_group:
            node.w = ICON_W
            node.h = ICON_H
            return

        # Recursively size children first
        for child in node.children:
            _compute_size(child)

        # Compute resource footprints to determine grid cell size
        n_res = len(node.resources)
        if n_res > 0:
            footprints = [_estimate_label_footprint(lbl) for _, _, lbl in node.resources]
            cell_w = max(fw for fw, _ in footprints)
            cell_h = max(fh for _, fh in footprints)
            rows = (n_res + RESOURCES_PER_ROW - 1) // RESOURCES_PER_ROW
            cols = min(n_res, RESOURCES_PER_ROW)
            res_block_w = cols * cell_w + (cols - 1) * RESOURCE_GAP
            res_block_h = rows * cell_h + (rows - 1) * RESOURCE_GAP
        else:
            res_block_w = 0
            res_block_h = 0

        # Determine arrangement of child containers
        rtype = node.resource_type
        if rtype in ("aws_az", "tv_aws_az"):
            # AZ: subnets stacked vertically
            children_w = max((c.w for c in node.children), default=0)
            children_h = (
                sum(c.h for c in node.children)
                + max(0, len(node.children) - 1) * SUBNET_SPACING
            )
        elif rtype == "aws_vpc":
            # VPC: AZs arranged horizontally, VPC-level resources below
            children_w = (
                sum(c.w for c in node.children)
                + max(0, len(node.children) - 1) * AZ_SPACING
            )
            children_h = max((c.h for c in node.children), default=0)
            # Add space below AZs for VPC-level resources
            if res_block_h > 0:
                children_h += SUBNET_SPACING + res_block_h
                children_w = max(children_w, res_block_w + 2 * CONTAINER_PAD_SIDE)
        else:
            # Region / Account / other: children arranged horizontally
            children_w = (
                sum(c.w for c in node.children)
                + max(0, len(node.children) - 1) * VPC_SPACING
            )
            children_h = max((c.h for c in node.children), default=0)

        content_w = max(children_w, res_block_w)
        content_h = children_h
        # For non-VPC groups with resources and children, stack resources below children
        if rtype not in ("aws_vpc",) and res_block_h > 0 and children_h > 0:
            content_h += SUBNET_SPACING + res_block_h
        elif rtype not in ("aws_vpc",) and res_block_h > 0:
            content_h = res_block_h

        node.w = max(content_w + 2 * CONTAINER_PAD_SIDE, MIN_CONTAINER_W)
        node.h = max(
            content_h + CONTAINER_PAD_TOP + CONTAINER_PAD_BOTTOM, MIN_CONTAINER_H
        )

    _compute_size(root)

    # ------------------------------------------------------------------
    # Phase 3: Assign positions top-down (parent-relative coords)
    # ------------------------------------------------------------------

    def _assign_positions(node, start_x=0, start_y=0):
        """Assign x, y coordinates within parent for all descendants."""
        node.x = start_x
        node.y = start_y

        if not node.is_group:
            return

        cx = CONTAINER_PAD_SIDE
        cy = CONTAINER_PAD_TOP
        rtype = node.resource_type

        if rtype in ("aws_az", "tv_aws_az"):
            # Stack children vertically
            for child in node.children:
                _assign_positions(child, cx, cy)
                cy += child.h + SUBNET_SPACING
        elif rtype == "aws_vpc":
            # AZs arranged horizontally
            for child in node.children:
                _assign_positions(child, cx, cy)
                cx += child.w + AZ_SPACING
            # VPC-level resources below AZs
            if node.resources:
                az_bottom = CONTAINER_PAD_TOP + max(
                    (c.h for c in node.children), default=0
                )
                res_y = az_bottom + SUBNET_SPACING
                _place_resources_grid(node, CONTAINER_PAD_SIDE, res_y)
        else:
            # Horizontal arrangement for Region / Account
            for child in node.children:
                _assign_positions(child, cx, cy)
                cx += child.w + VPC_SPACING

        # Place resources inside non-VPC containers below children
        if rtype not in ("aws_vpc",) and node.resources:
            child_bottom = CONTAINER_PAD_TOP
            if node.children:
                child_bottom += max(
                    (c.y - node.y + c.h for c in node.children),
                    default=0,
                )
                child_bottom = CONTAINER_PAD_TOP + max(
                    (c.h for c in node.children), default=0
                )
                child_bottom += SUBNET_SPACING
            _place_resources_grid(node, CONTAINER_PAD_SIDE, child_bottom)

    def _place_resources_grid(node, base_x, base_y):
        """Place resource icons in a grid within the parent container.

        Grid cell size is based on the largest footprint (icon + label)
        among all resources in this container. The icon is centered
        horizontally within each cell.
        """
        node.resource_positions = []
        if not node.resources:
            return
        footprints = [_estimate_label_footprint(lbl) for _, _, lbl in node.resources]
        cell_w = max(fw for fw, _ in footprints)
        cell_h = max(fh for _, fh in footprints)
        for i, (rkey, rtype, rlabel) in enumerate(node.resources):
            col = i % RESOURCES_PER_ROW
            row = i // RESOURCES_PER_ROW
            # Center the 48px icon within the cell width
            icon_offset_x = (cell_w - ICON_W) / 2
            rx = base_x + col * (cell_w + RESOURCE_GAP) + icon_offset_x
            ry = base_y + row * (cell_h + RESOURCE_GAP)
            node.resource_positions.append((rkey, rtype, rlabel, rx, ry))

    _assign_positions(root, 30, 30)

    # ------------------------------------------------------------------
    # Phase 4: Emit cells
    # ------------------------------------------------------------------
    doc = DrawioDocument()
    resource_cell_ids = {}  # resource_key -> cell_id (for edges)

    def _emit_node(node, parent_cell_id="1"):
        """Recursively emit mxCell elements for a LayoutNode and its descendants."""
        if not node.is_group:
            return

        style = get_group_style(node.resource_type, node.key)
        if style is None:
            # Unknown group type — use a generic dashed rect
            style = (
                "fillColor=none;strokeColor=#5A6C86;dashed=1;verticalAlign=top;"
                "fontStyle=0;fontColor=#5A6C86;whiteSpace=wrap;html=1;"
            )

        node.cell_id = doc.add_container(
            parent_cell_id, node.label, style, node.x, node.y, node.w, node.h
        )
        resource_cell_ids[node.key] = node.cell_id

        # Emit child containers
        for child in node.children:
            _emit_node(child, node.cell_id)

        # Emit resources inside this container
        for rkey, rtype, rlabel, rx, ry in node.resource_positions:
            rstyle = get_resource_style(rtype)
            rid = doc.add_resource(
                node.cell_id, rlabel, rstyle, rx, ry, ICON_W, ICON_H
            )
            resource_cell_ids[rkey] = rid

    _emit_node(root)

    # Emit outer resources (users, internet) to the left of the account box
    outer_x = 30
    outer_y = root.y + 60
    for rkey, rtype, rlabel in outer_resources:
        rstyle = get_resource_style(rtype)
        fw, fh = _estimate_label_footprint(rlabel)
        rid = doc.add_resource("1", rlabel, rstyle, outer_x - fw - 30, outer_y, ICON_W, ICON_H)
        resource_cell_ids[rkey] = rid
        outer_y += fh + 20

    # Emit edge resources (Route53, CloudFront, etc.) above or beside the account
    edge_x = root.x + CONTAINER_PAD_SIDE
    edge_y = root.y - 80
    for rkey, rtype, rlabel in edge_resources:
        rstyle = get_resource_style(rtype)
        rid = doc.add_resource("1", rlabel, rstyle, edge_x, edge_y)
        resource_cell_ids[rkey] = rid
        edge_x += ICON_W + RESOURCE_GAP + 20

    # ------------------------------------------------------------------
    # Phase 5: Emit edges
    # ------------------------------------------------------------------
    bidir_edges = tfdata.get("bidirectional_edges", set())
    emitted_edges = set()

    for resource_key, connections in graphdict.items():
        rtype = _safe_resource_type(resource_key)
        if rtype in GROUP_NODES:
            continue  # Skip group -> child edges (those are containment, not connections)

        src_id = resource_cell_ids.get(resource_key)
        if src_id is None:
            continue

        for conn_key in connections:
            conn_type = _safe_resource_type(conn_key)
            if conn_type in GROUP_NODES:
                continue

            tgt_id = resource_cell_ids.get(conn_key)
            if tgt_id is None:
                continue

            edge_pair = frozenset((resource_key, conn_key))
            if edge_pair in emitted_edges:
                continue
            emitted_edges.add(edge_pair)

            is_bidir = edge_pair in bidir_edges
            # Use VPC cell as parent for edges between resources in same VPC,
            # or "1" (root layer) for cross-VPC / external edges
            doc.add_edge("1", src_id, tgt_id, bidirectional=is_bidir)

    # ------------------------------------------------------------------
    # Phase 6: Write file
    # ------------------------------------------------------------------
    xml_content = doc.to_xml()
    output_path = f"{outfile}.drawio"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(xml_content)
    click.echo(click.style(f"\nRendering Draw.io Architecture Diagram...", fg="white", bold=True))
    click.echo(f"  Output file: {output_path}")
    click.echo(f"  Completed!")
