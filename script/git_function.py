from interfaces.command_runner import CommandRunner
from interfaces.logger import Logger


def check_if_current_is_git_repo(runner: CommandRunner, logger: Logger) -> bool:
    try:
        runner.execute_command(["git", "-C", ".", "rev-parse", "--is-inside-work-tree"])
        logger.debug("Current folder is Git repository")
        return True
    except SystemExit:
        logger.debug("Current folder is NOT a Git repository")
        return False