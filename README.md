# Secrya KeepSafe

Version: 1.3.1
Author: DeltaHotelSierra

Overview

- Secrya KeepSafe is a lightweight CLI tool for analyzing potential phishing emails and URLs, generating phishing templates for training, and producing colorized reports.

Key features

- Email analysis: score emails for phishing risk, list indicators and explanations.
- URL security checks: DNS resolution, IP listing, known-company IP comparison, homoglyph/special-character detection, and a numeric risk score.
- Report generation: saves human-readable reports to `/reports/` with a colorized risk line.
- Interactive CLI: guided menus to analyze emails, URLs, generate templates, and view/delete saved reports.
- Prompt logging: stores prompts used for template generation and analysis (for audit/debug).

Quick start (Linux / macOS / Windows)

Prerequisites

- Python 3.9+ (3.11 or 3.12 recommended)
- Git

Verify your Python command first:

```bash
python3 --version
```

If `python3` is not available on macOS, use:

```bash
/usr/bin/python3 --version
```

Install

1. Clone the repository:

```bash
git clone https://github.com/DeltaHotelSierra/Secrya_KeepSafe.git
cd Secrya_KeepSafe
```

2. (Optional but recommended) Create and activate a virtual environment:

Linux / macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

macOS fallback (when `python3` is not found):

```bash
/usr/bin/python3 -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install Python dependencies:

```bash
python -m pip install -U pip
python -m pip install -r requirements.txt
```

If you are not using a virtual environment:

```bash
python3 -m pip install -r requirements.txt
# or on some macOS installs:
/usr/bin/python3 -m pip install -r requirements.txt
```

Run the tool

- Interactive mode (recommended):

```bash
python run.py --interactive
# or
python -m phishing_tool.main --interactive
```

If you are not in a virtual environment:

```bash
python3 run.py --interactive
# or
/usr/bin/python3 run.py --interactive
```

- Analyze a single URL from the CLI:

```bash
python -m phishing_tool.main --analyze-url "http://example.com"
```

Troubleshooting (macOS)

- `zsh: command not found: brew`:
  Homebrew is optional. You can run this project without Homebrew using `python3` or `/usr/bin/python3`.
- `xcode-select: Failed to locate 'python'`:
  Use `python3` instead of `python`, or use the absolute path `/usr/bin/python3`.
- Missing package errors such as `ModuleNotFoundError: No module named colorama`:

```bash
python -m pip install -r requirements.txt
```

Where reports are saved

- Generated reports are saved to the top-level `reports/` folder. Use `View recent reports` inside the interactive UI to open, delete, or delete-all.

How to add to a customer's computer

- Ensure Python and pip are installed.
- Copy the repository to the target machine (git clone or archive copy).
- Create a virtual environment and run `pip install -r requirements.txt`.
- Optionally create a systemd service or a scheduled task to run periodic checks or a wrapper script for convenience.

Files of interest

- `phishing_tool/` — main package and modules (ui.py, analysis.py, url_security.py, report.py, cli.py, templates.py, prompt_logger.py)
- `run.py` — launcher script to run the tool consistently without adjusting PYTHONPATH
- `reports/` — saved reports
- `phishing_tool/DROP_EMAILS_HERE/` — place email files here for analysis (one file per email)
- `phishing_tool/GENERATED_EMAILS/` — sample/generated emails for testing

Screenshots

- Add screenshots in this section. Example placeholders:

![Interactive Menu](screenshots/interactive_menu.png)

![Sample Report](screenshots/sample_report.png)

Platform-specific notes

- Linux: term colors work in standard terminals (xterm, gnome-terminal). For system installs, use virtualenv and a service wrapper.
- macOS: same as Linux; prefer the built-in Terminal or iTerm2 for 24-bit color support.
- Windows: use Windows Terminal or enable ANSI color support; PowerShell Core / Windows Terminal recommended.

Security & privacy notes

- This tool performs DNS lookups and network calls when analyzing URLs — ensure network policies allow this.
- Do not run untrusted mail-processing code in privileged environments.

Versioning & ownership

- Version: 1.3.1
- Owner / Author: DeltaHotelSierra

Support

- For issues, open a GitHub issue in the repository.

License

- Include your preferred license here.

test
test
