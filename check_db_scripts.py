import base64
import json
import os
from sys import argv
# from urllib.parse import quote
import requests

# Driver program to check above comparison function
# from version_compare import check_version

READ_TOKEN = "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"
# CURRENT_BRANCH = "feature/add-DML-scripts"
# CURRENT_BRANCH = quote(CURRENT_BRANCH, safe='')

versions_main = set()
versions_local = set()
ENVs = ['common', 'ci', 'prod', 'qa']

# Run only if there are db_scrit file changes in a branch
owner = 'vijethkash123'
repo = 'GitWorkflowTest'
branch = 'feature/add-DML-scripts'
branch = quote(branch, safe='')
PR_NUMBER = 1
READ_TOKEN = "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"
headers={"accept": "application/vnd.github.v3", "Authorization": f"token {READ_TOKEN}"}

files_changed_url = f"https://api.github.com/repos/vijethkash123/GitWorkflowTest/pulls/{PR_NUMBER}/files"
response = requests.get(files_changed_url, headers=headers)
if response.status_code != 200:
    print(f"Error: Unable to fetch changed files. Status code: {response.status_code}")
    exit(1)

changed_files_data = response.json()
file_names = [file['filename'] for file in changed_files_data]
print("Changed Files:")
for file_name in file_names:
    print(file_name)

found = any('database_scripts' in file_name for file_name in file_names)

print(found)

if not found:
    print("No need to run compare, No database scripts changed")
    exit()

else:
    for file in file_names:
        if 'database_scripts' in file:
            temp = file.split('/')
            versions_local.add(temp[2][:2])

versions_local = sorted(versions_local)
# main_branch_url = fetch(
#         f"https://api.github.com/repos/vijethkash123/GitWorkflowTest/pulls/1",
#         headers={"accept": "application/vnd.github.v3, application/vnd.github.diff", "Authorization": f"token {READ_TOKEN}"},
#     )
# print(main_branch_url.content)
#
for env in ENVs:
    main_branch_url = requests.get(
        f"https://api.github.com/repos/vijethkash123/GitWorkflowTest/contents/database_scripts/{env}?ref=main",
        headers={"accept": "application/vnd.github.v3", "Authorization": f"token {READ_TOKEN}"},
    )
    if main_branch_url.status_code == 200:
        main_branch_data = json.loads(main_branch_url.content)
        for file_info in main_branch_data:
            versions_main.add(file_info['name'][:2])
    else:
        print("Unable to get the version of main branch")
        print(f"Got status code : {main_branch_url.status_code}")
        exit(1)


for item in versions_local:
    if item in versions_main:
        print("Version of " + item + " is already present in Main branch")
        exit(1)

print("Success")
#
#
# for env in ENVs:
#     local_branch_url = fetch(
#         f"https://api.github.com/repos/vijethkash123/GitWorkflowTest/contents/database_scripts/{env}?ref={CURRENT_BRANCH}",
#         headers={"accept": "application/vnd.github.v3", "Authorization": f"token {READ_TOKEN}"},
#     )
#     if local_branch_url.status_code == 200:
#         local_branch_url = json.loads(local_branch_url.content)
#         for file_info in local_branch_url:
#             print(file_info['name'][:2])
#             versions_local.add(file_info['name'][:2])
#     else:
#         print("Unable to get the version of local branch")
#         print(f"Got status code : {local_branch_url.status_code}")
#         exit(1)
#
# print(sorted(versions_local))
#
# # result = check_version(main_branch_version, local_branch_version)
# # print(result)