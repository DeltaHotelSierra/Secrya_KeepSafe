import os
from pathlib import Path

import pytest

from phishing_tool import templates


def test_supported_tactics_return_educational_text():
    """Each supported tactic should return a string containing the marker text."""
    for tactic in templates.get_supported_tactics():
        out = templates.generate_template(tactic)
        assert isinstance(out, str)
        assert "EDUCATIONAL TEMPLATE" in out


def test_unknown_tactic_raises_value_error_with_message():
    """Providing an unknown tactic should raise ValueError mentioning 'Unknown template type'."""
    with pytest.raises(ValueError) as exc:
        templates.generate_template("this-does-not-exist")
    msg = str(exc.value)
    assert "Unknown template type" in msg or "Supported" in msg


def test_save_true_creates_file(tmp_path, monkeypatch):
    """When save=True a file is created in the GENERATED_DIR and contains the template."""
    # Redirect GENERATED_DIR to a temporary folder for the test
    monkeypatch.setattr(templates, "GENERATED_DIR", tmp_path)
    # Ensure the directory exists and is empty
    templates._ensure_generated_dir()

    out = templates.generate_template("spoofing", save=True, name="pytest_save")
    # Last line should contain the saved path
    saved_line = out.splitlines()[-1]
    assert "Saved to:" in saved_line
    saved_path = saved_line.split(": ", 1)[1]
    assert os.path.exists(saved_path)
    # File content should include educational marker
    content = Path(saved_path).read_text(encoding="utf-8")
    assert "EDUCATIONAL TEMPLATE" in content


def test_slugify_handles_special_characters():
    """_slugify should create a filename-safe slug and fall back to 'template' on empties."""
    assert templates._slugify("") == "template"
    assert templates._slugify("   ") == "template"
    # Comma + space become underscores (implementation allows sequences)
    assert templates._slugify("Hello, World!") == "Hello__World"
    assert templates._slugify("..weird--name..") == "weird--name"
