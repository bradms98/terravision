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
    # Service group container styles (icon + property-list layout)
    "aws_s3_bucket": (
        "fillColor=none;strokeColor=#3F8624;dashed=0;"
        "fontStyle=0;fontColor=#3F8624;whiteSpace=wrap;html=1;"
        "container=1;collapsible=0;recursiveResize=0;rounded=1;"
    ),
    "aws_backup_vault": (
        "fillColor=none;strokeColor=#E7157B;dashed=0;verticalAlign=top;"
        "fontStyle=0;fontColor=#E7157B;whiteSpace=wrap;html=1;"
        "container=1;collapsible=0;recursiveResize=0;rounded=1;"
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
    # =========================================================================
    # Compute (#ED7100)
    # =========================================================================
    "aws_instance": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ec2;",
    "aws_launch_template": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ec2;",
    "aws_launch_configuration": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ec2;",
    "aws_ami": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.ami;",
    "aws_ami_copy": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.ami;",
    "aws_ami_from_instance": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.ami;",
    "aws_placement_group": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ec2;",
    "aws_key_pair": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ec2;",
    "aws_spot_instance_request": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.spot_instance;",
    "aws_spot_fleet_request": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.spot_instance;",
    "aws_ec2_fleet": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ec2;",
    "aws_ec2_capacity_reservation": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ec2;",
    "aws_ec2_host": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ec2;",
    "aws_lambda_function": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda;",
    "aws_lambda_alias": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda;",
    "aws_lambda_event_source_mapping": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda;",
    "aws_lambda_function_url": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda;",
    "aws_lambda_layer_version": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.lambda_function;",
    "aws_lambda_permission": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda;",
    "aws_lambda_provisioned_concurrency_config": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda;",
    "aws_ecs_service": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ecs;",
    "aws_ecs_cluster": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ecs;",
    "aws_ecs_task_definition": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.ecs_task;",
    "aws_ecs_capacity_provider": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ecs;",
    "aws_ecs_account_setting_default": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ecs;",
    "aws_fargate": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.fargate;",
    "aws_ecs_fargate": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.fargate;",
    "aws_eks_cluster": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.eks;",
    "aws_eks_node_group": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.eks;",
    "aws_eks_addon": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.eks;",
    "aws_eks_fargate_profile": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.eks;",
    "aws_eks_identity_provider_config": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.eks;",
    "aws_ecr_repository": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ecr;",
    "aws_ecr_lifecycle_policy": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ecr;",
    "aws_ecr_repository_policy": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ecr;",
    "aws_ecrpublic_repository": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ecr;",
    "aws_batch_compute_environment": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.batch;",
    "aws_batch_job_definition": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.batch;",
    "aws_batch_job_queue": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.batch;",
    "aws_batch_scheduling_policy": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.batch;",
    "aws_elastic_beanstalk_application": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elastic_beanstalk;",
    "aws_elastic_beanstalk_environment": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elastic_beanstalk;",
    "aws_lightsail_instance": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lightsail;",
    "aws_lightsail_static_ip": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lightsail;",
    "aws_lightsail_domain": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lightsail;",
    "aws_lightsail_key_pair": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lightsail;",
    "aws_apprunner_service": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.app_runner;",
    "aws_apprunner_auto_scaling_configuration_version": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.app_runner;",
    "aws_apprunner_connection": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.app_runner;",
    "aws_apprunner_vpc_connector": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.app_runner;",
    "aws_autoscaling_group": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.auto_scaling2;",
    "aws_autoscaling_policy": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.auto_scaling2;",
    "aws_autoscaling_schedule": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.auto_scaling2;",
    "aws_eip": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.elastic_ip_address;",
    "aws_eip_association": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.elastic_ip_address;",
    # =========================================================================
    # Networking & Content Delivery (#8C4FFF)
    # =========================================================================
    # VPC core
    "aws_vpc": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.vpc;",
    "aws_subnet": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.vpc;",
    "aws_default_vpc": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.vpc;",
    "aws_default_subnet": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.vpc;",
    "aws_ec2_transit_gateway": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.transit_gateway;",
    "aws_ec2_transit_gateway_vpc_attachment": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.transit_gateway_attachment;",
    "aws_ec2_transit_gateway_route": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.transit_gateway;",
    "aws_ec2_transit_gateway_route_table": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.transit_gateway;",
    "aws_ec2_transit_gateway_route_table_association": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.transit_gateway;",
    "aws_ec2_transit_gateway_route_table_propagation": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.transit_gateway;",
    "aws_ec2_transit_gateway_peering_attachment": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.transit_gateway_attachment;",
    "aws_internet_gateway": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.internet_gateway;",
    "aws_egress_only_internet_gateway": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.internet_gateway;",
    "aws_nat_gateway": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.nat_gateway;",
    "aws_route_table": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.route_table;",
    "aws_route": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.route_table;",
    "aws_route_table_association": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.route_table;",
    "aws_main_route_table_association": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.route_table;",
    "aws_vpn_gateway": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.vpn_gateway;",
    "aws_vpn_gateway_attachment": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.vpn_gateway;",
    "aws_vpn_connection": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.site_to_site_vpn;",
    "aws_vpn_connection_route": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.site_to_site_vpn;",
    "aws_customer_gateway": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.customer_gateway;",
    "aws_vpc_peering_connection": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.peering_connection;",
    "aws_vpc_peering_connection_accepter": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.peering_connection;",
    "aws_vpc_endpoint": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.endpoints;",
    "aws_vpc_endpoint_service": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.endpoints;",
    "aws_vpc_endpoint_route_table_association": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.endpoints;",
    "aws_vpc_endpoint_subnet_association": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.endpoints;",
    "aws_vpc_dhcp_options": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.vpc;",
    "aws_vpc_dhcp_options_association": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.vpc;",
    "aws_vpc_ipv4_cidr_block_association": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.vpc;",
    "aws_flow_log": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.vpc;",
    "aws_network_acl": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.network_access_control_list;",
    "aws_network_acl_rule": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.network_access_control_list;",
    "aws_default_network_acl": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.network_access_control_list;",
    "aws_security_group": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.identity_and_access_management;",
    "aws_security_group_rule": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.identity_and_access_management;",
    "aws_default_security_group": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.identity_and_access_management;",
    # CloudFront
    "aws_cloudfront_distribution": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloudfront;",
    "aws_cloudfront_origin_access_identity": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloudfront;",
    "aws_cloudfront_origin_access_control": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloudfront;",
    "aws_cloudfront_cache_policy": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloudfront;",
    "aws_cloudfront_function": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloudfront;",
    "aws_cloudfront_response_headers_policy": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloudfront;",
    # Route 53
    "aws_route53_record": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.route_53;",
    "aws_route53_zone": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.route_53_hosted_zone;",
    "aws_route53_health_check": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.route_53_health_check;",
    "aws_route53_resolver_endpoint": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.route_53_resolver;",
    "aws_route53_resolver_rule": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.route_53_resolver;",
    "aws_route53_delegation_set": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.route_53;",
    "aws_route53_query_log": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.route_53;",
    # API Gateway
    "aws_api_gateway_rest_api": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.api_gateway;",
    "aws_api_gateway_stage": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.api_gateway;",
    "aws_api_gateway_deployment": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.api_gateway;",
    "aws_api_gateway_resource": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.api_gateway;",
    "aws_api_gateway_method": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.api_gateway;",
    "aws_api_gateway_integration": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.api_gateway;",
    "aws_api_gateway_domain_name": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.api_gateway;",
    "aws_api_gateway_base_path_mapping": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.api_gateway;",
    "aws_api_gateway_authorizer": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.api_gateway;",
    "aws_api_gateway_usage_plan": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.api_gateway;",
    "aws_api_gateway_api_key": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.api_gateway;",
    "aws_api_gateway_vpc_link": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.api_gateway;",
    "aws_apigatewayv2_api": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.api_gateway;",
    "aws_apigatewayv2_stage": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.api_gateway;",
    "aws_apigatewayv2_route": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.api_gateway;",
    "aws_apigatewayv2_integration": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.api_gateway;",
    "aws_apigatewayv2_domain_name": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.api_gateway;",
    "aws_apigatewayv2_authorizer": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.api_gateway;",
    "aws_apigatewayv2_vpc_link": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.api_gateway;",
    # Load Balancing
    "aws_lb": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elastic_load_balancing;",
    "aws_alb": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.application_load_balancer;",
    "aws_nlb": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.network_load_balancer;",
    "aws_lb_target_group": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elastic_load_balancing;",
    "aws_alb_target_group": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.application_load_balancer;",
    "aws_lb_listener": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elastic_load_balancing;",
    "aws_alb_listener": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.application_load_balancer;",
    "aws_lb_listener_rule": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elastic_load_balancing;",
    "aws_alb_listener_rule": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.application_load_balancer;",
    "aws_lb_target_group_attachment": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elastic_load_balancing;",
    "aws_alb_target_group_attachment": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.application_load_balancer;",
    # Direct Connect
    "aws_dx_connection": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.direct_connect;",
    "aws_dx_gateway": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.direct_connect;",
    "aws_dx_gateway_association": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.direct_connect;",
    "aws_dx_private_virtual_interface": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.direct_connect;",
    "aws_dx_public_virtual_interface": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.direct_connect;",
    "aws_dx_transit_virtual_interface": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.direct_connect;",
    # Global Accelerator
    "aws_globalaccelerator_accelerator": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.global_accelerator;",
    "aws_globalaccelerator_listener": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.global_accelerator;",
    "aws_globalaccelerator_endpoint_group": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.global_accelerator;",
    # Network interfaces
    "aws_network_interface": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.elastic_network_interface;",
    "aws_network_interface_attachment": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.elastic_network_interface;",
    "aws_efs_mount_target": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.elastic_network_interface;",
    # Network Firewall
    "aws_networkfirewall_firewall": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.network_firewall;",
    "aws_networkfirewall_firewall_policy": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.network_firewall;",
    "aws_networkfirewall_rule_group": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.network_firewall;",
    # Network Manager / Cloud WAN
    "aws_networkmanager_global_network": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloud_wan;",
    "aws_networkmanager_core_network": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloud_wan;",
    "aws_networkmanager_vpc_attachment": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.transit_gateway_attachment;",
    "aws_networkmanager_connect_attachment": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloud_wan;",
    "aws_networkmanager_connect_peer": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloud_wan;",
    "aws_networkmanager_site": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloud_wan;",
    # App Mesh
    "aws_appmesh_mesh": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.app_mesh;",
    "aws_appmesh_virtual_service": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.app_mesh;",
    "aws_appmesh_virtual_node": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.app_mesh;",
    "aws_appmesh_virtual_router": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.app_mesh;",
    "aws_appmesh_virtual_gateway": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.app_mesh;",
    # PrivateLink / Client VPN
    "aws_ec2_client_vpn_endpoint": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.client_vpn;",
    "aws_ec2_client_vpn_network_association": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.client_vpn;",
    "aws_vpc_endpoint_connection_notification": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.endpoints;",
    # =========================================================================
    # Storage (#3F8624)
    # =========================================================================
    # S3
    "aws_s3_bucket": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;",
    "aws_s3_bucket_policy": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;",
    "aws_s3_bucket_public_access_block": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;",
    "aws_s3_bucket_server_side_encryption_configuration": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;",
    "aws_s3_bucket_versioning": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;",
    "aws_s3_bucket_lifecycle_configuration": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;",
    "aws_s3_bucket_ownership_controls": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;",
    "aws_s3_bucket_intelligent_tiering_configuration": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;",
    "aws_s3_bucket_acl": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;",
    "aws_s3_bucket_cors_configuration": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;",
    "aws_s3_bucket_logging": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;",
    "aws_s3_bucket_notification": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;",
    "aws_s3_bucket_object": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;",
    "aws_s3_object": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;",
    "aws_s3_bucket_replication_configuration": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;",
    "aws_s3_bucket_website_configuration": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;",
    "aws_s3_bucket_metric": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;",
    "aws_s3_bucket_analytics_configuration": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;",
    "aws_s3_bucket_inventory": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;",
    "aws_s3_bucket_object_lock_configuration": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;",
    "aws_s3_access_point": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;",
    "aws_s3_account_public_access_block": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;",
    # EFS
    "aws_efs_file_system": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elastic_file_system;",
    "aws_efs_access_point": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elastic_file_system;",
    "aws_efs_file_system_policy": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elastic_file_system;",
    # EBS
    "aws_ebs_volume": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elastic_block_store;",
    "aws_ebs_snapshot": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elastic_block_store;",
    "aws_ebs_snapshot_copy": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elastic_block_store;",
    "aws_volume_attachment": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elastic_block_store;",
    "aws_ebs_encryption_by_default": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elastic_block_store;",
    # Glacier
    "aws_glacier_vault": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3_glacier;",
    "aws_glacier_vault_lock": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3_glacier;",
    # FSx
    "aws_fsx_lustre_file_system": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.fsx;",
    "aws_fsx_windows_file_system": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.fsx;",
    "aws_fsx_ontap_file_system": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.fsx;",
    "aws_fsx_openzfs_file_system": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.fsx;",
    # Storage Gateway
    "aws_storagegateway_gateway": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.storage_gateway;",
    "aws_storagegateway_nfs_file_share": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.storage_gateway;",
    "aws_storagegateway_smb_file_share": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.storage_gateway;",
    "aws_storagegateway_cache": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.storage_gateway;",
    # Backup
    "aws_backup_plan": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.backup;",
    "aws_backup_selection": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.backup;",
    "aws_backup_vault": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.backup;",
    "aws_backup_vault_lock_configuration": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.backup;",
    "aws_backup_vault_policy": f"{_RESOURCE_ICON_BASE}fillColor=#3F8624;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.backup;",
    # =========================================================================
    # Database (#C925D1)
    # =========================================================================
    # RDS
    "aws_rds_cluster": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.rds;",
    "aws_rds_cluster_instance": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.rds;",
    "aws_rds_cluster_endpoint": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.rds;",
    "aws_rds_cluster_parameter_group": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.rds;",
    "aws_rds_global_cluster": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.rds;",
    "aws_db_instance": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.rds;",
    "aws_db_subnet_group": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.rds;",
    "aws_db_parameter_group": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.rds;",
    "aws_db_option_group": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.rds;",
    "aws_db_proxy": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.rds_proxy_instance;",
    "aws_db_proxy_default_target_group": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.rds_proxy_instance;",
    "aws_db_proxy_target": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.rds_proxy_instance;",
    "aws_db_snapshot": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.rds;",
    "aws_db_instance_automated_backups_replication": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.rds;",
    "aws_db_event_subscription": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.rds;",
    # DynamoDB
    "aws_dynamodb_table": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.dynamodb;",
    "aws_dynamodb_table_item": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.dynamodb;",
    "aws_dynamodb_global_table": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.dynamodb;",
    "aws_dynamodb_kinesis_streaming_destination": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.dynamodb;",
    "aws_dynamodb_contributor_insights": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.dynamodb;",
    "aws_dynamodb_table_replica": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.dynamodb;",
    # ElastiCache
    "aws_elasticache_cluster": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elasticache;",
    "aws_elasticache_replication_group": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elasticache;",
    "aws_elasticache_subnet_group": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elasticache;",
    "aws_elasticache_parameter_group": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elasticache;",
    "aws_elasticache_user": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elasticache;",
    "aws_elasticache_user_group": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elasticache;",
    # Redshift
    "aws_redshift_cluster": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.redshift;",
    "aws_redshift_subnet_group": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.redshift;",
    "aws_redshift_parameter_group": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.redshift;",
    "aws_redshift_security_group": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.redshift;",
    "aws_redshift_snapshot_schedule": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.redshift;",
    "aws_redshiftserverless_namespace": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.redshift;",
    "aws_redshiftserverless_workgroup": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.redshift;",
    # Neptune
    "aws_neptune_cluster": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.neptune;",
    "aws_neptune_cluster_instance": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.neptune;",
    "aws_neptune_cluster_parameter_group": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.neptune;",
    "aws_neptune_subnet_group": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.neptune;",
    # DocumentDB
    "aws_docdb_cluster": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.documentdb_with_mongodb_compatibility;",
    "aws_docdb_cluster_instance": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.documentdb_with_mongodb_compatibility;",
    "aws_docdb_cluster_parameter_group": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.documentdb_with_mongodb_compatibility;",
    "aws_docdb_subnet_group": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.documentdb_with_mongodb_compatibility;",
    # Timestream
    "aws_timestreamwrite_database": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.timestream;",
    "aws_timestreamwrite_table": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.timestream;",
    # QLDB
    "aws_qldb_ledger": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.qldb;",
    "aws_qldb_stream": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.qldb;",
    # MemoryDB
    "aws_memorydb_cluster": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elasticache;",
    "aws_memorydb_subnet_group": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elasticache;",
    # Keyspaces (Cassandra)
    "aws_keyspaces_keyspace": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.keyspaces;",
    "aws_keyspaces_table": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.keyspaces;",
    # DAX
    "aws_dax_cluster": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.dynamodb_accelerator;",
    "aws_dax_subnet_group": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.dynamodb_accelerator;",
    "aws_dax_parameter_group": f"{_RESOURCE_ICON_BASE}fillColor=#C925D1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.dynamodb_accelerator;",
    # =========================================================================
    # Security, Identity & Compliance (#DD344C)
    # =========================================================================
    # IAM
    "aws_iam_role": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.identity_and_access_management;",
    "aws_iam_role_policy": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.identity_and_access_management;",
    "aws_iam_role_policy_attachment": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.identity_and_access_management;",
    "aws_iam_policy": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.identity_and_access_management;",
    "aws_iam_policy_attachment": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.identity_and_access_management;",
    "aws_iam_user": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.identity_and_access_management;",
    "aws_iam_user_policy": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.identity_and_access_management;",
    "aws_iam_user_policy_attachment": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.identity_and_access_management;",
    "aws_iam_group": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.identity_and_access_management;",
    "aws_iam_group_policy": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.identity_and_access_management;",
    "aws_iam_group_policy_attachment": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.identity_and_access_management;",
    "aws_iam_group_membership": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.identity_and_access_management;",
    "aws_iam_instance_profile": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.identity_and_access_management;",
    "aws_iam_openid_connect_provider": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.identity_and_access_management;",
    "aws_iam_saml_provider": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.identity_and_access_management;",
    "aws_iam_server_certificate": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.identity_and_access_management;",
    "aws_iam_access_key": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.identity_and_access_management;",
    "aws_iam_account_alias": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.identity_and_access_management;",
    "aws_iam_account_password_policy": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.identity_and_access_management;",
    "aws_iam_service_linked_role": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.identity_and_access_management;",
    # KMS
    "aws_kms_key": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.key_management_service;",
    "aws_kms_alias": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.key_management_service;",
    "aws_kms_grant": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.key_management_service;",
    "aws_kms_ciphertext": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.key_management_service;",
    "aws_kms_replica_key": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.key_management_service;",
    "aws_kms_external_key": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.key_management_service;",
    # ACM
    "aws_acm_certificate": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.certificate_manager;",
    "aws_acm_certificate_validation": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.certificate_manager;",
    "aws_acmpca_certificate_authority": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.certificate_manager;",
    # Secrets Manager
    "aws_secretsmanager_secret": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.secrets_manager;",
    "aws_secretsmanager_secret_version": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.secrets_manager;",
    "aws_secretsmanager_secret_rotation": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.secrets_manager;",
    "aws_secretsmanager_secret_policy": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.secrets_manager;",
    # Cognito
    "aws_cognito_user_pool": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cognito;",
    "aws_cognito_user_pool_client": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cognito;",
    "aws_cognito_user_pool_domain": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cognito;",
    "aws_cognito_identity_pool": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cognito;",
    "aws_cognito_identity_pool_roles_attachment": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cognito;",
    "aws_cognito_resource_server": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cognito;",
    "aws_cognito_user_group": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cognito;",
    # WAF
    "aws_wafv2_web_acl": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.waf;",
    "aws_wafv2_web_acl_association": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.waf;",
    "aws_wafv2_ip_set": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.waf;",
    "aws_wafv2_rule_group": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.waf;",
    "aws_wafv2_regex_pattern_set": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.waf;",
    "aws_waf_web_acl": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.waf;",
    "aws_waf_rule": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.waf;",
    "aws_waf_ipset": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.waf;",
    "aws_wafregional_web_acl": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.waf;",
    # GuardDuty
    "aws_guardduty_detector": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.guardduty;",
    "aws_guardduty_member": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.guardduty;",
    "aws_guardduty_organization_admin_account": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.guardduty;",
    "aws_guardduty_organization_configuration": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.guardduty;",
    # Security Hub
    "aws_securityhub_account": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.security_hub;",
    "aws_securityhub_member": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.security_hub;",
    "aws_securityhub_standards_subscription": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.security_hub;",
    "aws_securityhub_finding_aggregator": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.security_hub;",
    # Inspector
    "aws_inspector_assessment_target": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.inspector;",
    "aws_inspector_assessment_template": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.inspector;",
    "aws_inspector2_enabler": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.inspector;",
    # Macie
    "aws_macie2_account": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.macie;",
    "aws_macie2_classification_job": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.macie;",
    # Shield
    "aws_shield_protection": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.shield;",
    "aws_shield_protection_group": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.shield;",
    # Directory Service
    "aws_directory_service_directory": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.directory_service;",
    # Firewall Manager
    "aws_fms_policy": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.firewall_manager;",
    "aws_fms_admin_account": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.firewall_manager;",
    # SSO / Identity Center
    "aws_ssoadmin_permission_set": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.single_sign_on;",
    "aws_ssoadmin_account_assignment": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.single_sign_on;",
    "aws_identitystore_user": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.single_sign_on;",
    "aws_identitystore_group": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.single_sign_on;",
    # STS
    "aws_iam_service_specific_credential": f"{_RESOURCE_ICON_BASE}fillColor=#DD344C;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.identity_and_access_management;",
    # =========================================================================
    # Application Integration (#E7157B)
    # =========================================================================
    # SQS
    "aws_sqs_queue": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sqs;",
    "aws_sqs_queue_policy": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sqs;",
    "aws_sqs_queue_redrive_policy": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sqs;",
    "aws_sqs_queue_redrive_allow_policy": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sqs;",
    # SNS
    "aws_sns_topic": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sns;",
    "aws_sns_topic_policy": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sns;",
    "aws_sns_topic_subscription": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sns;",
    "aws_sns_platform_application": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sns;",
    "aws_sns_sms_preferences": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sns;",
    # Step Functions
    "aws_sfn_state_machine": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.step_functions;",
    "aws_sfn_activity": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.step_functions;",
    # EventBridge
    "aws_cloudwatch_event_rule": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.eventbridge;",
    "aws_cloudwatch_event_target": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.eventbridge;",
    "aws_cloudwatch_event_bus": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.eventbridge;",
    "aws_cloudwatch_event_bus_policy": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.eventbridge;",
    "aws_cloudwatch_event_permission": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.eventbridge;",
    "aws_cloudwatch_event_archive": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.eventbridge;",
    "aws_cloudwatch_event_connection": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.eventbridge;",
    "aws_cloudwatch_event_api_destination": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.eventbridge;",
    "aws_scheduler_schedule": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.eventbridge;",
    "aws_scheduler_schedule_group": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.eventbridge;",
    "aws_pipes_pipe": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.eventbridge;",
    # AppSync
    "aws_appsync_graphql_api": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.appsync;",
    "aws_appsync_datasource": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.appsync;",
    "aws_appsync_resolver": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.appsync;",
    "aws_appsync_function": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.appsync;",
    # MQ
    "aws_mq_broker": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.mq;",
    "aws_mq_configuration": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.mq;",
    # SES
    "aws_ses_domain_identity": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.simple_email_service;",
    "aws_ses_email_identity": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.simple_email_service;",
    "aws_ses_receipt_rule": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.simple_email_service;",
    "aws_ses_receipt_rule_set": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.simple_email_service;",
    "aws_ses_configuration_set": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.simple_email_service;",
    "aws_ses_template": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.simple_email_service;",
    "aws_sesv2_email_identity": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.simple_email_service;",
    "aws_sesv2_configuration_set": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.simple_email_service;",
    # =========================================================================
    # Management & Governance (#E7157B)
    # =========================================================================
    # CloudWatch
    "aws_cloudwatch_log_group": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloudwatch;",
    "aws_cloudwatch_log_stream": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloudwatch;",
    "aws_cloudwatch_log_metric_filter": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloudwatch;",
    "aws_cloudwatch_log_subscription_filter": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloudwatch;",
    "aws_cloudwatch_log_destination": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloudwatch;",
    "aws_cloudwatch_log_resource_policy": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloudwatch;",
    "aws_cloudwatch_metric_alarm": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.cloudwatch_alarm;",
    "aws_cloudwatch_composite_alarm": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.cloudwatch_alarm;",
    "aws_cloudwatch_dashboard": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloudwatch;",
    "aws_cloudwatch_metric_stream": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloudwatch;",
    "aws_cloudwatch_query_definition": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloudwatch;",
    # CloudTrail
    "aws_cloudtrail": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloudtrail;",
    "aws_cloudtrail_event_data_store": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloudtrail;",
    # CloudFormation
    "aws_cloudformation_stack": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloudformation;",
    "aws_cloudformation_stack_set": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloudformation;",
    "aws_cloudformation_stack_set_instance": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloudformation;",
    # SSM
    "aws_ssm_parameter": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.parameter_store;",
    "aws_ssm_document": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.systems_manager;",
    "aws_ssm_association": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.systems_manager;",
    "aws_ssm_maintenance_window": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.systems_manager;",
    "aws_ssm_maintenance_window_target": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.systems_manager;",
    "aws_ssm_maintenance_window_task": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.systems_manager;",
    "aws_ssm_patch_baseline": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.systems_manager;",
    "aws_ssm_patch_group": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.systems_manager;",
    "aws_ssm_resource_data_sync": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.systems_manager;",
    "aws_ssm_activation": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.systems_manager;",
    # Config
    "aws_config_config_rule": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.config;",
    "aws_config_configuration_recorder": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.config;",
    "aws_config_delivery_channel": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.config;",
    "aws_config_configuration_aggregator": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.config;",
    "aws_config_conformance_pack": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.config;",
    "aws_config_remediation_configuration": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.config;",
    # Organizations
    "aws_organizations_organization": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.organizations;",
    "aws_organizations_account": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.organizations;",
    "aws_organizations_organizational_unit": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.organizations;",
    "aws_organizations_policy": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.organizations;",
    "aws_organizations_policy_attachment": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.organizations;",
    # Service Catalog
    "aws_servicecatalog_portfolio": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.service_catalog;",
    "aws_servicecatalog_product": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.service_catalog;",
    # Trusted Advisor / Health / Budgets
    "aws_budgets_budget": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cost_explorer;",
    "aws_budgets_budget_action": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cost_explorer;",
    "aws_ce_anomaly_monitor": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cost_explorer;",
    "aws_ce_anomaly_subscription": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cost_explorer;",
    "aws_ce_cost_category": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cost_explorer;",
    # Resource Groups
    "aws_resourcegroups_group": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.systems_manager;",
    # License Manager
    "aws_licensemanager_license_configuration": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.license_manager;",
    # Control Tower
    "aws_controltower_control": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.control_tower;",
    # =========================================================================
    # Analytics (#8C4FFF)
    # =========================================================================
    # Kinesis
    "aws_kinesis_stream": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.kinesis;",
    "aws_kinesis_stream_consumer": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.kinesis;",
    "aws_kinesis_firehose_delivery_stream": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.kinesis_data_firehose;",
    "aws_kinesis_analytics_application": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.kinesis_data_analytics;",
    "aws_kinesisanalyticsv2_application": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.kinesis_data_analytics;",
    "aws_kinesis_video_stream": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.kinesis_video_streams;",
    # Athena
    "aws_athena_database": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.athena;",
    "aws_athena_workgroup": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.athena;",
    "aws_athena_named_query": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.athena;",
    "aws_athena_data_catalog": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.athena;",
    # Glue
    "aws_glue_job": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.glue;",
    "aws_glue_catalog_database": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.glue;",
    "aws_glue_catalog_table": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.glue;",
    "aws_glue_connection": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.glue;",
    "aws_glue_crawler": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.glue;",
    "aws_glue_security_configuration": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.glue;",
    "aws_glue_trigger": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.glue;",
    "aws_glue_workflow": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.glue;",
    "aws_glue_classifier": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.glue;",
    "aws_glue_dev_endpoint": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.glue;",
    "aws_glue_ml_transform": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.glue;",
    "aws_glue_partition": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.glue;",
    "aws_glue_registry": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.glue;",
    "aws_glue_schema": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.glue;",
    "aws_glue_data_catalog_encryption_settings": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.glue;",
    # OpenSearch / Elasticsearch
    "aws_elasticsearch_domain": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elasticsearch_service;",
    "aws_elasticsearch_domain_policy": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elasticsearch_service;",
    "aws_opensearch_domain": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elasticsearch_service;",
    "aws_opensearch_domain_policy": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elasticsearch_service;",
    "aws_opensearchserverless_collection": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elasticsearch_service;",
    # MSK
    "aws_msk_cluster": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.managed_streaming_for_kafka;",
    "aws_msk_configuration": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.managed_streaming_for_kafka;",
    "aws_msk_serverless_cluster": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.managed_streaming_for_kafka;",
    "aws_mskconnect_connector": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.managed_streaming_for_kafka;",
    # EMR
    "aws_emr_cluster": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.emr;",
    "aws_emr_instance_group": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.emr;",
    "aws_emr_security_configuration": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.emr;",
    "aws_emrserverless_application": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.emr;",
    # Lake Formation
    "aws_lakeformation_resource": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lake_formation;",
    "aws_lakeformation_permissions": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lake_formation;",
    "aws_lakeformation_data_lake_settings": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lake_formation;",
    # QuickSight
    "aws_quicksight_data_source": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.quicksight;",
    "aws_quicksight_group": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.quicksight;",
    "aws_quicksight_user": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.quicksight;",
    # Data Pipeline
    "aws_datapipeline_pipeline": f"{_RESOURCE_ICON_BASE}fillColor=#8C4FFF;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.data_pipeline;",
    # =========================================================================
    # Machine Learning (#1A9C3E)
    # =========================================================================
    # SageMaker
    "aws_sagemaker_endpoint": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sagemaker;",
    "aws_sagemaker_endpoint_configuration": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sagemaker;",
    "aws_sagemaker_model": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sagemaker;",
    "aws_sagemaker_notebook_instance": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.sagemaker_notebook;",
    "aws_sagemaker_domain": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sagemaker;",
    "aws_sagemaker_user_profile": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sagemaker;",
    "aws_sagemaker_app": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sagemaker;",
    "aws_sagemaker_feature_group": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sagemaker;",
    "aws_sagemaker_image": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sagemaker;",
    "aws_sagemaker_model_package_group": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sagemaker;",
    "aws_sagemaker_pipeline": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sagemaker;",
    "aws_sagemaker_project": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sagemaker;",
    "aws_sagemaker_studio_lifecycle_config": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sagemaker;",
    "aws_sagemaker_workforce": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sagemaker;",
    "aws_sagemaker_workteam": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sagemaker;",
    # Bedrock
    "aws_bedrock_custom_model": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sagemaker;",
    "aws_bedrock_model_invocation_logging_configuration": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sagemaker;",
    "aws_bedrockagent_agent": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sagemaker;",
    "aws_bedrockagent_knowledge_base": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sagemaker;",
    # Comprehend
    "aws_comprehend_entity_recognizer": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.comprehend;",
    "aws_comprehend_document_classifier": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.comprehend;",
    # Rekognition
    "aws_rekognition_collection": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.rekognition;",
    "aws_rekognition_project": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.rekognition;",
    # Lex
    "aws_lex_bot": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lex;",
    "aws_lex_intent": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lex;",
    "aws_lex_slot_type": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lex;",
    "aws_lexv2models_bot": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lex;",
    # Polly / Transcribe / Translate / Textract / Forecast / Personalize / Kendra
    "aws_polly_voice": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.polly;",
    "aws_transcribe_language_model": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.transcribe;",
    "aws_transcribe_vocabulary": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.transcribe;",
    "aws_kendra_index": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.kendra;",
    "aws_kendra_data_source": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.kendra;",
    "aws_forecast_dataset": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.forecast;",
    "aws_personalize_schema": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.personalize;",
    "aws_personalize_dataset_group": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.personalize;",
    # =========================================================================
    # Migration & Transfer (#ED7100)
    # =========================================================================
    # DataSync
    "aws_datasync_agent": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.datasync;",
    "aws_datasync_task": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.datasync;",
    "aws_datasync_location_s3": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.datasync;",
    "aws_datasync_location_smb": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.datasync;",
    "aws_datasync_location_efs": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.datasync;",
    "aws_datasync_location_nfs": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.datasync;",
    "aws_datasync_location_fsx_lustre_file_system": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.datasync;",
    "aws_datasync_location_fsx_windows_file_system": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.datasync;",
    "aws_datasync_location_hdfs": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.datasync;",
    # Transfer Family
    "aws_transfer_server": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.transfer_family;",
    "aws_transfer_user": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.transfer_family;",
    "aws_transfer_ssh_key": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.transfer_family;",
    "aws_transfer_workflow": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.transfer_family;",
    # DMS
    "aws_dms_replication_instance": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.database_migration_service;",
    "aws_dms_replication_task": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.database_migration_service;",
    "aws_dms_endpoint": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.database_migration_service;",
    "aws_dms_replication_subnet_group": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.database_migration_service;",
    "aws_dms_certificate": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.database_migration_service;",
    "aws_dms_event_subscription": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.database_migration_service;",
    # Migration Hub
    "aws_migrationhub_home_region": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.migration_hub;",
    # Application Migration Service
    "aws_mgn_replication_configuration_template": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.migration_hub;",
    # =========================================================================
    # Developer Tools (#5A6C86)
    # =========================================================================
    # CodeBuild
    "aws_codebuild_project": f"{_RESOURCE_ICON_BASE}fillColor=#5A6C86;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.codebuild;",
    "aws_codebuild_source_credential": f"{_RESOURCE_ICON_BASE}fillColor=#5A6C86;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.codebuild;",
    "aws_codebuild_report_group": f"{_RESOURCE_ICON_BASE}fillColor=#5A6C86;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.codebuild;",
    "aws_codebuild_webhook": f"{_RESOURCE_ICON_BASE}fillColor=#5A6C86;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.codebuild;",
    # CodePipeline
    "aws_codepipeline": f"{_RESOURCE_ICON_BASE}fillColor=#5A6C86;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.codepipeline;",
    "aws_codepipeline_webhook": f"{_RESOURCE_ICON_BASE}fillColor=#5A6C86;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.codepipeline;",
    # CodeDeploy
    "aws_codedeploy_app": f"{_RESOURCE_ICON_BASE}fillColor=#5A6C86;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.codedeploy;",
    "aws_codedeploy_deployment_group": f"{_RESOURCE_ICON_BASE}fillColor=#5A6C86;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.codedeploy;",
    "aws_codedeploy_deployment_config": f"{_RESOURCE_ICON_BASE}fillColor=#5A6C86;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.codedeploy;",
    # CodeCommit
    "aws_codecommit_repository": f"{_RESOURCE_ICON_BASE}fillColor=#5A6C86;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.codecommit;",
    "aws_codecommit_trigger": f"{_RESOURCE_ICON_BASE}fillColor=#5A6C86;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.codecommit;",
    "aws_codecommit_approval_rule_template": f"{_RESOURCE_ICON_BASE}fillColor=#5A6C86;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.codecommit;",
    # CodeArtifact
    "aws_codeartifact_domain": f"{_RESOURCE_ICON_BASE}fillColor=#5A6C86;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.codeartifact;",
    "aws_codeartifact_repository": f"{_RESOURCE_ICON_BASE}fillColor=#5A6C86;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.codeartifact;",
    # CodeStar
    "aws_codestarconnections_connection": f"{_RESOURCE_ICON_BASE}fillColor=#5A6C86;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.codestar;",
    "aws_codestarnotifications_notification_rule": f"{_RESOURCE_ICON_BASE}fillColor=#5A6C86;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.codestar;",
    # X-Ray
    "aws_xray_sampling_rule": f"{_RESOURCE_ICON_BASE}fillColor=#5A6C86;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.x_ray;",
    "aws_xray_group": f"{_RESOURCE_ICON_BASE}fillColor=#5A6C86;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.x_ray;",
    "aws_xray_encryption_config": f"{_RESOURCE_ICON_BASE}fillColor=#5A6C86;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.x_ray;",
    # Cloud9
    "aws_cloud9_environment_ec2": f"{_RESOURCE_ICON_BASE}fillColor=#5A6C86;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloud9;",
    # CodeGuru
    "aws_codegurureviewer_repository_association": f"{_RESOURCE_ICON_BASE}fillColor=#5A6C86;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.codeguru;",
    "aws_codeguruprofiler_profiling_group": f"{_RESOURCE_ICON_BASE}fillColor=#5A6C86;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.codeguru;",
    # =========================================================================
    # IoT (#1A9C3E)
    # =========================================================================
    "aws_iot_thing": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.iot_core;",
    "aws_iot_thing_type": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.iot_core;",
    "aws_iot_thing_group": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.iot_core;",
    "aws_iot_policy": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.iot_core;",
    "aws_iot_policy_attachment": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.iot_core;",
    "aws_iot_certificate": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.iot_core;",
    "aws_iot_topic_rule": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.iot_core;",
    "aws_iot_role_alias": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.iot_core;",
    "aws_iot_authorizer": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.iot_core;",
    "aws_iot_thing_principal_attachment": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.iot_core;",
    "aws_iot_analytics_channel": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.iot_analytics;",
    "aws_iot_analytics_dataset": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.iot_analytics;",
    "aws_iot_analytics_datastore": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.iot_analytics;",
    "aws_iot_analytics_pipeline": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.iot_analytics;",
    "aws_iot_event_detector_model": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.iot_events;",
    "aws_iot_event_input": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.iot_events;",
    "aws_greengrass_group": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.iot_greengrass;",
    "aws_greengrass_core_definition": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.iot_greengrass;",
    "aws_greengrass_function_definition": f"{_RESOURCE_ICON_BASE}fillColor=#1A9C3E;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.iot_greengrass;",
    # =========================================================================
    # Media Services (#E7157B)
    # =========================================================================
    "aws_media_convert_queue": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elemental_mediaconvert;",
    "aws_media_live_channel": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elemental_medialive;",
    "aws_media_live_input": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elemental_medialive;",
    "aws_media_store_container": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elemental_mediastore;",
    "aws_media_package_channel": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elemental_mediapackage;",
    "aws_media_connect_flow": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elemental_mediaconnect;",
    "aws_media_tailor_configuration": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elemental_mediatailor;",
    "aws_ivs_channel": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elemental_medialive;",
    # =========================================================================
    # End User Computing (#ED7100)
    # =========================================================================
    "aws_workspaces_workspace": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.workspaces;",
    "aws_workspaces_directory": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.workspaces;",
    "aws_workspaces_ip_group": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.workspaces;",
    "aws_appstream_fleet": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.appstream_20;",
    "aws_appstream_stack": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.appstream_20;",
    # =========================================================================
    # Customer Engagement (#E7157B)
    # =========================================================================
    "aws_connect_instance": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.connect;",
    "aws_connect_contact_flow": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.connect;",
    "aws_connect_queue": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.connect;",
    "aws_pinpoint_app": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.pinpoint;",
    "aws_pinpoint_email_channel": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.pinpoint;",
    "aws_pinpoint_sms_channel": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.pinpoint;",
    # =========================================================================
    # Application Auto Scaling (#ED7100)
    # =========================================================================
    "aws_appautoscaling_target": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.auto_scaling2;",
    "aws_appautoscaling_policy": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.auto_scaling2;",
    "aws_appautoscaling_scheduled_action": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.auto_scaling2;",
    # =========================================================================
    # Amplify / AppConfig / Mobile (#ED7100)
    # =========================================================================
    "aws_amplify_app": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.amplify;",
    "aws_amplify_branch": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.amplify;",
    "aws_amplify_domain_association": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.amplify;",
    "aws_amplify_backend_environment": f"{_RESOURCE_ICON_BASE}fillColor=#ED7100;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.amplify;",
    "aws_appconfig_application": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.systems_manager;",
    "aws_appconfig_configuration_profile": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.systems_manager;",
    "aws_appconfig_environment": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.systems_manager;",
    "aws_appconfig_deployment_strategy": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.systems_manager;",
    "aws_appconfig_deployment": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.systems_manager;",
    # =========================================================================
    # Serverless Application Model / CloudMap (#E7157B)
    # =========================================================================
    "aws_service_discovery_service": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloud_map;",
    "aws_service_discovery_private_dns_namespace": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloud_map;",
    "aws_service_discovery_public_dns_namespace": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloud_map;",
    "aws_service_discovery_http_namespace": f"{_RESOURCE_ICON_BASE}fillColor=#E7157B;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloud_map;",
    # =========================================================================
    # General / Edge
    # =========================================================================
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
