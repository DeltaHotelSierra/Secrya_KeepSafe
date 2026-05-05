import argparse
from pathlib import Path

try:
    from . import analysis, report, templates, ui
except ImportError:  # pragma: no cover - support direct script execution
    import analysis
    import report
    import templates
    import ui


BASE_DIR = Path(__file__).resolve().parent
TEST_DATA_DIR = BASE_DIR / "test_data"


def setup_parser() -> argparse.ArgumentParser:
    """Create and return the argparse.ArgumentParser for the tool."""
    parser = argparse.ArgumentParser(
        description="Phishing Analysis Tool - analyze emails, URLs, and generate templates"
    )
    parser.add_argument(
        "--analyze",
        dest="analyze",
        help="Analyze an email file for phishing indicators (provide file path)",
    )
    parser.add_argument(
        "--analyze-url",
        dest="analyze_url",
        help="Analyze a URL for scam indicators (provide url)",
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


def validate_file_path(path: str) -> bool:
    """Return True if the file exists on disk."""
    return Path(path).is_file()


def validate_url(url: str) -> bool:
    """Return True when the input looks like a usable URL."""
    if not url or not isinstance(url, str):
        return False
    stripped = url.strip()
    return stripped.startswith("http://") or stripped.startswith("https://") or "." in stripped


def _read_choice(prompt_text: str, valid_choices: set[str]) -> str:
    """Read a menu choice from the user until it matches a valid value."""
    while True:
        choice = input(prompt_text).strip()
        if choice in valid_choices:
            return choice
        ui.print_warning("Enter one of the listed numbers.")


def _read_backable_choice(prompt_text: str, max_choice: int) -> int | None:
    """Read a numeric choice or return None when the user goes back."""
    while True:
        choice = input(prompt_text).strip()
        if choice.lower() in {"b", "back", "q", "quit"}:
            return None
        if choice.isdigit():
            selection = int(choice)
            if 1 <= selection <= max_choice:
                return selection
        ui.print_warning("Enter a valid number or 'b' to go back.")


def _load_text_file(file_path: Path) -> str:
    """Load a UTF-8 text file from disk."""
    return file_path.read_text(encoding="utf-8")


def _show_report_and_save(report_text: str, report_name: str) -> None:
    """Print a report and persist it in the reports folder."""
    saved_path = report.save_report(report_text, report_name)
    print(report_text)
    ui.print_success(f"Report saved to {saved_path}")


def handle_email_file_menu() -> None:
    """List test email files, let the user pick one, and analyze it."""
    if not TEST_DATA_DIR.exists():
        ui.print_warning("test_data folder is missing.")
        return

    test_files = sorted(
        [path for path in TEST_DATA_DIR.iterdir() if path.is_file()
         and path.suffix.lower() == ".txt"],
        key=lambda path: path.name.lower(),
    )
    if not test_files:
        ui.print_warning("No email files found in test_data.")
        return

    while True:
        ui.print_header("Analyze Email File")
        for index, file_path in enumerate(test_files, start=1):
            ui.print_colored(f"{index}. {file_path.name}", "BLUE")
        ui.print_colored("B. Back", "WHITE")

        selection = _read_backable_choice("Select file: ", len(test_files))
        if selection is None:
            return

        selected_file = test_files[selection - 1]
        content = _load_text_file(selected_file)
        analysis_result = analysis.analyze_email(content)
        report_text = report.format_report(
            analysis_result, str(selected_file.name))
        _show_report_and_save(report_text, f"email_{selected_file.stem}")
        return


def handle_url_menu() -> None:
    """Prompt for a URL, analyze it, and save the report."""
    while True:
        ui.print_header("Analyze URL")
        ui.print_colored(
            "Enter a URL to inspect or type 'b' to go back.", "WHITE")
        url = input("URL: ").strip()
        if url.lower() in {"b", "back", "q", "quit"}:
            return
        if not validate_url(url):
            ui.print_warning("Enter a valid URL.")
            continue

        analysis_result = analysis.analyze_url(url)
        report_text = report.format_url_report(analysis_result, url)
        _show_report_and_save(report_text, "url_analysis")
        return


def handle_template_menu() -> None:
    """Offer template generation options."""
    template_options = {
        "1": "spoofing",
        "2": "typosquatting",
        "3": "urgency",
        "4": "social_engineering",
    }
    while True:
        ui.print_header("Generate Template")
        ui.print_colored("1. spoofing", "BLUE")
        ui.print_colored("2. typosquatting", "BLUE")
        ui.print_colored("3. urgency", "BLUE")
        ui.print_colored("4. social_engineering", "BLUE")
        ui.print_colored("B. Back", "WHITE")

        choice = input("Select template: ").strip().lower()
        if choice in {"b", "back", "q", "quit"}:
            return
        tactic = template_options.get(choice)
        if not tactic:
            ui.print_warning("Select a valid template number.")
            continue
        print(templates.generate_template(tactic))
        return


def handle_recent_reports_menu() -> None:
    """List recent saved reports and let the user view one."""
    while True:
        recent_reports = report.list_recent_reports()
        ui.print_header("Recent Reports")
        if not recent_reports:
            ui.print_warning("No reports have been saved yet.")
            return

        for index, report_path in enumerate(recent_reports, start=1):
            ui.print_colored(f"{index}. {report_path.name}", "BLUE")
        ui.print_colored("B. Back", "WHITE")

        selection = _read_backable_choice(
            "Select report: ", len(recent_reports))
        if selection is None:
            return

        selected_report = recent_reports[selection - 1]
        ui.print_separator()
        print(report.read_report(selected_report))
        ui.print_separator()
        return


def handle_interactive_menu() -> None:
    """Show the main menu and route each option to its submenu."""
    while True:
        print(ui.create_interactive_menu())
        choice = _read_choice("Choice: ", {"1", "2", "3", "4", "5"})
        if choice == "1":
            handle_email_file_menu()
        elif choice == "2":
            handle_url_menu()
        elif choice == "3":
            handle_template_menu()
        elif choice == "4":
            handle_recent_reports_menu()
        elif choice == "5":
            ui.print_info("Exiting...")
            return


def run_from_args(args: argparse.Namespace) -> None:
    """Run the non-interactive command selected by parsed arguments."""
    if args.analyze:
        if not validate_file_path(args.analyze):
            ui.print_error(f"File not found: {args.analyze}")
            return
        selected_file = Path(args.analyze)
        content = _load_text_file(selected_file)
        analysis_result = analysis.analyze_email(content)
        report_text = report.format_report(analysis_result, str(selected_file))
        _show_report_and_save(report_text, f"email_{selected_file.stem}")
        return

    if args.analyze_url:
        if not validate_url(args.analyze_url):
            ui.print_error(f"Invalid URL: {args.analyze_url}")
            return
        analysis_result = analysis.analyze_url(args.analyze_url)
        report_text = report.format_url_report(
            analysis_result, args.analyze_url)
        _show_report_and_save(report_text, "url_analysis")
        return

    if args.generate_template:
        print(templates.generate_template(args.generate_template))
        return

    if args.interactive:
        handle_interactive_menu()


if __name__ == "__main__":
    parser = setup_parser()
    parsed_args = parser.parse_args()
    if any([parsed_args.analyze, parsed_args.analyze_url, parsed_args.generate_template, parsed_args.interactive]):
        run_from_args(parsed_args)
    else:
        parser.print_help()
