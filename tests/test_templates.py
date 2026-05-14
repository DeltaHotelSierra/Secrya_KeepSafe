import os
import shutil
from pathlib import Path
import tempfile

import pytest

from phishing_tool import templates


def test_slugify_edge_cases():
    assert templates._slugify("") == "template"
    assert templates._slugify("    ") == "template"
    # The implementation replaces non-alphanumerics with underscores; commas and
    # spaces become multiple underscores in sequence.
    assert templates._slugify("Hello, World!") == "Hello__World"
    assert templates._slugify("..weird--name..") == "weird--name"


def test_collision_avoidance(tmp_path):
    # Temporarily point GENERATED_DIR to a temp directory
    orig_dir = templates.GENERATED_DIR
    try:
        templates.GENERATED_DIR = tmp_path
        # Ensure dir exists
        templates._ensure_generated_dir()
        # Save first file
        out1 = templates.generate_template("vishing", save=True, name="coltest")
        # Save second file with same name; should not overwrite
        out2 = templates.generate_template("vishing", save=True, name="coltest")
        # Extract filenames from returned strings
        f1 = out1.splitlines()[-1].split(": ", 1)[1]
        f2 = out2.splitlines()[-1].split(": ", 1)[1]
        assert os.path.exists(f1)
        assert os.path.exists(f2)
        assert f1 != f2
    finally:
        templates.GENERATED_DIR = orig_dir
