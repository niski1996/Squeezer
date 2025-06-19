from command_executor import CommandExecutor
from pathlib import Path

def check_if_current_is_git_repo(executor: CommandExecutor) -> bool:
    """Check if the current path is a Git repository."""
    try:
        executor.execute_command(["git", "-C", Path(".").resolve(), "rev-parse", "--is-inside-work-tree"])
        executor.logger.debug(f"Current folder is Git repository.")
        return True
    except SystemExit:
        executor.logger.debug(f"Current folder ' is NOT a Git repository.")
        return False


def get_actual_git_branch(executor: CommandExecutor) -> str:
    """Return the current Git branch name."""
    branch = executor.execute_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    executor.logger.debug(f"Retrieved current branch: {branch}")
    return branch


def get_direct_branch_parent(executor: CommandExecutor) -> str:
    """Return the parent branch of the current Git branch."""
    parent = executor.execute_command(["git", "rev-parse", "--abbrev-ref", "HEAD^"])
    executor.logger.debug(f"Retrieved parent branch: {parent}")
    return parent
