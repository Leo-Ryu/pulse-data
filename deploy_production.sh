#!/usr/bin/env bash

echo "Fetching all tags"
git fetch --all --tags --prune

echo "Checking out tag $1"
git checkout tags/$1 -b $1

echo "Starting deploy of cron.yaml"
gcloud app deploy cron.yaml --project=recidiviz-123

echo "Starting deploy of queue.yaml"
gcloud app deploy queue.yaml --project=recidiviz-123

echo "Starting deploy of main app"
gcloud app deploy --project=recidiviz-123