"""Draw.io shape mappings for AWS resources.

Maps Terraform resource types to native mxgraph.aws4.* shapes and styles
for generating draw.io XML with proper AWS Architecture diagram styling.
"""

# =============================================================================
# Container / Group styles
# =============================================================================

CONTAINER_BASE = (
    "points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],"
    "[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];"
    "outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;"
    "fontStyle=0;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;"
)

GROUP_STYLES = {
    "aws_account": (
        CONTAINER_BASE
        + "shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_account;"
        "strokeColor=#CD2264;fillColor=none;verticalAlign=top;align=left;"
        "spacingLeft=30;fontColor=#CD2264;dashed=0;"
    ),
    "tv_aws_region": (
        CONTAINER_BASE
        + "shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_region;"
        "strokeColor=#00A4A6;fillColor=none;verticalAlign=top;align=left;"
        "spacingLeft=30;fontColor=#147EBA;dashed=1;"
    ),
    "aws_vpc": (
        CONTAINER_BASE
        + "shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_vpc;"
        "strokeColor=#248814;fillColor=none;verticalAlign=top;align=left;"
        "spacingLeft=30;fontColor=#AAB7B8;dashed=0;"
    ),
    "aws_az": (
        "fillColor=none;strokeColor=#147EBA;dashed=1;verticalAlign=top;"
        "fontStyle=0;fontColor=#147EBA;whiteSpace=wrap;html=1;"
    ),
    "tv_aws_az": (
        "fillColor=none;strokeColor=#147EBA;dashed=1;verticalAlign=top;"
        "fontStyle=0;fontColor=#147EBA;whiteSpace=wrap;html=1;"
    ),
    "aws_subnet_public": (
        CONTAINER_BASE
        + "shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_security_group;"
        "grStroke=0;strokeColor=#7AA116;fillColor=#F2F6E8;verticalAlign=top;"
        "align=left;spacingLeft=30;fontColor=#248814;dashed=0;"
    ),
    "aws_subnet_private": (
        CONTAINER_BASE
        + "shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_security_group;"
        "grStroke=0;strokeColor=#00A4A6;fillColor=#E6F6F7;verticalAlign=top;"
        "align=left;spacingLeft=30;fontColor=#147EBA;dashed=0;"
    ),
    "aws_security_group": (
        CONTAINER_BASE
        + "shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_security_group;"
        "grStroke=0;strokeColor=#DD3522;fillColor=none;verticalAlign=top;"
        "align=left;spacingLeft=30;fontColor=#DD3522;dashed=0;"
    ),
    "aws_autoscaling_group": (
        "fillColor=none;strokeColor=#FF9900;dashed=1;verticalAlign=top;"
        "fontStyle=0;fontColor=#FF9900;whiteSpace=wrap;html=1;"
    ),
    "aws_appautoscaling_target": (
        "fillColor=none;strokeColor=#FF9900;dashed=1;verticalAlign=top;"
        "fontStyle=0;fontColor=#FF9900;whiteSpace=wrap;html=1;"
    ),
    "aws_group": (
        "fillColor=none;strokeColor=#5A6C86;dashed=1;verticalAlign=top;"
        "fontStyle=0;fontColor=#5A6C86;whiteSpace=wrap;html=1;"
    ),
}


# =============================================================================
# Resource icon styles  (Terraform type -> mxgraph.aws4.* shape)
# =============================================================================

_RESOURCE_ICON_BASE = (
    "sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;"
    "strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;"
    "align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;pointerEvents=1;"
)

RESOURCE_SHAPES = {
    # Compute
    "aws_instance": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ec2;",
    "aws_launch_template": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ec2;",
    "aws_lambda_function": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda;",
    "aws_ecs_service": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ecs;",
    "aws_ecs_cluster": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ecs;",
    "aws_fargate": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.fargate;",
    "aws_ecs_fargate": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.fargate;",
    "aws_eks_cluster": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.eks;",
    "aws_eks_node_group": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.eks;",
    "aws_ecr_repository": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ecr;",
    "aws_batch_compute_environment": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.batch;",
    "aws_elastic_beanstalk_application": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elastic_beanstalk;",
    "aws_lightsail_instance": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lightsail;",
    "aws_eip": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.elastic_ip_address;",
    # Network
    "aws_ec2_transit_gateway": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.transit_gateway;",
    "aws_ec2_transit_gateway_vpc_attachment": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.transit_gateway_attachment;",
    "aws_internet_gateway": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.internet_gateway;",
    "aws_nat_gateway": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.nat_gateway;",
    "aws_route_table": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.route_table;",
    "aws_route_table_association": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.route_table;",
    "aws_vpn_gateway": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.vpn_gateway;",
    "aws_vpn_connection": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.site_to_site_vpn;",
    "aws_customer_gateway": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.customer_gateway;",
    "aws_vpc_peering_connection": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.peering_connection;",
    "aws_vpc_endpoint": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.endpoints;",
    "aws_cloudfront_distribution": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloudfront;",
    "aws_route53_record": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.route_53;",
    "aws_route53_zone": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.route_53_hosted_zone;",
    "aws_api_gateway_rest_api": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.api_gateway;",
    "aws_apigatewayv2_api": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.api_gateway;",
    "aws_lb": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elastic_load_balancing;",
    "aws_alb": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.application_load_balancer;",
    "aws_nlb": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.network_load_balancer;",
    "aws_dx_connection": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.direct_connect;",
    "aws_globalaccelerator_accelerator": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.global_accelerator;",
    "aws_network_interface": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.elastic_network_interface;",
    "aws_efs_mount_target": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.elastic_network_interface;",
    # Network Manager / Cloud WAN
    "aws_networkmanager_global_network": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloud_wan;",
    "aws_networkmanager_core_network": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloud_wan;",
    "aws_networkmanager_vpc_attachment": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.transit_gateway_attachment;",
    "aws_networkmanager_connect_attachment": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloud_wan;",
    "aws_networkmanager_connect_peer": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloud_wan;",
    # Storage
    "aws_s3_bucket": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;",
    "aws_efs_file_system": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elastic_file_system;",
    "aws_ebs_volume": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elastic_block_store;",
    "aws_glacier_vault": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3_glacier;",
    "aws_backup_plan": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.backup;",
    # Database
    "aws_rds_cluster": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.rds;",
    "aws_db_instance": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.rds;",
    "aws_dynamodb_table": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.dynamodb;",
    "aws_elasticache_cluster": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elasticache;",
    "aws_elasticache_replication_group": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elasticache;",
    "aws_redshift_cluster": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.redshift;",
    "aws_neptune_cluster": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.neptune;",
    "aws_docdb_cluster": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.documentdb_with_mongodb_compatibility;",
    # Security
    "aws_iam_role": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.identity_and_access_management;",
    "aws_iam_policy": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.identity_and_access_management;",
    "aws_kms_key": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.key_management_service;",
    "aws_acm_certificate": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.certificate_manager;",
    "aws_secretsmanager_secret": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.secrets_manager;",
    "aws_cognito_user_pool": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cognito;",
    "aws_wafv2_web_acl": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.waf;",
    "aws_guardduty_detector": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.guardduty;",
    # Integration
    "aws_sqs_queue": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sqs;",
    "aws_sns_topic": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sns;",
    "aws_sfn_state_machine": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.step_functions;",
    "aws_cloudwatch_event_rule": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.eventbridge;",
    "aws_appsync_graphql_api": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.appsync;",
    "aws_mq_broker": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.mq;",
    # Management
    "aws_cloudwatch_log_group": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloudwatch;",
    "aws_cloudwatch_metric_alarm": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.cloudwatch_alarm;",
    "aws_cloudtrail": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloudtrail;",
    "aws_cloudformation_stack": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloudformation;",
    "aws_ssm_parameter": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.parameter_store;",
    "aws_config_config_rule": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.config;",
    # Analytics
    "aws_kinesis_stream": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.kinesis;",
    "aws_kinesis_firehose_delivery_stream": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.kinesis_data_firehose;",
    "aws_athena_database": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.athena;",
    "aws_glue_job": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.glue;",
    "aws_elasticsearch_domain": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elasticsearch_service;",
    "aws_msk_cluster": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.managed_streaming_for_kafka;",
    # ML
    "aws_sagemaker_endpoint": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sagemaker;",
    "aws_sagemaker_notebook_instance": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.sagemaker_notebook;",
    # General / Edge
    "tv_aws_users": f"{_RESOURCE_ICON_BASE}fillColor=#232F3E;shape=mxgraph.aws4.users;",
    "tv_aws_internet": f"{_RESOURCE_ICON_BASE}fillColor=#232F3E;shape=mxgraph.aws4.internet;",
    "tv_aws_mobile_client": f"{_RESOURCE_ICON_BASE}fillColor=#232F3E;shape=mxgraph.aws4.mobile_client;",
}

# Fallback style for unmapped resource types
FALLBACK_RESOURCE_STYLE = (
    f"{_RESOURCE_ICON_BASE}fillColor=#232F3E;"
    "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.general;"
)


def get_group_style(resource_type, resource_key=""):
    """Return draw.io container style for a group resource type.

    Args:
        resource_type: Terraform resource type (e.g. 'aws_subnet')
        resource_key: Full resource key for context (e.g. 'module.x.aws_subnet.public_a')

    Returns:
        Style string or None if not a known group type.
    """
    if resource_type == "aws_subnet":
        # Detect public vs private via case-insensitive check on resource key
        if "public" in resource_key.lower():
            return GROUP_STYLES["aws_subnet_public"]
        return GROUP_STYLES["aws_subnet_private"]
    return GROUP_STYLES.get(resource_type)


def get_resource_style(resource_type):
    """Return draw.io resource icon style for a Terraform resource type.

    Args:
        resource_type: Terraform resource type (e.g. 'aws_instance')

    Returns:
        Style string (falls back to generic AWS icon).
    """
    return RESOURCE_SHAPES.get(resource_type, FALLBACK_RESOURCE_STYLE)


# =============================================================================
# Change highlighting (create / delete / update borders)
# =============================================================================

CHANGE_HIGHLIGHT = {
    "create": "strokeColor=#00CC00;strokeWidth=3;",   # green border
    "delete": "strokeColor=#FF0000;strokeWidth=3;",   # red border
    "update": "strokeColor=#FF9900;strokeWidth=3;",   # orange border
    "no-op":  "",                                       # unchanged
}


def apply_change_highlight(base_style: str, action: str) -> str:
    """Add a colored border to a draw.io style string to indicate change action.

    Preserves the AWS service category fillColor while adding a visible
    strokeColor/strokeWidth overlay.

    Args:
        base_style: Original draw.io style string.
        action: One of 'create', 'delete', 'update', 'no-op'.

    Returns:
        Modified style string with highlight applied (or unchanged for no-op).
    """
    suffix = CHANGE_HIGHLIGHT.get(action, "")
    if not suffix:
        return base_style
    # Remove any existing strokeColor/strokeWidth so ours wins
    parts = [p for p in base_style.rstrip(";").split(";")
             if not p.startswith("strokeColor=") and not p.startswith("strokeWidth=")]
    return ";".join(parts) + ";" + suffix
