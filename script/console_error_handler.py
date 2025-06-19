import subprocess
import sys
import logging

class TerminalProcessor:
    def __init__(self, logger: logging.Logger):
        # Logger instance is required
        self.logger = logger


    def execute_command(self, args) -> str:
        if args is None or not isinstance(args, list):
            raise ValueError("Argument 'args' must be a list of command arguments.")
        command = " ".join(args)


        try:
            self.logger.debug(f"Executing command: {command}")
            # Run subprocess command and capture output
            result = subprocess.run(
                args,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True  # Decode bytes to str automatically
            )
            output = result.stdout.strip()

            return output

        except subprocess.CalledProcessError as e:
            # Log error message and exit
            self.logger.error(f"Command failed: {command}")
            error_msg = f"Error fetching parent branch: {e.stderr.strip()}"
            self.logger.error(error_msg)
            sys.exit(1)
