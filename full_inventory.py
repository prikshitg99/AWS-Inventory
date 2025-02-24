import boto3
import pandas as pd

# Define AWS Regions
REGIONS = ["us-east-1", "ap-south-1"]

# Initialize AWS session
session = boto3.session.Session()
ALL_SERVICES = session.get_available_services()

# Function to initialize clients for a specific region
def get_client(service, region):
    try:
        return boto3.client(service, region_name=region)
    except Exception as e:
        print(f"Error initializing client for {service} in {region}: {e}")
        return None

# Function to convert datetime columns to timezone-naive
def make_datetime_naive(df):
    for col in df.select_dtypes(include=['datetime64[ns, UTC]']).columns:
        df[col] = df[col].dt.tz_localize(None)
    return df

# Function to fetch resource details dynamically
def get_service_inventory(service, region):
    client = get_client(service, region)
    if not client:
        return None

    try:
        methods = [method for method in dir(client) if method.startswith("describe_") or method.startswith("list_")]
        for method in methods:
            try:
                response = getattr(client, method)()
                key = next((k for k in response.keys() if isinstance(response[k], list)), None)
                if key:
                    data = response[key]
                    if data:
                        df = pd.DataFrame(data)
                        return make_datetime_naive(df)
            except Exception as e:
                pass  # Ignore errors from API calls
    except Exception as e:
        print(f"Error fetching data for {service}: {e}")
    return None

# Save all data to an Excel file
with pd.ExcelWriter("aws_full_inventory.xlsx") as writer:
    for region in REGIONS:
        print(f"Fetching AWS inventory for {region}...")
        
        for service in ALL_SERVICES:
            print(f"Processing {service}...")
            df = get_service_inventory(service, region)
            if df is not None and not df.empty:
                sheet_name = f"{service[:30]} ({region})"  # Excel sheet names must be <= 31 chars
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f" {service} saved.")

print("\n AWS Full Inventory saved to aws_full_inventory.xlsx")
