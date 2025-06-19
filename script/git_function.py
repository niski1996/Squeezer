from interfaces.command_runner import CommandRunner
from interfaces.logger import Logger

def create_sibling_branch(souce_branch: str, target_branch_suffix: str,     runner: CommandRunner,
    logger: Logger) -> int:
    """Create a sibling branch with identical content and history to the source branch."""
    __git_add(runner, logger)
    __git_commit("Creating sibling branch", runner, logger)

    


def __git_add(
    runner: CommandRunner,
    logger: Logger,
    files: str = "."
) -> None:
    """Add files to the staging area.
    
    Args:
        runner: Command runner interface
        logger: Logger interface
    """
    try:
        runner.execute_command(["git", "add", "-A"])
        logger.debug(f"Added files to staging area")
    except SystemExit as e:
        logger.error(f"Failed to add files: {str(e)}")
        raise


def __git_commit(message: str, runner: CommandRunner, logger: Logger) -> None:
    """Commit changes to the repository.
    
    Args:
        message: Commit message
        runner: Command runner interface
        logger: Logger interface
    """
    if message is None:
        message = "message not provided"
    try:
        runner.execute_command(["git", "commit", "-m", message])
        logger.debug(f"Committed changes with message: {message}")
    except SystemExit as e:
        logger.error(f"Failed to commit changes: {str(e)}")
        raise

def create_sibling_branch(
    source_branch: str,
    new_branch_name: str,
    runner: CommandRunner,
    logger: Logger
) -> None:
    """Creates a new branch with identical content and history to source branch.
    
    Args:
        source_branch: Existing branch to copy from
        new_branch_name: Name for the new sibling branch
        runner: Command runner interface
        logger: Logger interface
    
    Raises:
        SystemExit: If any git command fails
    """
    try:
        # Verify source branch exists
        runner.execute_command(["git", "show-ref", "--verify", f"refs/heads/{source_branch}"])
        logger.debug(f"Verified source branch '{source_branch}' exists")

        # Create new branch pointing to same commit
        runner.execute_command(["git", "branch", new_branch_name, source_branch])
        logger.info(f"Created sibling branch '{new_branch_name}' from '{source_branch}'")

        # Optional: push to remote if needed
        # runner.execute_command(["git", "push", "origin", new_branch_name])
        
    except SystemExit as e:
        logger.error(f"Failed to create sibling branch: {str(e)}")
        raise

