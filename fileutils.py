"""fileutils: small file-handling helpers for a data-processing pipeline."""

import csv
import os
from typing import Dict, List


class FileOperationError(Exception):
    """Raised when a file operation fails. Keeps the original error message."""


class FileHandler:
    """Reads and writes text and CSV files using context managers."""

    ENCODING = "utf-8"

    # ---------- helper ----------
    def _ensure_path(self, path: str) -> None:
        """Make sure the directory that will hold `path` exists, creating it if needed."""
        directory = os.path.dirname(os.path.abspath(path))
        try:
            os.makedirs(directory, exist_ok=True)
        except OSError as exc:
            raise FileOperationError(f"Cannot create directory '{directory}': {exc}") from exc

    # ---------- text ----------
    def read_text(self, path: str) -> str:
        """Return the full contents of a UTF-8 text file."""
        try:
            with open(path, "r", encoding=self.ENCODING) as f:
                return f.read()
        except (OSError, UnicodeDecodeError) as exc:
            raise FileOperationError(f"Failed to read '{path}': {exc}") from exc

    def write_text(self, path: str, data: str) -> None:
        """Overwrite (or create) a text file with `data`."""
        self._ensure_path(path)
        try:
            with open(path, "w", encoding=self.ENCODING) as f:
                f.write(data)
        except (OSError, UnicodeEncodeError) as exc:
            raise FileOperationError(f"Failed to write '{path}': {exc}") from exc

    def append_text(self, path: str, data: str) -> None:
        """Append `data` to the file, creating it if necessary."""
        self._ensure_path(path)
        try:
            with open(path, "a", encoding=self.ENCODING) as f:
                f.write(data)
        except (OSError, UnicodeEncodeError) as exc:
            raise FileOperationError(f"Failed to append to '{path}': {exc}") from exc

    # ---------- csv ----------
    def read_csv(self, path: str) -> List[Dict[str, str]]:
        """Read a CSV file with a header row into a list of dictionaries."""
        try:
            with open(path, "r", encoding=self.ENCODING, newline="") as f:
                return [dict(row) for row in csv.DictReader(f)]
        except (OSError, UnicodeDecodeError, csv.Error) as exc:
            raise FileOperationError(f"Failed to read CSV '{path}': {exc}") from exc

    def write_csv(self, path: str, rows: List[Dict[str, str]]) -> None:
        """Write dictionaries to a CSV file; the first row's keys form the header."""
        self._ensure_path(path)
        try:
            with open(path, "w", encoding=self.ENCODING, newline="") as f:
                if not rows:
                    return  # nothing to write; leaves an empty file
                writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                writer.writeheader()
                writer.writerows(rows)
        except (OSError, UnicodeEncodeError, csv.Error, ValueError) as exc:
            # ValueError: a row contains keys that are not in the header
            raise FileOperationError(f"Failed to write CSV '{path}': {exc}") from exc