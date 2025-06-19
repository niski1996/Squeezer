import subprocess
from interfaces.logger import Logger
import sys
import logging

class DefaultCommandExecutor:
    def __init__(self, logger: Logger):
        self.logger = logger

    def execute_command(self, args: list[str]) -> str:
        if not args or not isinstance(args, list):
            raise ValueError("Argument 'args' must be a non-empty list of command arguments.")
        
        command_str = " ".join(str(arg) for arg in args)
        self.logger.debug(f"Executing command: {command_str}")

        try:
            result = subprocess.run(
                args,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return result.stdout.strip()

        except subprocess.CalledProcessError as e:
            error_msg = f"Command failed: {command_str}\nError: {e.stderr.strip()}"
            self.logger.error(error_msg)
            raise SystemExit(f"❌ {error_msg}")