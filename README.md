

# Install

1. Git clone the repo
2. Install [poetry](https://python-poetry.org/docs/master/)
3. `poetry install`

Now, you can scrape all the endpoints in one go by running `poetry run scrape_all`. Or, you can use the Unifi object and fetch + upload individual collection items with the available methods.

NOTE: a "collection" is a single endpoint on the unifi-api-browser, aka a "dashboard" you can view on your Unifi controller.

# Usage

## CLI

First, set the following environment variables:
```
UNIFI_API_BASE_URL=www.yourunifi-api-broswer.com
UNIFI_API_USERNAME=username
UNIFI_API_PASSWORD=password
BOTO3_ENDPOINT_URL='https://us-east-1.my-aws-s3-lookalike.com
BOTO3_ACCESS_KEY=ACCESSKEY
BOTO3_SECRET_KEY=SECRETKEY
BOTO3_BUCKET=my-bucket-name
```

Then, as long as you've installed properly, (`poetry install`), you should be able to do `poetry run scrape_all` and it'll just scrape all your endpoints and save the results to object storage.

## Python API
I use 'stat_sites' and 'stat_hourly_site' as examples of collections you can scrape here.

```
from unifipy import Unifi
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

# Get all available collections
all_available_collections = u.PAYLOADS.keys()

# Take a list of collections, scrape and upload them all to your object storage
u.scrape_set_of_collections(['stat_sites', 'stat_hourly_site' ...])

# Scrape & upload a single collection
u.fetch_and_upload_collection('stat_sites')

# Scrape a single collection without uploading it
u.fetch_collection('stat_sites')
...
```

# Setting up for development


## Install

1. Install poetry if you don't have it already
2. Git clone this repo
3. Run `poetry install --with dev`

## To run tests

`poetry run pytest`


## To lint

Go to the base unifipy directory and run `poetry run black .`
