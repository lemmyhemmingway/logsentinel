import os
import time
from collections.abc import Callable
from typing import Any

from src.agents.base import BaseAgent, FileAgentConfig


class FileAgent(BaseAgent):
    """
    An agent that monitors a file for new lines (tail -f style)
    and processes them using a provided callback.
    """

    def __init__(self, config: FileAgentConfig, on_line_received: Callable[[str], None] = None):
        super().__init__(config)
        self.config: FileAgentConfig = config
        self.on_line_received = on_line_received
        self._last_position = 0

    def start(self):
        """Starts the tailing process."""
        if self._running:
            return

        if not os.path.exists(self.config.file_path):
            print(f"File not found: {self.config.file_path}. Waiting for it to be created...")

        self._running = True

        # Initialize position
        if self.config.read_from_end and os.path.exists(self.config.file_path):
            self._last_position = os.path.getsize(self.config.file_path)
        else:
            self._last_position = 0

        print(f"Agent {self.config.name} started, watching {self.config.file_path}")

        try:
            while self._running:
                self._poll()
                time.sleep(self.config.poll_interval)
        except KeyboardInterrupt:
            self.stop()

    def _poll(self):
        """Polls the file for new changes."""
        if not os.path.exists(self.config.file_path):
            return

        current_size = os.path.getsize(self.config.file_path)

        # If file was truncated or rotated
        if current_size < self._last_position:
            print(f"File {self.config.file_path} truncated or rotated. Resetting position.")
            self._last_position = 0

        if current_size > self._last_position:
            with open(self.config.file_path) as f:
                f.seek(self._last_position)
                lines = f.readlines()
                self._last_position = f.tell()

                for line in lines:
                    line = line.strip()
                    if line and self.on_line_received:
                        self.on_line_received(line)

    def stop(self):
        """Stops the agent."""
        print(f"Stopping agent {self.config.name}...")
        self._running = False

    def get_status(self) -> dict[str, Any]:
        return {
            "name": self.config.name,
            "running": self._running,
            "file_path": self.config.file_path,
            "last_position": self._last_position,
        }
