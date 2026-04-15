"""Tests for docs/bin/build_ai_docs.py."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Add docs/bin to import path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "docs" / "bin"))

import build_ai_docs
