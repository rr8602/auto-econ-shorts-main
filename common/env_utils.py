import os

def is_github_actions():
    return os.getenv("GITHUB_ACTIONS") == "true"
