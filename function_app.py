import logging
import os

import azure.functions as func

from fetch_articles import main as fetch_articles
from fetch_articles_backfill import main_fetch_backfill

backfill_mode = os.getenv("BACKFILL_MODE", "")

app = func.FunctionApp()


@app.route(
    route="http_trigger", auth_level=func.AuthLevel.FUNCTION, methods=["GET", "POST"]
)
def http_trigger(req):
    logging.info("HTTP trigger function received a request.")

    try:
        if backfill_mode.lower() == "true":
            logging.info("Running in backfill mode.")
            main_fetch_backfill()
        else:
            logging.info("Running in normal fetch mode.")
            fetch_articles()
    except Exception as e:
        logging.error(f"Processing failed: {e}")
        return func.HttpResponse(f"Function execution failed: {e}", status_code=500)

    logging.info("HTTP trigger function executed successfully.")

    return func.HttpResponse("Function executed successfully.", status_code=200)
