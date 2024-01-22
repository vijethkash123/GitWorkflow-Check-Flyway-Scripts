import base64
import json
import os
from sys import argv
import requests


READ_TOKEN = os.environ["READ_TOKEN"]



versions_main = set()
versions_local = set()
ENVs = ['common', 'ci', 'prod', 'qa']

# Run only if there are db_scrit file changes in a branch
owner = 'vijethkash123'
repo = 'GitWorkflowTest'
# branch = 'feature/add-DML-scripts'
# branch = quote(branch, safe='')
PR_NUMBER = argv[1]
READ_TOKEN = os.environ["READ_TOKEN"]
print(PR_NUMBER)
headers={"accept": "application/vnd.github.v3", "Authorization": f"token {READ_TOKEN}"}

files_changed_url = f"https://api.github.com/repos/vijethkash123/GitWorkflowTest/pulls/{PR_NUMBER}/files"
response = requests.get(files_changed_url, headers=headers)
if response.status_code != 200:
    print(f"Error: Unable to fetch changed files. Status code: {response.status_code}")
    exit(1)

changed_files_data = response.json()
file_names = [file['filename'] for file in changed_files_data]
# print("Changed Files:")
# for file_name in file_names:
#     print(file_name)

found = any('database_scripts' in file_name for file_name in file_names)

print("Database version conflict: "+ str(found))

if not found:
    print("No need to run compare, No database scripts changed")
    exit(0)

else:
    for file in file_names:
        if 'database_scripts' in file:
            temp = file.split('/')
            versions_local.add(temp[2][:2])

versions_local = sorted(versions_local)

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
        print("Version of" + item + " and maybe others already present in Main branch")
        raise Exception(f"Version is already present in Main branch")

print("Success")
exit(0)


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


# main_branch_url = fetch(
#         f"https://api.github.com/repos/vijethkash123/GitWorkflowTest/pulls/1",
#         headers={"accept": "application/vnd.github.v3, application/vnd.github.diff", "Authorization": f"token {READ_TOKEN}"},
#     )
# print(main_branch_url.content)
#
