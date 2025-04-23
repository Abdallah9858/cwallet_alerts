import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.resource import SubscriptionClient

# Set Azure credentials using environment variables (Replace with your actual values or add to your system environment)
os.environ["AZURE_CLIENT_ID"] = "your-client-id"
os.environ["AZURE_CLIENT_SECRET"] = "your-client-secret"
os.environ["AZURE_TENANT_ID"] = "561f6207-9da0-40bf-8012-39dfd3ff9a8d"
os.environ["AZURE_SUBSCRIPTION_ID"] = "511a9969-f2e0-43f7-8745-23c67b3ac6ac"

# Authenticate using the environment variables
credential = DefaultAzureCredential()

# Get the subscription ID from the environment or set manually
subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")

# Initialize the Azure Monitor client
monitor_client = MonitorManagementClient(credential, subscription_id)

# Example function: Get the list of metric definitions for a resource
def list_metrics(resource_id):
    try:
        print(f"Fetching metrics for resource: {resource_id}")
        metrics = monitor_client.metrics.list(
            resource_id,
            timespan='2025-04-20T00:00:00Z/2025-04-20T23:59:59Z',  # Example timespan
            interval='PT1H',  # 1 hour intervals
            metricnames='Percentage CPU',  # Example metric name
            aggregation='Average'
        )
        for metric in metrics:
            print(metric.name.localized_value)
            for time_series in metric.timeseries:
                for data in time_series.data:
                    print(f"Timestamp: {data.timestamp}, Average: {data.average}")
    except Exception as e:
        print(f"Error fetching metrics: {str(e)}")

# Example resource ID (replace with actual resource ID you want to monitor)
resource_id = "/subscriptions/your-subscription-id/resourceGroups/your-resource-group/providers/Microsoft.Compute/virtualMachines/your-vm-name"

# Call the function to fetch and print metrics
list_metrics(resource_id)
