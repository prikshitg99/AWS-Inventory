AWS Multi-Region Inventory Script 🌍🚀

📊 Automated AWS Inventory Management using Python & Boto3

✅ Find & Export AWS Resources (EC2, S3, Lambda, IAM, ECR, VPC, DynamoDB, etc.) across multiple AWS regions

✅ Generate Excel reports for cloud asset tracking & cost optimization

✅ Simplify AWS infrastructure audits with real-time resource discovery


🚀 Why Use This Script?

🔹 Effortless AWS Asset Tracking - Automatically list all AWS services across multiple regions

🔹 Cost Optimization & Compliance - Identify unused AWS resources to reduce costs

🔹 Multi-Region Support - Scan EC2, S3, Lambda, ECR, VPC, IAM, DynamoDB and more!

🔹 Automated Reports - Export AWS inventory in a clean Excel (XLSX) format

Perfect for AWS Administrators, DevOps Engineers, Cloud Architects & Security Teams


🛠 Prerequisites

Before running this script, ensure you have:

✅ Python 3.x installed

✅ AWS CLI configured (aws configure)

✅ Boto3 & Pandas installed (pip install boto3 pandas)


🔧 Installation & Setup

1️⃣ Clone the Repository:

git clone https://github.com/your-username/aws-inventory.git

cd aws-inventory


2️⃣ Install Dependencies:

pip install -r requirements.txt


3️⃣ Configure AWS Credentials:

aws configure

(Enter AWS Access Key, Secret Key, and Default Region)



🎯 How to Use

Run the script to fetch AWS inventory:

python aws_inventory.py

📂 Output: aws_inventory.xlsx (Auto-generated Excel report)

📜 Supported AWS Services

This script collects inventory for:

🖥️ Compute: EC2, Lambda

📦 Storage: S3, ECR

🔍 Databases: DynamoDB

🌐 Networking: VPC, Subnets, Internet Gateways, NAT, Route Tables

🔐 Security: IAM Roles, Security Groups

🛠️ DevOps Tools: CodeCommit, CodeBuild

📊 Monitoring & Compliance: AWS Config, CloudTrail

🌍 Multi-Region Support

Modify REGIONS list in the script to scan specific AWS regions:

REGIONS = ["us-east-1", "us-west-1", "eu-central-1"]

🚀 Use Cases

✅ Cloud Asset Management

✅ AWS Cost Optimization

✅ Security & Compliance Audits

✅ Automated AWS Infrastructure Documentation


🎯 Keywords for SEO (GitHub Search Optimization)

🔹 AWS Inventory Script

🔹 AWS Multi-Region Asset Discovery

🔹 AWS Python Boto3 Automation

🔹 AWS Cost Optimization Tools

🔹 AWS Infrastructure Audit Script

🔹 DevOps Cloud Asset Management

🔹 EC2, S3, IAM, Lambda, VPC Inventory


📜 License

This project is open-source and licensed under the MIT License.


👨‍💻 Contributing

💡 Have ideas to improve the script? Fork the repo & submit a pull request!
