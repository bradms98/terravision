"""Native draw.io XML renderer for TerraVision.

Generates mxfile XML with nested AWS Architecture containers (Account > Region
> VPC > AZ > Subnet) using native mxgraph.aws4.* shapes, bypassing Graphviz
entirely.
"""

import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional, Tuple

import click

import modules.helpers as helpers
from modules.drawio_shapes import get_group_style, get_resource_style, apply_change_highlight

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

    # Extract AWS account ID from plan data for account label
    _account_id = None
    plandata = tfdata.get("plandata", {})
    def _find_account_id(obj):
        if isinstance(obj, dict):
            if "account_id" in obj and isinstance(obj["account_id"], str):
                return obj["account_id"]
            for v in obj.values():
                result = _find_account_id(v)
                if result:
                    return result
        elif isinstance(obj, list):
            for v in obj:
                result = _find_account_id(v)
                if result:
                    return result
        return None
    _account_id = _find_account_id(plandata)

    def _build_label(resource_key, is_group=False):
        """Build a plain-text label for draw.io (no Graphviz markup)."""
        resource_type = _safe_resource_type(resource_key)
        type_label = helpers.pretty_name(resource_key, show_title=False, is_group=True)
        name_tag = helpers.get_name_tag(resource_key, tfdata)
        cidr = helpers.get_cidr_label(resource_key, tfdata)
        resource_id = helpers.get_resource_id(resource_key, tfdata)

        if is_group:
            # For containers: Type - Name on line 1, resource ID on line 2, CIDR on line 3
            parts = [type_label]
            if name_tag:
                parts[0] = f"{type_label} - {name_tag}"
            # Account node: use account ID from plan data
            if resource_type == "aws_account" and _account_id:
                parts.append(_account_id)
            elif resource_id:
                parts.append(resource_id)
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

    # Resource types to hide (loaded from filters/default.yaml)
    HIDE_TYPES = set()
    try:
        import yaml
        from pathlib import Path
        _default_filter = Path(__file__).resolve().parent.parent / "filters" / "default.yaml"
        if _default_filter.exists():
            with open(_default_filter) as _f:
                _filter_data = yaml.safe_load(_f)
            HIDE_TYPES = set(_filter_data.get("exclude", []))
    except Exception:
        pass

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

    def _resolve_route_table(assoc_key, preferred_vpc_prefix=""):
        """Follow a route_table_association's connections to find its route_table.

        When multiple route tables are found (cross-VPC for_each expansion),
        prefer the one matching the given VPC module prefix.

        Returns route_table_key or None.
        """
        candidates = []
        for conn in graphdict.get(assoc_key, []):
            conn_type = _safe_resource_type(conn)
            if conn_type == "aws_route_table":
                candidates.append(conn)
        if not candidates:
            return None
        # Prefer candidate matching the container's VPC prefix
        if preferred_vpc_prefix:
            for c in candidates:
                if _get_module_prefix(c) == preferred_vpc_prefix:
                    return c
        return candidates[0]

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

            # --- Route table association → promote to route table icon ---
            # Processed BEFORE assigned_resources check since associations
            # may be shared across VPCs via for_each expansion, and route
            # tables are allowed to appear in multiple subnets.
            if child_type == "aws_route_table_association":
                container_vpc_prefix = _get_module_prefix(resource_key)
                rt_key = _resolve_route_table(child_key, preferred_vpc_prefix=container_vpc_prefix)
                if rt_key and rt_key not in seen_rt_in_subnet:
                    # Only promote if the route table belongs to the same VPC scope
                    rt_prefix = _get_module_prefix(rt_key)
                    if not rt_prefix or not container_vpc_prefix or rt_prefix == container_vpc_prefix or rt_prefix not in vpc_module_prefixes:
                        rlabel = _build_label(rt_key, is_group=False)
                        node.resources.append((rt_key, "aws_route_table", rlabel))
                        seen_rt_in_subnet.add(rt_key)
                continue  # always skip the association itself

            if child_key in assigned_resources:
                continue
            if child_key in descendant_keys:
                continue

            # --- Hide overly-granular types ---
            if child_type in HIDE_TYPES:
                continue

            # --- At VPC level, skip route tables (promoted into subnets) and
            # IGW (positioned as edge resource straddling VPC border) ---
            if resource_type == "aws_vpc" and child_type in ("aws_route_table", "aws_internet_gateway"):
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

        # Sort: regular resources first, then route tables, then networkmanager
        # (networkmanager renders in a separate horizontal row at the bottom)
        if node.resources:
            def _resource_sort_key(r):
                if r[1].startswith("aws_networkmanager_"):
                    return 2
                if r[1] == "aws_route_table":
                    return 1
                return 0
            node.resources.sort(key=_resource_sort_key)

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

    # Fallback: ensure every subnet has a route table by inheriting from
    # siblings in the same VPC when the graphdict association is incomplete
    def _fill_missing_route_tables(node):
        """For subnets missing a route table, copy one from a sibling."""
        if node.resource_type == "aws_vpc":
            # Collect all route tables from descendant subnets, keyed by public/private
            public_rt = None
            private_rt = None
            subnets_missing_rt = []

            def _scan_subnets(n):
                nonlocal public_rt, private_rt
                if n.resource_type == "aws_subnet":
                    has_rt = any(rt == "aws_route_table" for _, rt, _ in n.resources)
                    is_public = "public" in n.key.lower()
                    if has_rt:
                        for rkey, rtype, rlabel in n.resources:
                            if rtype == "aws_route_table":
                                if is_public and not public_rt:
                                    public_rt = (rkey, rtype, rlabel)
                                elif not is_public and not private_rt:
                                    private_rt = (rkey, rtype, rlabel)
                    else:
                        subnets_missing_rt.append((n, is_public))
                for child in n.children:
                    _scan_subnets(child)

            _scan_subnets(node)

            for subnet_node, is_public in subnets_missing_rt:
                rt = public_rt if is_public else private_rt
                if rt:
                    subnet_node.resources.append(rt)
                    # Re-sort to keep route tables last
                    subnet_node.resources.sort(
                        key=lambda r: (2 if r[1].startswith("aws_networkmanager_") else
                                       1 if r[1] == "aws_route_table" else 0)
                    )

        for child in node.children:
            _fill_missing_route_tables(child)

    _fill_missing_route_tables(root)

    # Collect "outer" resources (users, internet, etc.) and edge resources
    outer_resources = []
    edge_resources = []
    for resource_key in graphdict:
        rtype = _safe_resource_type(resource_key)
        if rtype in OUTER_NODES and resource_key not in built_nodes and resource_key not in assigned_resources:
            rlabel = _build_label(resource_key, is_group=False)
            outer_resources.append((resource_key, rtype, rlabel))
            built_nodes[resource_key] = LayoutNode(resource_key, rtype, rlabel)
        elif any(rtype.startswith(e) for e in EDGE_NODES) and resource_key not in built_nodes and resource_key not in assigned_resources:
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

        # Compute resource footprints, splitting networkmanager into separate row
        regular_res = [r for r in node.resources if not r[1].startswith("aws_networkmanager_")]
        nm_res = [r for r in node.resources if r[1].startswith("aws_networkmanager_")]

        res_block_w = 0
        res_block_h = 0
        if regular_res:
            reg_fp = [_estimate_label_footprint(lbl) for _, _, lbl in regular_res]
            reg_cell_w = max(fw for fw, _ in reg_fp)
            reg_cell_h = max(fh for _, fh in reg_fp)
            reg_rows = (len(regular_res) + RESOURCES_PER_ROW - 1) // RESOURCES_PER_ROW
            reg_cols = min(len(regular_res), RESOURCES_PER_ROW)
            res_block_w = reg_cols * reg_cell_w + (reg_cols - 1) * RESOURCE_GAP
            res_block_h = reg_rows * reg_cell_h + (reg_rows - 1) * RESOURCE_GAP
        if nm_res:
            nm_fp = [_estimate_label_footprint(lbl) for _, _, lbl in nm_res]
            nm_cell_w = max(fw for fw, _ in nm_fp)
            nm_cell_h = max(fh for _, fh in nm_fp)
            nm_row_w = len(nm_res) * nm_cell_w + (len(nm_res) - 1) * RESOURCE_GAP
            res_block_w = max(res_block_w, nm_row_w)
            if res_block_h > 0:
                res_block_h += RESOURCE_GAP
            res_block_h += nm_cell_h

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

    # Equalize subnet widths within each AZ so columns look uniform
    def _equalize_subnet_widths(node):
        if node.resource_type in ("aws_az", "tv_aws_az") and node.children:
            max_w = max(c.w for c in node.children)
            for c in node.children:
                c.w = max_w
        for child in node.children:
            _equalize_subnet_widths(child)

    _equalize_subnet_widths(root)

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
                child_bottom = CONTAINER_PAD_TOP + max(
                    (c.h for c in node.children), default=0
                )
                child_bottom += SUBNET_SPACING
            _place_resources_grid(node, CONTAINER_PAD_SIDE, child_bottom)

            # Center TGW resources horizontally within the region container
            if rtype == "tv_aws_region":
                tgw_positions = [
                    (i, rp) for i, rp in enumerate(node.resource_positions)
                    if rp[1].startswith("aws_ec2_transit_gateway")
                ]
                if tgw_positions:
                    tgw_fps = [_estimate_label_footprint(rp[2]) for _, rp in tgw_positions]
                    total_w = sum(fw for fw, _ in tgw_fps) + (len(tgw_fps) - 1) * RESOURCE_GAP
                    start_x = (node.w - total_w) / 2
                    for j, (idx, (rkey, rt, rl, rx, ry)) in enumerate(tgw_positions):
                        fw, _ = tgw_fps[j]
                        new_rx = start_x + sum(tgw_fps[k][0] + RESOURCE_GAP for k in range(j))
                        new_rx += (fw - ICON_W) / 2  # center icon in footprint
                        node.resource_positions[idx] = (rkey, rt, rl, new_rx, ry)

    def _place_resources_grid(node, base_x, base_y):
        """Place resource icons in a grid within the parent container.

        Grid cell size is based on the largest footprint (icon + label)
        among all resources in this container. The icon is centered
        horizontally within each cell. Networkmanager resources are placed
        in a separate horizontal row at the bottom, left-aligned.
        """
        node.resource_positions = []
        if not node.resources:
            return

        # Split into regular resources and networkmanager resources
        regular = [(r, _estimate_label_footprint(r[2])) for r in node.resources
                    if not r[1].startswith("aws_networkmanager_")]
        nm_res = [(r, _estimate_label_footprint(r[2])) for r in node.resources
                   if r[1].startswith("aws_networkmanager_")]

        # Place regular resources in the standard grid
        cur_y = base_y
        if regular:
            cell_w = max(fw for _, (fw, _) in regular)
            cell_h = max(fh for _, (_, fh) in regular)
            for i, ((rkey, rtype, rlabel), _) in enumerate(regular):
                col = i % RESOURCES_PER_ROW
                row = i // RESOURCES_PER_ROW
                icon_offset_x = (cell_w - ICON_W) / 2
                rx = base_x + col * (cell_w + RESOURCE_GAP) + icon_offset_x
                ry = base_y + row * (cell_h + RESOURCE_GAP)
                node.resource_positions.append((rkey, rtype, rlabel, rx, ry))
            n_rows = (len(regular) + RESOURCES_PER_ROW - 1) // RESOURCES_PER_ROW
            cur_y = base_y + n_rows * (cell_h + RESOURCE_GAP)

        # Place networkmanager resources in a horizontal row below
        if nm_res:
            nm_cell_w = max(fw for _, (fw, _) in nm_res)
            nm_cell_h = max(fh for _, (_, fh) in nm_res)
            if regular:
                cur_y += RESOURCE_GAP  # extra gap before nm row
            for i, ((rkey, rtype, rlabel), _) in enumerate(nm_res):
                icon_offset_x = (nm_cell_w - ICON_W) / 2
                rx = base_x + i * (nm_cell_w + RESOURCE_GAP) + icon_offset_x
                ry = cur_y
                node.resource_positions.append((rkey, rtype, rlabel, rx, ry))

    _assign_positions(root, 30, 30)

    def _is_ancestor(ancestor_node, descendant_node):
        """Check if ancestor_node contains descendant_node in its tree."""
        if ancestor_node is descendant_node:
            return True
        for child in ancestor_node.children:
            if _is_ancestor(child, descendant_node):
                return True
        return False

    def _absolute_position(target_node):
        """Compute absolute (page-level) x, y of a node by walking from root."""
        def _walk(node, ax, ay):
            ax += node.x
            ay += node.y
            if node is target_node:
                return ax, ay
            for child in node.children:
                result = _walk(child, ax, ay)
                if result:
                    return result
            return None
        result = _walk(root, 0, 0)
        return result if result else (target_node.x, target_node.y)

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

        # Apply change highlighting to container
        container_action = tfdata["meta_data"].get(node.key, {}).get("_change_action", "no-op")
        style = apply_change_highlight(style, container_action)

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
            action = tfdata["meta_data"].get(rkey, {}).get("_change_action", "no-op")
            rstyle = apply_change_highlight(rstyle, action)
            rid = doc.add_resource(
                node.cell_id, rlabel, rstyle, rx, ry, ICON_W, ICON_H
            )
            resource_cell_ids[rkey] = rid

    _emit_node(root)

    # Emit outer resources (users, internet) to the left of the account box
    # Internet icon is centered above the account container
    outer_x = 30
    outer_y = root.y + 60
    for rkey, rtype, rlabel in outer_resources:
        rstyle = get_resource_style(rtype)
        action = tfdata["meta_data"].get(rkey, {}).get("_change_action", "no-op")
        rstyle = apply_change_highlight(rstyle, action)
        fw, fh = _estimate_label_footprint(rlabel)
        if rtype == "tv_aws_internet":
            # Center above the account container
            internet_x = root.x + root.w / 2 - ICON_W / 2
            internet_y = root.y - fh - 20
            rid = doc.add_resource("1", rlabel, rstyle, internet_x, internet_y, ICON_W, ICON_H)
        else:
            rid = doc.add_resource("1", rlabel, rstyle, outer_x - fw - 30, outer_y, ICON_W, ICON_H)
            outer_y += fh + 20
        resource_cell_ids[rkey] = rid

    # Emit edge resources (Route53, CloudFront, etc.) above or beside the account
    # IGW is special: centered at the top of its connected VPC, straddling the border
    def _find_connected_vpc_node(resource_key):
        """Find the VPC LayoutNode that this resource connects to.

        Checks both the resource's own connections AND VPCs that list
        a matching resource type as a child (handles bare vs module-prefixed keys).
        """
        # Direct check: resource connects to a VPC
        for conn in graphdict.get(resource_key, []):
            conn_type = _safe_resource_type(conn)
            if conn_type == "aws_vpc" and conn in built_nodes:
                return built_nodes[conn]
        # Reverse check: find a VPC whose children include this resource type
        res_type = _safe_resource_type(resource_key)
        for k, children in graphdict.items():
            if _safe_resource_type(k) == "aws_vpc" and k in built_nodes:
                for child in children:
                    if _safe_resource_type(child) == res_type:
                        return built_nodes[k]
        return None

    edge_x = root.x + CONTAINER_PAD_SIDE
    edge_y = root.y - 80
    for rkey, rtype, rlabel in edge_resources:
        rstyle = get_resource_style(rtype)
        action = tfdata["meta_data"].get(rkey, {}).get("_change_action", "no-op")
        rstyle = apply_change_highlight(rstyle, action)
        if rtype == "aws_internet_gateway":
            # Place straddling the top border of the connected VPC
            vpc_node = _find_connected_vpc_node(rkey)
            if vpc_node and vpc_node.cell_id:
                abs_x, abs_y = _absolute_position(vpc_node)
                igw_x = abs_x + vpc_node.w / 2 - ICON_W / 2
                igw_y = abs_y - ICON_H / 2
                rid = doc.add_resource("1", rlabel, rstyle, igw_x, igw_y, ICON_W, ICON_H)
            else:
                rid = doc.add_resource("1", rlabel, rstyle, edge_x, edge_y, ICON_W, ICON_H)
                edge_x += ICON_W + RESOURCE_GAP + 20
        else:
            rid = doc.add_resource("1", rlabel, rstyle, edge_x, edge_y, ICON_W, ICON_H)
            edge_x += ICON_W + RESOURCE_GAP + 20
        resource_cell_ids[rkey] = rid

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
