# Secrya KeepSafe

**Educational Phishing Analysis & Template Generation Tool**

[![Tests](https://img.shields.io/badge/tests-6%2F6%20passing-brightgreen)](#testing)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](#requirements)
[![License](https://img.shields.io/badge/license-MIT-green)](#license)

## Overview

Secrya KeepSafe is a lightweight, educational CLI tool designed to help security professionals and organizations understand phishing threats by:

- **Analyzing emails** for phishing indicators with risk scoring
- **Evaluating URLs** for security concerns (DNS validation, IP analysis, homoglyph detection)
- **Generating educational templates** for security awareness training
- **Creating reports** with colorized output for easy interpretation

## ✨ Key Features

- 🔍 **Email Analysis** - Comprehensive phishing indicator detection with explanations
- 🔗 **URL Security Checks** - DNS resolution, IP validation, character analysis
- 📊 **Risk Scoring** - Numerical risk assessment for emails and URLs
- 🎨 **Colorized Reports** - Human-readable output with visual risk indicators
- 🎓 **Template Generation** - 7 tactics for security training (spoofing, typosquatting, urgency, social engineering, pretexting, vishing, smishing)
- 📝 **Interactive CLI** - Guided menus for all operations
- 📋 **Report Management** - Save, view, and organize analysis reports
- 🔐 **Audit Logging** - Track all operations for compliance

## 📋 Requirements

- **Python**: 3.9 or higher (3.10+ recommended)
- **OS**: Linux, macOS, or Windows
- **Dependencies**: Listed in `requirements.txt`

## ⚡ Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/DeltaHotelSierra/Secrya_KeepSafe.git
cd Secrya_KeepSafe
```

### 2. Create Virtual Environment (Recommended)

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the Tool

**Interactive Mode (Recommended):**

```bash
python run.py --interactive
```

**CLI Mode:**

```bash
python run.py --analyze-url "https://example.com"
python run.py --generate-template spoofing --save-template
```

## 📖 Usage

### Interactive Mode

```bash
python run.py --interactive
```

Navigate menus to:

- Analyze emails for phishing
- Check URLs for security issues
- Generate educational templates
- View and manage reports

### Command-Line Mode

**Analyze URL:**

```bash
python run.py --analyze-url "https://suspicious-domain.com"
```

**Generate Template:**

```bash
python run.py --generate-template spoofing
python run.py --generate-template urgency --save-template --template-name "my_template"
```

**List Saved Templates:**

```bash
python run.py --list-templates
```

**Analyze Email File:**

```bash
python run.py --analyze "path/to/email.txt"
```

### Template Tactics

The tool supports 7 phishing tactics for training:

| Tactic               | Description                   |
| -------------------- | ----------------------------- |
| `spoofing`           | Email address/domain spoofing |
| `typosquatting`      | Similar-looking domain names  |
| `urgency`            | Pressure-based manipulation   |
| `social_engineering` | Trust exploitation            |
| `pretexting`         | False pretense setup          |
| `vishing`            | Voice-based phishing          |
| `smishing`           | SMS-based phishing            |

## 📁 Project Structure

```
Secrya_KeepSafe/
├── .github/
│   └── workflows/              # CI/CD pipelines
├── docs/
│   └── prompts_journal/        # Prompt logging and audit trail
├── phishing_tool/              # Main package
│   ├── __init__.py
│   ├── main.py                 # Entry point
│   ├── cli.py                  # Command-line interface
│   ├── analysis.py             # Email analysis engine
│   ├── url_security.py         # URL security checks
│   ├── templates.py            # Template generation
│   ├── report.py               # Report formatting
│   ├── ui.py                   # User interface utilities
│   ├── prompt_logger.py        # Audit logging
│   └── GENERATED_EMAILS/       # Sample templates
├── tests/                      # Test suite
│   ├── test_templates.py
│   └── test_templates_pytest.py
├── reports/                    # Generated analysis reports
├── setup.py                    # Package configuration
├── setup.cfg                   # Tool configuration
├── requirements.txt            # Python dependencies
├── run.py                      # Launcher script
├── README.md                   # This file
└── tox.ini                     # Testing configuration
```

## 🧪 Testing

### Run Tests Locally

```bash
# Activate virtual environment
source .venv/bin/activate

# Run all tests
pytest -v

# Run with coverage
pytest --cov=phishing_tool tests/
```

### Test All Python Versions (with tox)

```bash
pip install tox
tox
```

### CI/CD Pipeline

Tests automatically run on:

- Push to `main` or `updated-work-templates`
- Pull requests to `main`
- Python 3.10 and 3.11

## 🚀 Development

### Setup Development Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install pytest flake8
```

### Code Quality

```bash
# Linting
flake8 phishing_tool tests

# Format check
python -m black --check phishing_tool tests
```

### Adding Features

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make changes and test thoroughly
3. Ensure all tests pass: `pytest -v`
4. Submit a pull request

## 📋 Configuration

### Environment Variables

Create a `.env` file (optional):

```env
# Custom settings can be added here
LOG_LEVEL=INFO
```

### Report Location

Generated reports are saved to `/reports/` directory. View them using the interactive menu or directly from the file system.

## 🔧 Troubleshooting

### "ModuleNotFoundError: No module named 'phishing_tool'"

```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Run from project root
python run.py --interactive
```

### macOS Python Issues

If `python3` not found:

```bash
/usr/bin/python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Windows PowerShell Execution Policy

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\Activate.ps1
```

### Color Output Not Showing

Ensure using:

- Terminal.app / iTerm2 on macOS
- Windows Terminal on Windows (not legacy cmd.exe)
- Standard terminals on Linux

## 📊 Reports

Generated reports include:

- **Risk Score** (0-100): Overall phishing likelihood
- **Indicators** Found: Specific phishing indicators detected
- **Recommendations** : Actions to take
- **Timestamp**: When analysis was performed

Reports are saved as plaintext files in `/reports/` with ISO format timestamps.

## 🔐 Security Considerations

- This tool performs **network operations** (DNS lookups, IP validation)
- Does **NOT** send emails or data externally
- For suspicious URLs, analysis is read-only
- Suitable for **internal security training only**
- Do not run in restricted environments without approval

## 📝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Ensure all tests pass
4. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👤 Author

**DeltaHotelSierra**

- GitHub: [@DeltaHotelSierra](https://github.com/DeltaHotelSierra)
- Repository: [Secrya_KeepSafe](https://github.com/DeltaHotelSierra/Secrya_KeepSafe)

## 🙏 Acknowledgments

- Built for cybersecurity education and awareness
- Uses Python 3.9+ with minimal dependencies
- Community contributions welcome

## ❓ Support

- **Issues**: Open a GitHub issue for bugs and feature requests
- **Documentation**: Check this README and inline code comments
- **Examples**: See `phishing_tool/GENERATED_EMAILS/` for sample templates

---

**Last Updated:** May 15, 2026  
**Version:** 1.3.1  
**Status:** ✅ Production Ready

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

## Developer

Create a local development environment and run tests:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pytest -q
```

Optional: use tox to test across Python versions (requires tox installed and multiple Python interpreters available):

```bash
pip install tox
tox
```

Screenshots

- Add screenshots in this section. Example placeholders:

![Interactive Menu](screenshots/interactive_menu.png)

![Sample Report](screenshots/sample_report.png)

Platform-specific notes

- Linux: term colors work in standard terminals (xterm, gnome-terminal). For system installs, use virtualenv and a service wrapper.
- macOS: same as Linux; prefer the built-in Terminal or iTerm2 for 24-bit color support.
- Windows: use Windows Terminal or enable ANSI color support; PowerShell Core / Windows Terminal recommended.

---

**Last Updated:** May 15, 2026  
**Version:** 1.3.1  
**Status:** ✅ Production Ready

test
