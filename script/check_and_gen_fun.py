from command_executor import CommandExecutor
from pathlib import Path
from interfaces.command_runner import CommandRunner
from interfaces.logger import Logger


def check_if_current_is_git_repo(
    runner: CommandRunner,
    logger: Logger,
    path: Path = Path(".")
) -> bool:
    """Check if the current path is a Git repository."""
    try:
        runner.execute_command(["git", "-C", str(path.resolve()), "rev-parse", "--is-inside-work-tree"])
        logger.debug(f"Current folder {path} is Git repository.")
        return True
    except SystemExit:
        logger.debug(f"Current folder {path} is NOT a Git repository.")
        return False
    
def check_if_branch_exists(
    runner: CommandRunner,
    logger: Logger,
    branch_name: str
) -> bool:
    """Check if a specified branch exists in the Git repository."""
    try:
        runner.execute_command(["git", "rev-parse", "--verify", branch_name])
        logger.debug(f"Branch '{branch_name}' exists.")
        return True
    except SystemExit:
        logger.debug(f"Branch '{branch_name}' does NOT exist.")
        return False

def get_actual_git_branch(
    runner: CommandRunner,
    logger: Logger
) -> str:
    """Return the current Git branch name."""
    branch = runner.execute_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    logger.debug(f"Retrieved current branch: {branch}")
    return branch

def get_direct_branch_parent(
    runner: CommandRunner,
    logger: Logger
) -> str:
    """Return the parent branch of the current Git branch."""
    parent = runner.execute_command(["git", "rev-parse", "--abbrev-ref", "HEAD^"])
    logger.debug(f"Retrieved parent branch: {parent}")
    return parent