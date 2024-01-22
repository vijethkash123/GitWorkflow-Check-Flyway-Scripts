import base64
import json
import os
from sys import argv
import requests


READ_TOKEN = os.environ["READ_TOKEN"]



versions_main = set()
versions_local = set()
ENVs = ['common', 'ci', 'prod', 'qa']

owner = 'vijethkash123'
repo = 'GitWorkflowTest'

print(argv)
if len(argv) < 2:
    print("PR Number not sent to call")
    exit(0)
PR_NUMBER = argv[1]
READ_TOKEN = os.environ["READ_TOKEN"]
headers={"accept": "application/vnd.github+json", "Authorization": f"token {READ_TOKEN}"}

workflow_runs = f"https://api.github.com/repos/vijethkash123/GitWorkflowTest/actions/runs?event_id={PR_NUMBER}"
response = requests.get(workflow_runs, headers=headers)
if response.status_code != 200:
    print(f"Error: Unable to fetch changed files. Status code: {response.status_code}")
    exit(1)
else:
    run_data = response.json()
    latest_run_id = run_data["workflow_runs"][0]["run_number"]
    print(f"Latest run ID: {latest_run_id}")

print("Submitting rerun POST request")
rerun_url = f"https://api.github.com/repos/vijethkash123/GitWorkflowTest/actions/runs/{latest_run_id}/rerun"
response = requests.post(rerun_url, headers)
print(response.status_code)
