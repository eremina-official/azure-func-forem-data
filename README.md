# Azure Function App in Forem Data Pipeline

Azure Function that fetches the latest DEV (Forem) articles via `https://dev.to/api/articles/latest` and stores each batch in an Azure Blob Storage container. The function keeps track of the newest processed timestamp in `latest_timestamp.json` so repeat executions only ingest fresh content.

## Configuration
- `BLOB_CONN_STR`: Azure Storage connection string used by the function runtime.
- `BACKFILL_MODE` (optional): when set to `true`, writes a rolling backfill blob instead of the incremental timestamp-based workflow.
- Update `local.settings.json` locally or the Function App configuration in Azure with the values above.

## Running Locally
1. Install dependencies: `pip install -r requirements.txt`.
2. Start the Azure Functions host: `func start`.

### Deploy to Azure
- Prerequisites: Azure CLI and Azure Functions Core Tools installed, and an Azure subscription.
- Quick deploy using the Core Tools:
  ```bash
  az login
  func azure functionapp publish <FUNCTION_APP_NAME>
  ```

***Engineering Notes:***

- Consumption plan has a time limit of 10 minutes per execution, from practical experience `dev.to` has a rate limit, so **fetching data in smaller batches with retries** was implemented to ensure that the function completes within this window.
- Adjusted the backfill logic to fetch data from REST API in smaller batches instead of trying to backfill all at once, which can lead to timeouts.
- Monitored execution and storage costs, especially if backfilling large volumes of data.
- Used Azure command line to deploy app and set environment variables: set env variables via Azure CLI or VS Code Azure Functions extension before deployment (Azure Functions: Upload Local Settings)
