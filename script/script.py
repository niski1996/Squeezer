import sys
from pathlib import Path
import argparse
import logging
from command_executor import CommandExecutor
from check_and_gen_fun import *
from git_function import *


def setup_logger(verbose: bool = False) -> logging.Logger:
    """Configure and return a logger based on verbosity."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG if verbose else logging.INFO)
    
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    ch.setFormatter(formatter)
    
    # Avoid adding multiple handlers if setup_logger is called multiple times
    if not logger.hasHandlers():
        logger.addHandler(ch)
    
    return logger


def main():
    """Main function of the script."""
    
    AUXILIARY_BRANCH_SUFFIX = "dev"
    TAG_LIMITER = {"open": "[", "close": "]"}
    REQUIRED_TAGS = ["major", "minor", "patch", "config"]

    parser = argparse.ArgumentParser(description='Git repository checker script.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output.')
    parser.add_argument('-m', '--message', type=str, help='Message to display.')

    args = parser.parse_args()

    logger = setup_logger(args.verbose)
    executor = CommandExecutor(logger=logger)

    current_dir = Path(".").resolve()
    logger.debug(f"Checking directory: {current_dir}")

    if check_if_current_is_git_repo(executor):
        logger.info(f"Directory '{current_dir}' IS a Git repository.")
    else:
        logger.error(f"Directory '{current_dir}' is NOT a Git repository.")
        sys.exit(1)

    actual_branch = get_actual_git_branch(executor)
    logger.info(f"Current directory: {current_dir}")
    logger.info(f"Current branch: {actual_branch}")

    parent_branch = get_direct_branch_parent(executor)
    logger.info(f"Parent branch: {parent_branch}")
    if not parent_branch:
        logger.error(f"{actual_branch} has no parent branch. Check if it isn't a root branch.")
        sys.exit(1)
    target_branch = actual_branch.rstrip(" !\n")
    auxiliary_branch = f"{target_branch}-{AUXILIARY_BRANCH_SUFFIX}"

    target_branch_exists = check_if_branch_exists(executor, target_branch)
    auxiliary_branch_exists = check_if_branch_exists(executor, auxiliary_branch)
    if not target_branch_exists or not auxiliary_branch_exists:
        if not target_branch_exists:
            logger.error(f"Target branch '{target_branch}' does not exist.")
        
    
    


    if args.message:
        logger.info(f"Message: {args.message}")


if __name__ == "__main__":
    main()
