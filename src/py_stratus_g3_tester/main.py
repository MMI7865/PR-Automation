import uuid
from utils.github_util import create_branch, commit_changes, create_pull_request, validate_pr_check, auto_merge_pr
if __name__ == "__main__":
    branch_name = "test_" + str(uuid.uuid4())[:4]
    file_path = "README.md"
    new_content = "Updated README for testing commit changes.\n"
    commit_message = "Updated README.md for testing commit function"
    pr_title = "Update README with test content"
    pr_body = "This PR updates the README file to demonstrate how to create a PR using PyGithub."

    create_branch(branch_name)
    commit_changes(branch_name, file_path, new_content, commit_message)
    pr = create_pull_request(branch_name, pr_title, pr_body)
    if validate_pr_check(pr.number):
        auto_merge_pr(pr.number)
