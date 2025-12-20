from github import Github
import os

g = Github(os.getenv("GITHUB_TOKEN"))
repo = g.get_repo(os.getenv("GITHUB_REPO"))

def get_logs(run_id):
    return repo.get_workflow_run(run_id).get_logs()
