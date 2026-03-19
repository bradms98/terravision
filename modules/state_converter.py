"""Convert Terraform state (tfstate v4) into synthetic plan structures.

Allows terravision to draw diagrams from existing infrastructure state
when no plan changes are pending (onboarding / steady-state use case).
"""

import json
from typing import Any, Dict, List


def state_to_resource_changes(state_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Convert tfstate v4 resources into synthetic ``resource_changes`` entries.

    Each managed resource instance becomes a no-op change entry that matches
    the shape produced by ``terraform show -json``.

    Args:
        state_data: Parsed tfstate JSON (version 4).

    Returns:
        List of synthetic resource_changes dicts.
    """
    changes: List[Dict[str, Any]] = []

    for resource in state_data.get("resources", []):
        if resource.get("mode") != "managed":
            continue

        res_type = resource["type"]
        res_name = resource["name"]
        module_addr = resource.get("module", "")

        for instance in resource.get("instances", []):
            # Build the fully-qualified address
            base_address = f"{res_type}.{res_name}"
            if module_addr:
                address = f"{module_addr}.{base_address}"
            else:
                address = base_address

            index_key = instance.get("index_key")

            # Append index suffix to address when count/for_each is used
            if index_key is not None:
                if isinstance(index_key, int):
                    address += f"[{index_key}]"
                else:
                    address += f'["{index_key}"]'

            attributes = instance.get("attributes", {}) or {}

            entry: Dict[str, Any] = {
                "address": address,
                "module_address": module_addr if module_addr else None,
                "mode": "managed",
                "type": res_type,
                "name": res_name,
                "change": {
                    "actions": ["no-op"],
                    "before": dict(attributes),
                    "after": dict(attributes),
                    "after_unknown": {},
                },
            }

            if index_key is not None:
                entry["index"] = index_key

            changes.append(entry)

    return changes


def state_to_prior_state(state_data: Dict[str, Any]) -> Dict[str, Any]:
    """Restructure flat tfstate ``resources`` into ``prior_state.values.root_module``.

    The resulting structure feeds ``graphmaker.inject_data_source_nodes()``
    which expects the nested module hierarchy from a plan's ``prior_state``.

    Args:
        state_data: Parsed tfstate JSON (version 4).

    Returns:
        Dict shaped like ``{"values": {"root_module": {...}}}``.
    """
    root_resources: List[Dict[str, Any]] = []
    child_modules: Dict[str, Dict[str, Any]] = {}

    for resource in state_data.get("resources", []):
        module_addr = resource.get("module", "")

        for instance in resource.get("instances", []):
            attributes = instance.get("attributes", {}) or {}
            base_address = f"{resource['type']}.{resource['name']}"

            index_key = instance.get("index_key")
            if index_key is not None:
                if isinstance(index_key, int):
                    base_address += f"[{index_key}]"
                else:
                    base_address += f'["{index_key}"]'

            entry = {
                "address": base_address if not module_addr else f"{module_addr}.{base_address}",
                "mode": resource.get("mode", "managed"),
                "type": resource["type"],
                "name": resource["name"],
                "values": dict(attributes),
            }

            if module_addr:
                if module_addr not in child_modules:
                    child_modules[module_addr] = {
                        "address": module_addr,
                        "resources": [],
                        "child_modules": [],
                    }
                child_modules[module_addr]["resources"].append(entry)
            else:
                root_resources.append(entry)

    root_module: Dict[str, Any] = {"resources": root_resources}
    if child_modules:
        root_module["child_modules"] = list(child_modules.values())

    return {"values": {"root_module": root_module}}
