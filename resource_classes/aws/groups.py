import sys
import os
import shutil
from pathlib import Path
from resource_classes import Cluster, get_layout_mode

defaultdir = "LR"
base_path = Path(os.path.abspath(os.path.dirname(__file__))).parent.parent


def _dir_for_group(group_type: str) -> str:
    """Return rankdir based on layout mode and group type.

    For grid layout:
      - VPCgroup: LR (AZs arranged side-by-side horizontally)
      - AvailabilityZone: TB (subnets stacked vertically)
      - SubnetGroup: TB (resources within subnet top-to-bottom)
      - Others: TB (top-to-bottom nesting)
    For auto layout: always LR (original behavior)
    """
    if get_layout_mode() == "grid":
        if group_type == "VPCgroup":
            return "LR"
        return "TB"
    return defaultdir


def _margin_for_grid(default_margin: str) -> str:
    """Return tighter margins for grid layout mode."""
    if get_layout_mode() == "grid":
        # Map large neato margins to compact dot margins
        mapping = {"100": "20", "50": "16"}
        return mapping.get(default_margin, default_margin)
    return default_margin


class VPCgroup(Cluster):
    def __init__(self, label, **kwargs):
        vpc_graph_attrs = {
            "style": "solid",
            "margin": _margin_for_grid("50"),
            "pencolor": "#8c4fff",
        }
        if get_layout_mode() != "grid":
            vpc_graph_attrs["rank"] = "same"
        vpc_label = f'<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0"><TR><TD><img src="{base_path}/resource_images/aws/general/vpc.png"/></TD><TD>{label}</TD></TR></TABLE>>'
        super().__init__(vpc_label, _dir_for_group("VPCgroup"), vpc_graph_attrs)


class RegionGroup(Cluster):
    def __init__(self, label, **kwargs):
        region_graph_attrs = {
            "style": "solid",
            "margin": _margin_for_grid("50"),
            "pencolor": "#00a4a6",
        }
        if get_layout_mode() != "grid":
            region_graph_attrs["rank"] = "same"
        if get_layout_mode() == "grid":
            region_graph_attrs["labelloc"] = "t"
            region_graph_attrs["labeljust"] = "l"
        region_label = f'<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0"><TR><TD><img src="{base_path}/resource_images/aws/general/region.png"/></TD><TD>{label}</TD></TR></TABLE>>'
        super().__init__(region_label, _dir_for_group("RegionGroup"), region_graph_attrs)


class SubnetGroup(Cluster):
    def __init__(self, label, **kwargs):
        if "Public" in label:
            image = "public_subnet.png"
            col = "#F2F7EE"
        else:
            image = "private_subnet.png"
            col = "#deebf7"
        vpc_graph_attrs = {
            "style": "filled",
            "margin": _margin_for_grid("50"),
            "color": col,
            "pencolor": "",
            "_shift": "1",
        }
        if get_layout_mode() == "grid":
            vpc_graph_attrs["labelloc"] = "t"
            vpc_graph_attrs["labeljust"] = "l"
        subnet_label = f'<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0"><TR><TD><img src="{base_path}/resource_images/aws/network/{image}"/></TD><TD>{label}</TD></TR></TABLE>>'
        super().__init__(subnet_label, _dir_for_group("SubnetGroup"), vpc_graph_attrs)


class SecurityGroup(Cluster):
    def __init__(self, label, **kwargs):
        vpc_graph_attrs = {"style": "solid", "margin": _margin_for_grid("50"), "pencolor": "red"}
        super().__init__(label, _dir_for_group("SecurityGroup"), vpc_graph_attrs)


class GenericAutoScalingGroup(Cluster):
    def __init__(self, label="AWS AutoScaling", **kwargs):
        graph_attrs = {
            "style": "dashed",
            "margin": _margin_for_grid("50"),
            "color": "#deebf7",
            "pencolor": "pink",
            "labeljust": "c",
            "_shift": "0",
        }
        cluster_label = f'<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0"><TR><TD><img src="{base_path}/resource_images/aws/management/auto-scaling.png"/></TD></TR><TR><TD>{label}</TD></TR></TABLE>>'
        super().__init__(cluster_label, _dir_for_group("GenericAutoScalingGroup"), graph_attrs)


class GenericGroup(Cluster):
    def __init__(self, label="Shared Services", **kwargs):
        graph_attrs = {
            "style": "dashed",
            "margin": _margin_for_grid("100"),
            "pencolor": "black",
        }
        super().__init__(label, _dir_for_group("GenericGroup"), graph_attrs)


class AvailabilityZone(Cluster):
    def __init__(self, label="Availability Zone", **kwargs):
        graph_attrs = {
            "style": "dashed",
            "margin": _margin_for_grid("100"),
            "pencolor": "#3399ff",
            "center": "true",
            "labeljust": "c",
            "_shift": "0",
        }
        if get_layout_mode() == "grid":
            graph_attrs["labelloc"] = "t"
        cluster_label = f'<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0"><TR><TD><FONT point-size="30" color="#3399ff">{label}</FONT></TD></TR></TABLE>>'
        super().__init__(cluster_label, _dir_for_group("AvailabilityZone"), graph_attrs)


class SecurityGroup(Cluster):
    def __init__(self, label="Security Group", **kwargs):
        graph_attrs = {
            "style": "solid",
            "margin": _margin_for_grid("50"),
            "pencolor": "red",
            "center": "true",
            "labeljust": "c",
            "_shift": "0",
        }
        cluster_label = f'<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0"><TR><TD><FONT color="red">{label}</FONT></TD></TR></TABLE>>'
        super().__init__(cluster_label, _dir_for_group("SecurityGroup"), graph_attrs)


class AWSGroup(Cluster):
    def __init__(self, label="AWS Cloud", **kwargs):
        aws_graph_attrs = {
            "style": "solid",
            "pencolor": "black",
            "margin": _margin_for_grid("100"),
            "ordering": "in",
            "penwidth": "2",
            "center": "true",
            "labeljust": "l",
            "_shift": "1",
            "_cloudgroup": "1",
        }
        if get_layout_mode() == "grid":
            aws_graph_attrs["labelloc"] = "t"
        aws_label = f'<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0"><TR><TD><img src="{base_path}/resource_images/aws/general/aws.png"/></TD><TD>{label}</TD></TR></TABLE>>'
        super().__init__(aws_label, _dir_for_group("AWSGroup"), aws_graph_attrs)


class AWSAccount(Cluster):
    def __init__(self, label="AWS Account", **kwargs):
        aws_graph_attrs = {
            "style": "solid",
            "pencolor": "#e7157b",
            "margin": _margin_for_grid("100"),
            "ordering": "in",
            "penwidth": "2",
            "center": "true",
            "labeljust": "l",
            "_shift": "1",
        }
        if get_layout_mode() == "grid":
            aws_graph_attrs["labelloc"] = "t"
        aws_label = f'<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0"><TR><TD><img src="{base_path}/resource_images/aws/general/aws_account.png"/></TD><TD>{label}</TD></TR></TABLE>>'
        super().__init__(aws_label, _dir_for_group("AWSAccount"), aws_graph_attrs)


class OnPrem(Cluster):
    def __init__(self, label="Corporate Datacenter", **kwargs):
        aws_graph_attrs = {
            "style": "solid",
            "pencolor": "black",
            "margin": _margin_for_grid("100"),
            "ordering": "in",
            "center": "true",
            "labeljust": "l",
            "_shift": "1",
        }
        aws_label = f'<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0"><TR><TD><img src="{base_path}/resource_images/aws/general/office-building.png"/></TD><TD>{label}</TD></TR></TABLE>>'
        super().__init__(aws_label, _dir_for_group("OnPrem"), aws_graph_attrs)


aws_vpc = VPCgroup
aws_group = GenericGroup
aws_account = AWSAccount
aws_security_group = SecurityGroup
aws_subnet = SubnetGroup
aws_appautoscaling_target = GenericAutoScalingGroup
aws_autoscaling_group = GenericAutoScalingGroup
tv_aws_onprem = OnPrem
aws_az = AvailabilityZone
tv_aws_az = AvailabilityZone
tv_aws_region = RegionGroup
aws_region = RegionGroup
