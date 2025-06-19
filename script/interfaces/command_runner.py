from typing import Protocol, runtime_checkable
import logging
import subprocess

@runtime_checkable
class CommandRunner(Protocol):
    def execute_command(self, args: list[str]) -> str: ...