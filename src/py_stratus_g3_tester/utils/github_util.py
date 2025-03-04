import os
import time
from github import Github
from github.Repository import Repository

# Get GitHub token from environment variable
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = "MMI7865/PR-Automation"

if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN environment variable not set!")


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
    return pr

def validate_pr_check(pr_number: int, check_name: str = "pr-check"):
    """
    Checks the status of a specific check run (default: "pr-check") for a given PR.
    Polls every 10 seconds until the check appears and completes, then prints the result.
    """
    repo = get_github_repo()
    pr = repo.get_pull(pr_number)
    latest_commit = pr.head.repo.get_commit(pr.head.sha)

    print(f"⚡ Monitoring '{check_name}' check run for PR #{pr_number} - {pr.title} (Commit SHA: {pr.head.sha})")

    target_check = None

    # Wait until the check run appears
    while not target_check:
        check_runs = latest_commit.get_check_runs()
        target_check = next((check for check in check_runs if check.name == check_name), None)

        if not target_check:
            print(f"⏳ Waiting for '{check_name}' check run to start...")
            time.sleep(10)

    while target_check.status in ["queued", "in_progress"]:
        print(f"\nCheck Run Name: {target_check.name}")
        print(f"Status: {target_check.status}")
        print("⏳ Check is still in progress. Waiting 10 seconds...")
        time.sleep(10)
        check_runs = latest_commit.get_check_runs()
        target_check = next((check for check in check_runs if check.name == check_name), None)

    print(f"\nCheck Run Name: {target_check.name}")
    print(f"Status: {target_check.status}")
    print(f"Conclusion: {target_check.conclusion}")
    print(f"Details URL: {target_check.html_url}")

    if target_check.conclusion == "success":
        print("✅ The check has passed!")
        return True
    else:
        print(f"❌ Check '{check_name}' failed!")
        return False
