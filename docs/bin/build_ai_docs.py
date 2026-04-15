#!/usr/bin/env python
"""
Convert RST documentation to AI-friendly Markdown.

Reads RST files from docs/docsite/rst/, strips Sphinx-specific markup,
converts to GitHub Flavored Markdown via pandoc, and writes output to
docs/docsite/ai-docs/ with a manifest.json.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
RST_DIR = ROOT / "docs" / "docsite" / "rst"
OUTPUT_DIR = ROOT / "docs" / "docsite" / "ai-docs"
CORE_CONFIG = ROOT / "docs" / "ai-docs-core.yml"

# Top-level files to exclude (navigation-only)
EXCLUDE_FILES = {"ansible_index.rst", "core_index.rst"}

# Directories to skip entirely
EXCLUDE_DIRS = {"images", "shared_snippets"}

# Filename patterns to skip
EXCLUDE_NAMES = {"index.rst"}

# Audience classification by topic directory
AUDIENCE_MAP: dict[str, str] = {
    "dev_guide": "developer",
    "playbook_guide": "author",
    "inventory_guide": "author",
    "getting_started": "author",
    "getting_started_ee": "author",
    "vault_guide": "author",
    "tips_tricks": "author",
    "command_guide": "author",
}


def main() -> None:
    """Entry point — implemented in later tasks."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
