import boto3
import pandas as pd

# Define AWS Regions
REGIONS = ["us-east-1", "ap-south-1"]

# Function to initialize clients for a specific region
def get_client(service, region):
    return boto3.client(service, region_name=region)

# Function to get EC2 inventory
def get_ec2_inventory(region):
    ec2_client = get_client("ec2", region)
    instances = ec2_client.describe_instances()
    data = []
    for reservation in instances["Reservations"]:
        for instance in reservation["Instances"]:
            data.append([
                instance.get("Tags", [{}])[0].get("Value", "N/A"),
                instance["InstanceId"],
                instance["InstanceType"],
                instance["Placement"]["AvailabilityZone"],
                ", ".join([sg["GroupName"] for sg in instance.get("SecurityGroups", [])]),
                instance.get("VpcId", "N/A"),
                "N/A"
            ])
    return pd.DataFrame(data, columns=["Instance Name", "Instance ID", "Instance Type", "Availability Zone", "Security group name", "VPC (Private)", "VPC Name"])

# Function to get S3 inventory
def get_s3_inventory(region):
    s3_client = get_client("s3", region)
    buckets = s3_client.list_buckets()["Buckets"]
    data = [[bucket["Name"], region] for bucket in buckets]
    return pd.DataFrame(data, columns=["Bucket Name", "AWS Region"])

# Function to get Lambda inventory
def get_lambda_inventory(region):
    lambda_client = get_client("lambda", region)
    functions = lambda_client.list_functions()["Functions"]
    data = [[func["FunctionName"], region, func.get("State", "N/A"), "N/A"] for func in functions]
    return pd.DataFrame(data, columns=["Function name", "Region", "TRIGGER", "TRIGGER NAME"])

# Function to get ECR inventory
def get_ecr_inventory(region):
    ecr_client = get_client("ecr", region)
    repositories = ecr_client.describe_repositories()["repositories"]
    data = [[repo["repositoryName"], region, repo["repositoryUri"].split(".")[0]] for repo in repositories]
    return pd.DataFrame(data, columns=["Repositories", "AWS Region", "Public/Private"])

# Function to get DynamoDB inventory
def get_dynamodb_inventory(region):
    dynamodb_client = get_client("dynamodb", region)
    tables = dynamodb_client.list_tables()["TableNames"]
    data = [[table, region] for table in tables]
    return pd.DataFrame(data, columns=["Table Name", "AWS Region"])

# Function to get CodeCommit inventory
def get_codecommit_inventory(region):
    codecommit_client = get_client("codecommit", region)
    repos = codecommit_client.list_repositories()["repositories"]
    data = [[repo["repositoryName"], region] for repo in repos]
    return pd.DataFrame(data, columns=["Repository Name", "Region"])

# Function to get CodeBuild inventory
def get_codebuild_inventory(region):
    codebuild_client = get_client("codebuild", region)
    projects = codebuild_client.list_projects()["projects"]
    data = []
    for project_name in projects:
        project = codebuild_client.batch_get_projects(names=[project_name])["projects"][0]
        data.append([project["name"], project["source"]["type"], region])
    return pd.DataFrame(data, columns=["Name", "Source provider", "Region"])

# Function to get IAM roles inventory
def get_iam_roles(region):
    iam_client = get_client("iam", region)
    roles = iam_client.list_roles()["Roles"]
    data = [[role["RoleName"], role["Arn"]] for role in roles]
    return pd.DataFrame(data, columns=["IAM Role Name", "ARN"])

# Function to get CloudTrail inventory
def get_cloudtrail(region):
    cloudtrail_client = get_client("cloudtrail", region)
    trails = cloudtrail_client.describe_trails()["trailList"]
    data = [[trail["Name"], trail["HomeRegion"], trail["S3BucketName"]] for trail in trails]
    return pd.DataFrame(data, columns=["Trail Name", "Home Region", "S3 Bucket"])

# Function to get AWS Config inventory
def get_aws_config(region):
    config_client = get_client("config", region)
    config_recorders = config_client.describe_configuration_recorders()["ConfigurationRecorders"]
    data = [[recorder["name"], region] for recorder in config_recorders]
    return pd.DataFrame(data, columns=["Config Recorder Name", "Region"])

# Function to get VPC and related inventories
def get_vpc_network_inventory(region):
    ec2_client = get_client("ec2", region)
    
    # Fetch details
    vpcs = ec2_client.describe_vpcs()["Vpcs"]
    subnets = ec2_client.describe_subnets()["Subnets"]
    igws = ec2_client.describe_internet_gateways()["InternetGateways"]
    nat_gateways = ec2_client.describe_nat_gateways()["NatGateways"]
    route_tables = ec2_client.describe_route_tables()["RouteTables"]
    vpc_peerings = ec2_client.describe_vpc_peering_connections()["VpcPeeringConnections"]

    # Collect data
    data = []

    for vpc in vpcs:
        data.append([region, "VPC", vpc["VpcId"], vpc.get("CidrBlock", "N/A"), vpc.get("IsDefault", "N/A"), "-", "-"])

    for subnet in subnets:
        data.append([region, "Subnet", subnet["VpcId"], subnet["SubnetId"], subnet.get("CidrBlock", "N/A"), subnet.get("AvailabilityZone", "N/A"), "-"])

    for igw in igws:
        vpc_id = igw["Attachments"][0].get("VpcId", "N/A") if igw.get("Attachments") else "N/A"
        data.append([region, "Internet Gateway", "-", igw["InternetGatewayId"], "-", "-", vpc_id])

    for nat in nat_gateways:
        data.append([region, "NAT Gateway", "-", nat["NatGatewayId"], nat["VpcId"], nat["SubnetId"], nat.get("State", "N/A")])

    for rt in route_tables:
        data.append([region, "Route Table", "-", rt["RouteTableId"], "-", "-", rt["VpcId"]])

    for peering in vpc_peerings:
        data.append([region, "VPC Peering", "-", peering["VpcPeeringConnectionId"], peering["RequesterVpcInfo"]["VpcId"], peering["AccepterVpcInfo"]["VpcId"], peering.get("Status", {}).get("Code", "N/A")])

    return pd.DataFrame(data, columns=["Region", "Resource Type", "VPC ID", "Resource ID", "CIDR/State", "Subnet/Accepter VPC", "Attached VPC/Requester VPC"])

#  Save all data to an Excel file
with pd.ExcelWriter("aws_inventory.xlsx") as writer:
    for region in REGIONS:
        print(f"Fetching AWS inventory for {region}...")

        # Store inventory data only if it exists
        services = {
            f"EC2 ({region})": get_ec2_inventory(region),
            f"S3 ({region})": get_s3_inventory(region),
            f"Lambda ({region})": get_lambda_inventory(region),
            f"ECR ({region})": get_ecr_inventory(region),
            f"DynamoDB ({region})": get_dynamodb_inventory(region),
            f"CodeCommit ({region})": get_codecommit_inventory(region),
            f"CodeBuild ({region})": get_codebuild_inventory(region),
            f"IAM ({region})": get_iam_roles(region),
            f"CloudTrail ({region})": get_cloudtrail(region),
            f"AWS Config ({region})": get_aws_config(region),
        }

        for sheet_name, df in services.items():
            if not df.empty:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f" {sheet_name} saved.")

        # Save combined VPC & Network data
        vpc_network_df = get_vpc_network_inventory(region)
        if not vpc_network_df.empty:
            vpc_network_df.to_excel(writer, sheet_name="VPC and Subnet", index=False)
            print(f" VPC and Subnet saved.")

print("\n AWS Multi-Region Inventory saved to aws_inventory.xlsx")
