import logging
import os
import sys

from unifiapipy import Unifi

UNIFI_API_BASE_URL = os.getenv("UNIFI_API_BASE_URL")
UNIFI_API_USER = os.getenv("UNIFI_API_USERNAME")
UNIFI_API_PASSWORD = os.getenv("UNIFI_API_PASSWORD")
BOTO3_ENDPOINT_URL = os.getenv("BOTO3_ENDPOINT_URL")
BOTO3_ACCESS_KEY = os.getenv("BOTO3_ACCESS_KEY")
BOTO3_SECRET_KEY = os.getenv("BOTO3_SECRET_KEY")
BOTO3_BUCKET = os.getenv("BOTO3_BUCKET")


def do_full_scrape():
    logging.basicConfig(
        stream=sys.stdout, level=logging.INFO, format="%(asctime)s %(message)s"
    )
    u = Unifi(
        UNIFI_API_BASE_URL,
        UNIFI_API_USER,
        UNIFI_API_PASSWORD,
        BOTO3_ENDPOINT_URL,
        BOTO3_ACCESS_KEY,
        BOTO3_SECRET_KEY,
        BOTO3_BUCKET,
    )
    u.login()
    all_collections = u.PAYLOADS.keys()
    for collection in all_collections:
        logging.info("Scraping and uploading " + collection)
        u.fetch_and_upload_collection(collection)
    logging.info("Success! Check your object storage for the results.")


if __name__ == "__main__":
    do_full_scrape()
