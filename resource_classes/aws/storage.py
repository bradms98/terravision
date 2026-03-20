from . import _AWS


class _Storage(_AWS):
    _type = "storage"
    _icon_dir = "resource_images/aws/storage"


class Backup(_Storage):
    _icon = "backup.png"


class CloudendureDisasterRecovery(_Storage):
    _icon = "cloudendure-disaster-recovery.png"


class EFSInfrequentaccessPrimaryBg(_Storage):
    _icon = "efs-infrequentaccess-primary-bg.png"


class EFSStandardPrimaryBg(_Storage):
    _icon = "efs-standard-primary-bg.png"


class ElasticBlockStoreEBS(_Storage):
    _icon = "elastic-block-store-ebs.png"


class ElasticFileSystemEFS(_Storage):
    _icon = "elastic-file-system-efs.png"


class FsxForLustre(_Storage):
    _icon = "fsx-for-lustre.png"


class FsxForWindowsFileServer(_Storage):
    _icon = "fsx-for-windows-file-server.png"


class Fsx(_Storage):
    _icon = "fsx.png"


class S3Glacier(_Storage):
    _icon = "s3-glacier.png"


class SimpleStorageServiceS3(_Storage):
    _icon = "simple-storage-service-s3.png"


class SnowballEdge(_Storage):
    _icon = "snowball-edge.png"


class Snowball(_Storage):
    _icon = "snowball.png"


class Snowmobile(_Storage):
    _icon = "snowmobile.png"


class StorageGateway(_Storage):
    _icon = "storage-gateway.png"


class Storage(_Storage):
    _icon = "storage.png"


class S3Object(_Storage):
    _icon = "simple-storage-service-s3-object.png"


# Aliases

CDR = CloudendureDisasterRecovery
EBS = ElasticBlockStoreEBS
EFS = ElasticFileSystemEFS
FSx = Fsx
S3 = SimpleStorageServiceS3

# Terraform aliases
aws_backup_plan = Backup
aws_backup_vault = Backup
aws_backup_selection = Backup
aws_ebs_snapshot = ElasticBlockStoreEBS
aws_ebs_volume = ElasticBlockStoreEBS
aws_efs_access_point = ElasticFileSystemEFS
aws_efs_file_system = ElasticFileSystemEFS
aws_efs = ElasticFileSystemEFS
aws_fsx_lustre_file_system = FsxForLustre
aws_fsx_ontap_file_system = Fsx
aws_fsx_openzfs_file_system = Fsx
aws_fsx_windows_file_system = FsxForWindowsFileServer
aws_glacier_vault = S3Glacier
# aws_s3_bucket is defined in groups.py as S3BucketGroup (container/cluster)
aws_s3_bucket_object = SimpleStorageServiceS3
aws_s3_object = S3Object
aws_storagegateway_gateway = StorageGateway
aws_storagegateway_smb_file_share = StorageGateway
aws_storagegateway_nfs_file_share = StorageGateway

# S3 bucket ancillary resources (rendered inside S3 bucket container)
aws_s3_bucket_policy = SimpleStorageServiceS3
aws_s3_bucket_server_side_encryption_configuration = SimpleStorageServiceS3
aws_s3_bucket_public_access_block = SimpleStorageServiceS3
aws_s3_bucket_lifecycle_configuration = SimpleStorageServiceS3
aws_s3_bucket_versioning = SimpleStorageServiceS3
aws_s3_bucket_ownership_controls = SimpleStorageServiceS3
aws_s3_bucket_intelligent_tiering_configuration = SimpleStorageServiceS3
aws_s3_bucket_acl = SimpleStorageServiceS3
aws_s3_bucket_cors_configuration = SimpleStorageServiceS3
aws_s3_bucket_logging = SimpleStorageServiceS3
aws_s3_bucket_notification = SimpleStorageServiceS3
aws_s3_bucket_object_lock_configuration = SimpleStorageServiceS3
aws_s3_bucket_replication_configuration = SimpleStorageServiceS3
aws_s3_bucket_website_configuration = SimpleStorageServiceS3
