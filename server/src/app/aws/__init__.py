from app.core import settings


class AWSConfig:
    """
    Configuration class for S3 settings.

    This class handles the initialization and validation of AWS S3 configuration
    parameters required for establishing connections to S3 services.

    Attributes:
        aws_access_key (str): AWS access key ID for authentication
        aws_secret_key (str): AWS secret access key for authentication
        region (str): AWS region name (defaults to 'ap-south-1' if not specified)
        bucket_name (str): Name of the S3 bucket to interact with

    Raises:
        ValueError: If any required AWS credentials or bucket configuration is missing
    """

    def __init__(self):
        """
        Initialize S3 configuration with settings from application configuration.

        The configuration is validated to ensure all required parameters are present
        before the class can be used.
        """
        self.aws_access_key = settings.AWS_ACCESS_KEY
        self.aws_secret_key = settings.AWS_SECRET_ACCESS_KEY
        self.region = settings.AWS_REGION or "ap-south-1"  # South pacific Mumbai
        self.bucket_name = settings.AWS_BUCKET_NAME

        if not all([self.aws_access_key, self.aws_secret_key, self.bucket_name]):
            raise ValueError("Missing required AWS credentials or bucket configuration")
