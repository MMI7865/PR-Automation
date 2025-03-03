import os
from github import Github
from github import Auth
from github.GitRef import GitRef
from github.Repository import Repository
from github.PullRequest import PullRequest
from github.CommitCombinedStatus import CommitCombinedStatus
from github.CheckRun import CheckRun


# Get GitHub token from environment variable
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = "MMI7865/PR-Automation"

if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN environment variable not set!")

g = None

# Function to authenticate and get repository instance
def get_github_repo() -> Repository:
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    return repo

# Function to create a new branch from the default branch
def create_branch(branch_name: str):
    repo = get_github_repo()
    default_branch = repo.get_branch(repo.default_branch)  # Get default branch
    new_ref = f"refs/heads/{branch_name}"
    repo.create_git_ref(ref=new_ref, sha=default_branch.commit.sha)
    print(f"✅ Branch '{branch_name}' created successfully!")

def commit_changes(branch_name: str, file_path: str, new_content: str, commit_message: str):
    """Commit a change to a file in the repository on an existing branch."""
    repo = get_github_repo()

    # Get the file from the repository
    file = repo.get_contents(file_path, ref=branch_name)

    # Commit the new content
    repo.update_file(
        path=file.path,
        message=commit_message,
        content=new_content,
        sha=file.sha,
        branch=branch_name
    )
    print(f"✅ Committed changes to '{file_path}' on branch '{branch_name}'")

def create_pull_request(branch_name: str, pr_title: str, pr_body: str):
    """Create a pull request from the branch to the default branch."""
    repo = get_github_repo()

    pr = repo.create_pull(
        title=pr_title,
        body=pr_body,
        head=branch_name,
        base=repo.default_branch
    )

    print(f"✅ PR created: {pr.html_url}")
        