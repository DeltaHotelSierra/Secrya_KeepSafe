import argparse
import os
import re
from pathlib import Path

try:
    from . import ui, analysis, templates, report, url_security
except ImportError:  # pragma: no cover - support direct script execution
    import ui
    import analysis
    import templates
    import report
    import url_security


BASE_DIR = Path(__file__).resolve().parent
GENERATED_EMAILS_DIR = BASE_DIR / "GENERATED_EMAILS"
USER_EMAILS_DIR = BASE_DIR / "DROP_EMAILS_HERE"


def setup_parser() -> argparse.ArgumentParser:
    """Create and return the argparse.ArgumentParser for the tool."""
    parser = argparse.ArgumentParser(
        description="Phishing Analysis Tool - analyze emails and generate templates"
    )
    parser.add_argument(
        "--analyze",
        dest="analyze",
        help="Analyze email file for phishing indicators (provide file path)",
    )
    parser.add_argument(
        "--analyze-url",
        dest="analyze_url",
        help="Analyze URL for phishing (provide url)",
    )
    parser.add_argument(
        "--generate-template",
        dest="generate_template",
        help="Generate educational template: spoofing/typosquatting/urgency/social_engineering",
    )
    parser.add_argument(
        "--save-template",
        action="store_true",
        dest="save_template",
        help="When used with --generate-template, save the generated template to GENERATED_EMAILS/",
    )
    parser.add_argument(
        "--template-name",
        dest="template_name",
        help="Optional filename prefix when saving a generated template",
    )
    parser.add_argument(
        "--list-templates",
        action="store_true",
        dest="list_templates",
        help="List generated templates saved in GENERATED_EMAILS/",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        dest="interactive",
        help="Launch the interactive menu",
    )
    return parser


def _list_email_files(folder: Path) -> list:
    """List all text email files in the given folder."""
    if not folder.exists():
        return []
    email_files = sorted([f for f in folder.glob("*.txt")])
    return email_files


def _save_report(report_text: str, filename_prefix: str) -> str:
    """Save report to reports folder with timestamp. Returns the saved file path."""
    return str(report.save_report(report_text, filename_prefix))


def _list_saved_reports() -> list:
    """List all saved reports in reports folder."""
    return report.list_recent_reports(limit=200)


def _colorize_report_text(report_text: str) -> str:
    """Re-apply colored risk formatting when displaying a saved report."""
    ansi_pattern = re.compile(r"\x1b\[[0-9;]*m")
    risk_pattern = re.compile(
        r"^Risk Level:\s*(?P<level>.+?)\s*\((?P<score>[0-9]+(?:\.[0-9]+)?)\/10\)$")

    colored_lines = []
    for line in report_text.splitlines():
        plain_line = ansi_pattern.sub("", line)
        match = risk_pattern.match(plain_line)
        if match:
            colored_lines.append(
                report.format_risk_line(match.group(
                    "level").strip(), float(match.group("score")))
            )
        else:
            colored_lines.append(line)
    return "\n".join(colored_lines)


def _prompt_email_file_path() -> Path | None:
    """Prompt for a user-owned email file path."""
    file_path = input(
        "Enter the path to your email file (or 0 to cancel): ").strip()
    if file_path == "0":
        return None
    path = Path(file_path)
    if not path.is_file():
        ui.print_error("File not found")
        return None
    return path


def _analyze_email_file(path: Path) -> None:
    """Analyze an email file and save the report."""
    content = path.read_text(encoding="utf-8")
    result = analysis.analyze_email(content)
    formatted = report.format_report(result, path.name)
    print(formatted)
    saved_path = _save_report(formatted, f"email_{path.stem}")
    ui.print_success(f"Report saved to: {saved_path}")


def _analyze_email_submenu() -> None:
    """Submenu for analyzing generated or user-downloaded email files."""
    while True:
        ui.print_header("Email Analysis")
        print("1. Analyze generated email from GENERATED_EMAILS")
        print("2. Analyze your own email from DROP_EMAILS_HERE")
        print("0. Back")
        choice = input("Choice: ").strip()
        if choice == "0":
            return
        if choice == "1":
            email_files = _list_email_files(GENERATED_EMAILS_DIR)
            if not email_files:
                ui.print_error(
                    "No generated emails found in GENERATED_EMAILS/")
                continue
            ui.print_header("Available Generated Emails")
            for idx, file_path in enumerate(email_files, 1):
                print(f"{idx}. {file_path.name}")
            try:
                file_choice = input(
                    "Select file number (or 0 to cancel): ").strip()
                if file_choice == "0":
                    continue
                file_idx = int(file_choice) - 1
                if file_idx < 0 or file_idx >= len(email_files):
                    ui.print_error("Invalid selection")
                    continue
                _analyze_email_file(email_files[file_idx])
            except ValueError:
                ui.print_error("Invalid input. Please enter a number.")
            except Exception as e:
                ui.print_error(f"Error analyzing email: {e}")
        elif choice == "2":
            email_files = _list_email_files(USER_EMAILS_DIR)
            if not email_files:
                ui.print_error("No user emails found in DROP_EMAILS_HERE/")
                continue
            ui.print_header("Available Your Emails")
            for idx, file_path in enumerate(email_files, 1):
                print(f"{idx}. {file_path.name}")
            try:
                file_choice = input(
                    "Select file number (or 0 to cancel): ").strip()
                if file_choice == "0":
                    continue
                file_idx = int(file_choice) - 1
                if file_idx < 0 or file_idx >= len(email_files):
                    ui.print_error("Invalid selection")
                    continue
                _analyze_email_file(email_files[file_idx])
            except ValueError:
                ui.print_error("Invalid input. Please enter a number.")
            except Exception as e:
                ui.print_error(f"Error analyzing email: {e}")
        else:
            ui.print_warning("Invalid choice. Please try again.")


def _analyze_url_submenu() -> None:
    """Submenu for analyzing URLs for phishing."""
    ui.print_header("URL Phishing Analysis")
    url = input("Enter URL to analyze (or 0 to cancel): ").strip()
    if url == "0":
        return
    if not validate_url(url):
        ui.print_error("Invalid URL format")
        return

    ui.print_info(f"Analyzing URL: {url}")

    # Perform security analysis
    result = url_security.analyze_url_security(url)

    # Format comprehensive report
    url_report = url_security.generate_url_security_report(result, url)
    print(url_report)
    saved_path = _save_report(
        url_report, f"url_{result['domain'].replace('.', '_')}")
    ui.print_success(f"Report saved to: {saved_path}")


def _view_reports_submenu() -> None:
    """Submenu for viewing saved reports."""
    while True:
        reports = _list_saved_reports()
        if not reports:
            ui.print_info("No saved reports found.")
            return
        ui.print_header("Saved Reports")
        for idx, report_file in enumerate(reports, 1):
            file_size = report_file.stat().st_size
            print(f"{idx}. {report_file.name} ({file_size} bytes)")
        print("\nActions:")
        print("v. View a report")
        print("d. Delete selected reports")
        print("a. Delete all reports")
        print("0. Back")
        choice = input("Choice: ").strip().lower()
        if choice == "0":
            return
        if choice == "v":
            try:
                report_choice = input(
                    "Select report number to view (or 0 to cancel): ").strip()
                if report_choice == "0":
                    continue
                report_idx = int(report_choice) - 1
                if report_idx < 0 or report_idx >= len(reports):
                    ui.print_error("Invalid selection")
                    continue
                selected_report = reports[report_idx]
                content = selected_report.read_text(encoding="utf-8")
                print(_colorize_report_text(content))
            except ValueError:
                ui.print_error("Invalid input. Please enter a number.")
            except Exception as e:
                ui.print_error(f"Error reading report: {e}")
            continue
        if choice == "d":
            try:
                selection = input(
                    "Enter report numbers to delete separated by commas (or 0 to cancel): ").strip()
                if selection == "0":
                    continue
                indices = []
                for part in selection.split(","):
                    part = part.strip()
                    if not part:
                        continue
                    indices.append(int(part) - 1)
                if not indices:
                    ui.print_warning("No reports selected.")
                    continue
                to_delete = []
                for idx in sorted(set(indices)):
                    if idx < 0 or idx >= len(reports):
                        ui.print_error(
                            "One or more selected numbers are invalid")
                        to_delete = []
                        break
                    to_delete.append(reports[idx])
                if not to_delete:
                    continue
                confirm = input(
                    f"Delete {len(to_delete)} selected report(s)? (y/N): ").strip().lower()
                if confirm != "y":
                    continue
                for report_path in to_delete:
                    report_path.unlink(missing_ok=True)
                ui.print_success("Selected report(s) deleted.")
            except ValueError:
                ui.print_error(
                    "Invalid input. Please enter numbers separated by commas.")
            except Exception as e:
                ui.print_error(f"Error deleting reports: {e}")
            continue
        if choice == "a":
            confirm = input(
                "Delete ALL saved reports? (y/N): ").strip().lower()
            if confirm == "y":
                try:
                    for report_path in reports:
                        report_path.unlink(missing_ok=True)
                    ui.print_success("All reports deleted.")
                except Exception as e:
                    ui.print_error(f"Error deleting reports: {e}")
            continue
        ui.print_warning("Invalid choice. Please try again.")


def _generate_template_submenu() -> None:
    """Submenu for generating educational phishing templates."""
    tactics = ["spoofing", "typosquatting", "urgency", "social_engineering"]
    ui.print_header("Available Templates")
    for idx, tactic in enumerate(tactics, 1):
        print(f"{idx}. {tactic}")
    try:
        choice = input("Select template number (or 0 to cancel): ").strip()
        if choice == "0":
            return
        tactic_idx = int(choice) - 1
        if tactic_idx < 0 or tactic_idx >= len(tactics):
            ui.print_error("Invalid selection")
            return
        selected_tactic = tactics[tactic_idx]
        template_output = templates.generate_template(selected_tactic)
        print(template_output)
    except ValueError:
        ui.print_error("Invalid input. Please enter a number.")
    except Exception as e:
        ui.print_error(f"Error generating template: {e}")


def handle_interactive_menu() -> None:
    """Show the interactive menu and execute user choices."""
    while True:
        print(ui.create_interactive_menu())
        choice = input("Choice: ").strip()
        if choice == "5":
            print("Exiting...")
            return
        elif choice == "1":
            _analyze_email_submenu()
        elif choice == "2":
            _analyze_url_submenu()
        elif choice == "3":
            _generate_template_submenu()
        elif choice == "4":
            _view_reports_submenu()
        else:
            ui.print_warning("Invalid choice. Please try again.")
        print()


def validate_file_path(path: str) -> bool:
    """Return True if the file exists on disk."""
    return os.path.isfile(path)


def validate_url(url: str) -> bool:
    """Basic URL validation: returns True if starts with http/https or looks like domain."""
    if not url or not isinstance(url, str):
        return False
    url = url.strip()
    return url.startswith("http://") or url.startswith("https://") or "." in url


if __name__ == "__main__":
    parser = setup_parser()
    args = parser.parse_args()
    if args.analyze:
        if not validate_file_path(args.analyze):
            print(f"Error: File not found: {args.analyze}")
        else:
            try:
                content = open(args.analyze, encoding="utf-8").read()
                result = analysis.analyze_email(content)
                formatted = report.format_report(result, args.analyze)
                print(formatted)
            except Exception as e:
                print(f"Error: {e}")
    elif args.analyze_url:
        print(f"URL analysis coming soon: {args.analyze_url}")
    elif args.generate_template:
        print(templates.generate_template(args.generate_template))
    elif args.interactive:
        handle_interactive_menu()
    else:
        parser.print_help()
