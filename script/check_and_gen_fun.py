from command_executor import CommandExecutor

def is_git_repo(executor: CommandExecutor, path: str = "./") -> bool:
    """Check if the given path is a Git repository."""
    try:
        executor.execute_command(["git", "-C", path, "rev-parse", "--is-inside-work-tree"])
        executor.logger.debug(f"Path '{path}' is a Git repository.")
        return True
    except SystemExit:
        executor.logger.debug(f"Path '{path}' is NOT a Git repository.")
        return False


def actual_git_branch(executor: CommandExecutor) -> str:
    """Return the current Git branch name."""
    branch = executor.execute_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    executor.logger.debug(f"Retrieved current branch: {branch}")
    return branch


def direct_branch_parent(executor: CommandExecutor) -> str:
    """Return the parent branch of the current Git branch."""
    parent = executor.execute_command(["git", "rev-parse", "--abbrev-ref", "HEAD^"])
    executor.logger.debug(f"Retrieved parent branch: {parent}")
    return parent
