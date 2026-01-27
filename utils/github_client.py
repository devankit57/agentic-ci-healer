from github import Github
import os
from datetime import datetime

g = Github(os.getenv("GITHUB_TOKEN"))
repo = g.get_repo(os.getenv("GITHUB_REPO"))

def create_fix_pr(file, content):
    branch = f"agentic-fix-{int(datetime.utcnow().timestamp())}"
    base = repo.get_branch("main")

    repo.create_git_ref(
        ref=f"refs/heads/{branch}",
        sha=base.commit.sha
    )

    file_obj = repo.get_contents(file, ref=branch)

    repo.update_file(
        path=file,
        message="agentic-ci-healer: auto fix",
        content=file_obj.decoded_content.decode() + content,
        sha=file_obj.sha,
        branch=branch
    )

    pr = repo.create_pull(
        title="🤖 Agentic CI Healer Fix",
        body="Automatically generated fix by AI agent",
        head=branch,
        base="main"
    )

    return pr.html_url
