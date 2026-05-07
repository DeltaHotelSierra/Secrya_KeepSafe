import argparse
import os
import re
from datetime import datetime
from pathlib import Path

try:
    from . import ui, analysis, templates, report, url_security
except ImportError:  # pragma: no cover - support direct script execution
    import ui
    import analysis
    import templates
    import report
    import url_security


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
        "--interactive",
        action="store_true",
        dest="interactive",
        help="Launch the interactive menu",
    )
    return parser


def _list_test_emails() -> list:
    """List all email files in test_data folder."""
    test_data_dir = Path("test_data")
    if not test_data_dir.exists():
        return []
    email_files = sorted([f for f in test_data_dir.glob("*.txt")])
    return email_files


def _save_report(report_text: str, filename_prefix: str) -> str:
    """Save report to reports folder with timestamp. Returns the saved file path."""
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"{filename_prefix}_{timestamp}.txt"
    report_path = reports_dir / report_filename
    report_path.write_text(report_text, encoding="utf-8")
    return str(report_path)


def _list_saved_reports() -> list:
    """List all saved reports in reports folder."""
    reports_dir = Path("reports")
    if not reports_dir.exists():
        return []
    report_files = sorted(reports_dir.glob("*.txt"), reverse=True)
    return report_files


def _analyze_email_submenu() -> None:
    """Submenu for analyzing email files from test_data."""
    email_files = _list_test_emails()
    if not email_files:
        ui.print_error("No email files found in test_data/")
        return
    ui.print_header("Available Email Files")
    for idx, file_path in enumerate(email_files, 1):
        print(f"{idx}. {file_path.name}")
    try:
        choice = input("Select file number (or 0 to cancel): ").strip()
        if choice == "0":
            return
        file_idx = int(choice) - 1
        if file_idx < 0 or file_idx >= len(email_files):
            ui.print_error("Invalid selection")
            return
        selected_file = email_files[file_idx]
        content = selected_file.read_text(encoding="utf-8")
        result = analysis.analyze_email(content)
        formatted = report.format_report(result, selected_file.name)
        print(formatted)
        saved_path = _save_report(formatted, f"email_{selected_file.stem}")
        ui.print_success(f"Report saved to: {saved_path}")
    except ValueError:
        ui.print_error("Invalid input. Please enter a number.")
    except Exception as e:
        ui.print_error(f"Error analyzing email: {e}")


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
    url_report = f"""URL PHISHING ANALYSIS REPORT
========================
URL Analyzed: {result['url']}
Domain: {result['domain']}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SECURITY CHECK RESULTS:
------------------------

DNS Resolution:
  Status: {'✓ Resolved' if result['dns_resolved'] else '✗ Failed to resolve'}
  Error: {result['dns_error'] if result['dns_error'] else 'None'}
  Resolved IPs: {', '.join(result['resolved_ips']) if result['resolved_ips'] else 'N/A'}

Domain Verification:
  Status: {'✓ Verified Legitimate' if result['is_verified'] else '✗ Not Verified'}
  Details: {result['verification_status']}

Character Analysis:
  Suspicious Patterns: {'Yes' if result['special_chars_risk'] else 'No'}
  Details: {chr(10).join(['  - ' + risk for risk in result['char_risks']]) if result['char_risks'] else '  None detected'}

RISK ASSESSMENT:
------------------------
Risk Level: {result['risk_level']}

Detected Indicators:
{chr(10).join(['  - ' + indicator for indicator in result['risk_indicators']]) if result['risk_indicators'] else '  None detected'}

RECOMMENDATIONS:
------------------------
{chr(10).join(['  - ' + rec for rec in result['recommendations']])}

COPY-PASTE READY:
------------------------
Real Domain: {result['domain']}
Real IP(s): {', '.join(result['resolved_ips']) if result['resolved_ips'] else 'Unable to resolve'}
Visit: https://{result['domain']}
"""
    print(url_report)
    saved_path = _save_report(url_report, f"url_{result['domain'].replace('.', '_')}")
    ui.print_success(f"Report saved to: {saved_path}")


def _view_reports_submenu() -> None:
    """Submenu for viewing saved reports."""
    reports = _list_saved_reports()
    if not reports:
        ui.print_info("No saved reports found.")
        return
    ui.print_header("Saved Reports")
    for idx, report_file in enumerate(reports, 1):
        file_size = report_file.stat().st_size
        print(f"{idx}. {report_file.name} ({file_size} bytes)")
    try:
        choice = input("Select report number to view (or 0 to cancel): ").strip()
        if choice == "0":
            return
        report_idx = int(choice) - 1
        if report_idx < 0 or report_idx >= len(reports):
            ui.print_error("Invalid selection")
            return
        selected_report = reports[report_idx]
        content = selected_report.read_text(encoding="utf-8")
        print(content)
    except ValueError:
        ui.print_error("Invalid input. Please enter a number.")
    except Exception as e:
        ui.print_error(f"Error reading report: {e}")


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
        if choice == "6":
            print("Exiting...")
            return
        elif choice == "1":
            _analyze_email_submenu()
        elif choice == "2":
            ui.print_info("Mail client integration coming soon")
        elif choice == "3":
            _analyze_url_submenu()
        elif choice == "4":
            _generate_template_submenu()
        elif choice == "5":
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
