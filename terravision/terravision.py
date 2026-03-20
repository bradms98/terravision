#!/usr/bin/env python
from typing import Any, Dict, List, Optional
import copy
import json
import os
import sys
import click

import modules.annotations as annotations
import modules.drawing as drawing
import modules.graphmaker as graphmaker
import modules.helpers as helpers
import modules.interpreter as interpreter
import modules.tfwrapper as tfwrapper
import modules.resource_handlers as resource_handlers
import modules.llm as llm
import modules.validators as validators
import modules.state_converter as state_converter
from modules.config_loader import load_config
from modules.provider_detector import detect_providers
from importlib.metadata import version

__version__ = version("terravision")


def my_excepthook(exc_type: type, exc_value: BaseException, exc_traceback: Any) -> None:
    """Custom exception hook for unhandled errors."""
    import traceback

    print(f"Unhandled error: {exc_type}, {exc_value}")
    traceback.print_exception(exc_type, exc_value, exc_traceback)


def _show_banner() -> None:
    """Display TerraVision ASCII banner."""
    banner = (
        "\n\n\n"
        " _____                          _     _             \n"
        "/__   \\___ _ __ _ __ __ ___   _(_)___(_) ___  _ __  \n"
        "  / /\\/ _ \\ '__| '__/ _` \\ \\ / / / __| |/ _ \\| '_ \\ \n"
        " / / |  __/ |  | | | (_| |\\ V /| \\__ \\ | (_) | | | |\n"
        " \\/   \\___|_|  |_|  \\__,_| \\_/ |_|___/_|\\___/|_| |_|\n"
        "                                                    \n"
        "\n"
    )
    print(banner)


def _enrich_graph_data(
    tfdata: Dict[str, Any], debug: bool, already_processed: bool
) -> Dict[str, Any]:
    """Enrich graph data with relationships and transformations.

    Args:
        tfdata: Terraform data dictionary
        debug: Enable debug mode
        already_processed: Whether data was already processed

    Returns:
        Enriched tfdata dictionary
    """
    tfdata = interpreter.prefix_module_names(tfdata)
    tfdata = interpreter.resolve_all_variables(tfdata, debug, already_processed)
    tfdata = resource_handlers.handle_special_cases(tfdata)
    tfdata = graphmaker.inject_data_source_nodes(tfdata)
    tfdata = graphmaker.add_relations(tfdata)
    tfdata = graphmaker.consolidate_nodes(tfdata)
    tfdata = annotations.add_annotations(tfdata)
    tfdata = graphmaker.detect_and_set_counts(tfdata)
    tfdata = graphmaker.handle_special_resources(tfdata)
    tfdata = graphmaker.handle_variants(tfdata)
    tfdata = graphmaker.create_multiple_resources(tfdata)
    tfdata = graphmaker.scope_subnet_id_resources(tfdata)
    tfdata = graphmaker.cleanup_cross_subnet_connections(tfdata)
    tfdata = graphmaker.reverse_relations(tfdata)
    # Bidirectional links are now rendered as two-way arrows instead of being removed
    # tfdata = helpers.remove_recursive_links(tfdata)
    tfdata = helpers.find_bidirectional_links(tfdata)
    tfdata = resource_handlers.match_resources(tfdata)

    return tfdata


def _print_graph_debug(outputdict: Dict[str, Any], title: str) -> None:
    """Print formatted graph dictionary for debugging.

    Args:
        outputdict: Dictionary to print
        title: Title to display
    """
    click.echo(click.style(f"\n{title}:\n", fg="white", bold=True))
    click.echo(json.dumps(outputdict, indent=4, sort_keys=True))


def compile_tfdata(
    source: str,
    varfile: List[str],
    workspace: str,
    debug: bool,
    annotate: str = "",
    planfile: str = "",
    graphfile: str = "",
    statefile: str = "",
) -> Dict[str, Any]:
    """Compile Terraform data from source files into enriched graph dictionary.

    Args:
        source: Source path (folder, git URL, or JSON file)
        varfile: List of paths to .tfvars files
        workspace: Terraform workspace name
        debug: Enable debug output and export tracedata
        annotate: Path to custom annotations YAML file
        planfile: Path to pre-generated Terraform plan JSON file
        graphfile: Path to pre-generated Terraform graph DOT file
        statefile: Path to Terraform state JSON file (fallback when no plan changes)

    Returns:
        Enriched tfdata dictionary with graphdict and metadata
    """
    already_processed = False
    if planfile:
        validators.validate_pregenerated_inputs(planfile, graphfile, source, statefile)
        if graphfile:
            tfdata = tfwrapper.process_pregenerated_source(
                planfile, graphfile, source, annotate, debug
            )
        else:
            # State-only mode: planfile + statefile, no graph needed
            click.echo(
                click.style(
                    "\nUsing plan + state files (no graph). "
                    "No Terraform commands will be executed.\n",
                    fg="cyan",
                    bold=True,
                )
            )
            plandata = validators.validate_planfile(planfile)
            state_data = validators.validate_statefile(statefile)
            synthetic_changes = state_converter.state_to_resource_changes(state_data)
            if not synthetic_changes:
                click.echo(
                    click.style(
                        "\nERROR: State file contains no managed resources.\n",
                        fg="red",
                        bold=True,
                    )
                )
                sys.exit(1)
            tfdata = {
                "codepath": os.path.abspath(source) if os.path.isdir(source) else source,
                "workdir": os.getcwd(),
                "plandata": dict(plandata),
                "tf_resources_created": synthetic_changes,
            }
            tfdata["plandata"]["prior_state"] = state_converter.state_to_prior_state(state_data)
            tfdata = tfwrapper.setup_tfdata(tfdata)
            tfdata = graphmaker.infer_relationships_from_metadata(tfdata)
            tfdata = tfwrapper.add_vpc_implied_relations(tfdata)
            tfdata["original_graphdict"] = copy.deepcopy(tfdata["graphdict"])
            tfdata["original_metadata"] = copy.deepcopy(tfdata["meta_data"])
            # Parse source directory for HCL metadata.
            # In state-only mode, external module clones may fail (no git creds
            # in container). Continue without HCL enrichment if that happens —
            # we still have full resource attributes from the state file.
            codepath_list = (
                [tfdata["codepath"]]
                if isinstance(tfdata["codepath"], str)
                else tfdata["codepath"]
            )
            import modules.fileparser as fileparser
            try:
                tfdata = fileparser.read_tfsource(codepath_list, [], annotate, tfdata)
            except SystemExit:
                click.echo(
                    click.style(
                        "\nWARNING: Source parsing failed (external modules unavailable). "
                        "Continuing with state-only data.\n",
                        fg="yellow",
                    )
                )
                # Ensure enrichment pipeline can still run without HCL data
                tfdata.setdefault("all_resource", {})
                tfdata.setdefault("module_source_dict", {})
                tfdata.setdefault("all_variable", {})
                # Detect provider from graphdict keys so detect_providers() is skipped
                from modules.provider_detector import get_provider_for_resource, SUPPORTED_PROVIDERS
                _prov_counts = {}
                for _k in tfdata.get("graphdict", {}):
                    _p = get_provider_for_resource(_k)
                    if _p in SUPPORTED_PROVIDERS:
                        _prov_counts[_p] = _prov_counts.get(_p, 0) + 1
                if _prov_counts:
                    _primary = max(_prov_counts, key=_prov_counts.get)
                    tfdata["provider_detection"] = {
                        "primary_provider": _primary,
                        "providers": list(_prov_counts.keys()),
                        "resource_counts": _prov_counts,
                        "confidence": 1.0,
                    }
    elif source.endswith(".json"):
        validators.validate_source(source)
        tfdata = tfwrapper.load_json_source(source)
        already_processed = True
        if "all_resource" not in tfdata:
            _print_graph_debug(tfdata["graphdict"], "Loaded JSON graphviz dictionary")
    else:
        validators.validate_source(source)
        tfdata = tfwrapper.process_terraform_source(
            source, varfile, workspace, annotate, debug
        )

    # State-only fallback: when plan has no resource_changes and a statefile
    # is provided, populate synthetic entries from the state file.
    if (
        not tfdata.get("tf_resources_created")
        and statefile
    ):
        click.echo(
            click.style(
                "\nNo resource changes in plan — using state file as fallback.\n",
                fg="cyan",
                bold=True,
            )
        )
        state_data = validators.validate_statefile(statefile)
        synthetic_changes = state_converter.state_to_resource_changes(state_data)
        if not synthetic_changes:
            click.echo(
                click.style(
                    "\nERROR: State file contains no managed resources.\n",
                    fg="red",
                    bold=True,
                )
            )
            sys.exit(1)
        tfdata["tf_resources_created"] = synthetic_changes
        # Provide prior_state for inject_data_source_nodes
        if "plandata" not in tfdata:
            tfdata["plandata"] = {}
        tfdata["plandata"]["prior_state"] = state_converter.state_to_prior_state(state_data)
        # Re-run graph building since tf_resources_created was empty on first pass
        if tfdata.get("tfgraph"):
            tfdata = tfwrapper.tf_makegraph(tfdata, debug)
        else:
            tfdata = tfwrapper.setup_tfdata(tfdata)
        tfdata = graphmaker.infer_relationships_from_metadata(tfdata)
        tfdata = tfwrapper.add_vpc_implied_relations(tfdata)
        tfdata["original_graphdict"] = copy.deepcopy(tfdata["graphdict"])
        tfdata["original_metadata"] = copy.deepcopy(tfdata["meta_data"])

    # Detect cloud provider and store in tfdata (multi-cloud support)
    if "all_resource" in tfdata and "provider_detection" not in tfdata:
        try:
            provider_detection = detect_providers(tfdata)
            tfdata["provider_detection"] = provider_detection
            click.echo(
                click.style(
                    f"\nDetected cloud provider: {provider_detection['primary_provider'].upper()} "
                    f"({provider_detection['resource_counts'][provider_detection['primary_provider']]} resources)\n",
                    fg="cyan",
                    bold=True,
                )
            )
        except Exception as e:
            click.echo(
                click.style(
                    f"\nERROR: Failed to detect cloud provider: {e}",
                    fg="red",
                    bold=True,
                )
            )
            sys.exit()

    if "all_resource" in tfdata:
        _print_graph_debug(tfdata["graphdict"], "Terraform JSON graph dictionary")
        tfdata = _enrich_graph_data(tfdata, debug, already_processed)
        tfdata["graphdict"] = helpers.sort_graphdict(tfdata["graphdict"])
        _print_graph_debug(tfdata["graphdict"], "Enriched graphviz dictionary")
    return tfdata


def preflight_check(aibackend: Optional[str] = None) -> None:
    """Check required dependencies and Terraform version compatibility.

    Args:
        aibackend: AI backend to validate ('ollama' or 'bedrock')
    """
    click.echo(click.style("\nPreflight check..", fg="white", bold=True))
    helpers.check_dependencies()
    helpers.check_terraform_version()

    if aibackend:
        # Load default AWS config for preflight (endpoints are the same across providers)
        default_config = load_config("aws")

        if aibackend.lower() == "ollama":
            llm.check_ollama_server(default_config.OLLAMA_HOST)
        elif aibackend.lower() == "bedrock":
            llm.check_bedrock_endpoint(default_config.BEDROCK_API_ENDPOINT)

    click.echo("\n")


@click.version_option(version=__version__, prog_name="terravision")
@click.group()
def cli() -> None:
    """TerraVision generates cloud architecture diagrams and documentation from Terraform scripts.

    For help with a specific command type:
    terravision [COMMAND] --help
    """
    pass


@cli.command()
@click.option("--debug", is_flag=True, default=False, help="Dump exception tracebacks")
@click.option(
    "--source",
    default=".",
    help="Source files location (Git URL, Folder or .JSON file)",
)
@click.option(
    "--workspace",
    multiple=False,
    default="default",
    help="The Terraform workspace to initialise",
)
@click.option(
    "--varfile",
    multiple=True,
    default=[],
    help="Path to .tfvars variables file",
)
@click.option(
    "--outfile",
    default="architecture",
    help="Filename for output diagram (default architecture.dot.png)",
)
@click.option(
    "--format", default="png", help="Output format(png, svg, pdf, jpg, dot etc.)"
)
@click.option(
    "--show", is_flag=True, default=False, help="Show diagram after generation"
)
@click.option(
    "--simplified",
    is_flag=True,
    default=False,
    help="Simplified high level services shown only",
)
@click.option("--annotate", default="", help="Path to custom annotations file (YAML)")
@click.option(
    "--filter",
    "filter_name",
    default="",
    help="Filter profile name from filters/ directory (e.g. network, security)",
)
@click.option(
    "--aibackend",
    default="",
    type=click.Choice(["", "bedrock", "ollama"], case_sensitive=False),
    help="AI backend to use (bedrock or ollama)",
)
@click.option("--avl_classes", hidden=True)
@click.option(
    "--planfile",
    default="",
    type=click.Path(),
    help="Path to Terraform plan JSON (terraform show -json)",
)
@click.option(
    "--graphfile",
    default="",
    type=click.Path(),
    help="Path to Terraform graph DOT (terraform graph)",
)
@click.option(
    "--layout",
    default="grid",
    type=click.Choice(["auto", "grid"], case_sensitive=False),
    help="Layout engine: grid (dot, nested containers) or auto (neato, force-directed)",
)
@click.option(
    "--statefile",
    default="",
    type=click.Path(),
    help="Path to Terraform state JSON (fallback when plan has no changes)",
)
def draw(
    debug: bool,
    source: str,
    workspace: str,
    varfile: tuple,
    outfile: str,
    format: str,
    show: bool,
    simplified: bool,
    annotate: str,
    filter_name: str,
    aibackend: str,
    avl_classes: Any,
    planfile: str,
    graphfile: str,
    layout: str,
    statefile: str,
) -> None:
    """Draw architecture diagram from Terraform code.

    Args:
        debug: Enable debug mode
        source: Source path (Git URL, folder, or .JSON file)
        workspace: Terraform workspace
        varfile: Variable files tuple
        outfile: Output filename
        format: Output format (any Graphviz format: png, svg, pdf, jpg, etc.)
        show: Show diagram after generation
        simplified: Generate simplified diagram
        annotate: Path to annotations file
        aibackend: AI backend to use
        avl_classes: Available classes (hidden)
        planfile: Path to pre-generated Terraform plan JSON file
        graphfile: Path to pre-generated Terraform graph DOT file
        layout: Layout mode (grid or auto)
        statefile: Path to Terraform state JSON (fallback when plan has no changes)
    """
    if not debug:
        sys.excepthook = my_excepthook
    _show_banner()
    if planfile and (workspace != "default" or varfile):
        click.echo(
            click.style(
                "WARNING: --workspace and --varfile are ignored when --planfile is provided.",
                fg="yellow",
            )
        )
    preflight_check(aibackend if not planfile else None)
    tfdata = compile_tfdata(
        source, varfile, workspace, debug, annotate, planfile, graphfile, statefile
    )
    # Pass to LLM if this is not a pregraphed JSON
    if "all_resource" in tfdata and aibackend:
        tfdata = llm.refine_with_llm(tfdata, aibackend, debug)

    # Strip networking groups for simplified diagrams, bridging connections
    if simplified:
        graphmaker.simplify_graphdict(tfdata)
        _print_graph_debug(tfdata["graphdict"], "Simplified graphviz dictionary")

    # Apply filter profile to exclude resource types
    if filter_name:
        graphmaker.filter_graphdict(tfdata, filter_name)
        _print_graph_debug(tfdata["graphdict"], "Filtered graphviz dictionary")

    # Add provider suffix to output filename for non-AWS providers
    final_outfile = outfile
    if tfdata.get("provider_detection"):
        provider = tfdata["provider_detection"].get("primary_provider", "aws")
        if provider != "aws" and not outfile.endswith(f"-{provider}"):
            final_outfile = f"{outfile}-{provider}"

    drawing.render_diagram(tfdata, show, final_outfile, format, source, layout)


@cli.command()
@click.option("--debug", is_flag=True, default=False, help="Dump exception tracebacks")
@click.option(
    "--source",
    default=".",
    help="Source files location (Git URL or folder)",
)
@click.option(
    "--workspace",
    multiple=False,
    default="default",
    help="The Terraform workspace to initialise",
)
@click.option(
    "--varfile", multiple=True, default=[], help="Path to .tfvars variables file"
)
@click.option(
    "--show_services",
    is_flag=True,
    default=False,
    help="Only show unique list of cloud services actually used",
)
@click.option(
    "--outfile",
    default="architecture",
    help="Filename for output list (default architecture.json)",
)
@click.option("--annotate", default="", help="Path to custom annotations file (YAML)")
@click.option(
    "--filter",
    "filter_name",
    default="",
    help="Filter profile name from filters/ directory (e.g. network, security)",
)
@click.option(
    "--simplified",
    is_flag=True,
    default=False,
    help="Simplified high level services shown only",
)
@click.option(
    "--aibackend",
    # type=click.Choice(["bedrock", "ollama"], case_sensitive=False),
    help="AI backend to use (bedrock or ollama)",
)
@click.option("--avl_classes", hidden=True)
@click.option(
    "--planfile",
    default="",
    type=click.Path(),
    help="Path to Terraform plan JSON (terraform show -json)",
)
@click.option(
    "--graphfile",
    default="",
    type=click.Path(),
    help="Path to Terraform graph DOT (terraform graph)",
)
def graphdata(
    debug: bool,
    source: str,
    varfile: tuple,
    workspace: str,
    show_services: bool,
    simplified: bool,
    annotate: str,
    filter_name: str,
    aibackend: str,
    avl_classes: Any,
    outfile: str = "graphdata.json",
    planfile: str = "",
    graphfile: str = "",
) -> None:
    """List cloud resources and relations as JSON.

    Args:
        debug: Enable debug mode
        source: Source path (Git URL, folder, or .JSON file)
        varfile: Variable files tuple
        workspace: Terraform workspace
        show_services: Show only unique services
        simplified: Generate simplified graph data
        annotate: Path to annotations file
        aibackend: AI backend to use
        avl_classes: Available classes (hidden)
        outfile: Output JSON filename
        planfile: Path to pre-generated Terraform plan JSON file
        graphfile: Path to pre-generated Terraform graph DOT file
    """
    if not debug:
        sys.excepthook = my_excepthook
    _show_banner()
    if planfile and (workspace != "default" or varfile):
        click.echo(
            click.style(
                "WARNING: --workspace and --varfile are ignored when --planfile is provided.",
                fg="yellow",
            )
        )
    preflight_check(aibackend if not planfile else None)
    tfdata = compile_tfdata(
        source, varfile, workspace, debug, annotate, planfile, graphfile
    )
    # Pass to LLM if this is not a pregraphed JSON
    if "all_resource" in tfdata and aibackend and (not show_services):
        tfdata = llm.refine_with_llm(tfdata, aibackend, debug)
    if simplified:
        graphmaker.simplify_graphdict(tfdata)
    if filter_name:
        graphmaker.filter_graphdict(tfdata, filter_name)
    click.echo(click.style("\nFinal Output JSON Dictionary :", fg="white", bold=True))
    unique = helpers.unique_services(tfdata["graphdict"])
    click.echo(
        json.dumps(
            tfdata["graphdict"] if not show_services else unique,
            indent=4,
            sort_keys=True,
        )
    )
    if not outfile.endswith(".json"):
        outfile += ".json"
    click.echo(f"\nExporting graph object into file {outfile}")
    with open(outfile, "w") as f:
        json.dump(
            tfdata["graphdict"] if not show_services else unique,
            f,
            indent=4,
            sort_keys=True,
        )
    click.echo("\nCompleted!")


def main():
    cli(
        default_map={
            "draw": {"avl_classes": dir()},
            "graphdata": {"avl_classes": dir()},
        }
    )


if __name__ == "__main__":
    main()
