import argparse
import os

try:
    from . import ui
except ImportError:  # pragma: no cover - support direct script execution
    import ui


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


def handle_interactive_menu() -> None:
    """Show the interactive menu and accept user choices (basic loop)."""
    while True:
        print(ui.create_interactive_menu())
        choice = input("Choice: ").strip()
        if choice == "5":
            print("Exiting...")
            return
        print(f"You selected: {choice}")
        print("Feature coming soon")


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
        print("Would analyze:", args.analyze)
    elif args.analyze_url:
        print("Would analyze URL:", args.analyze_url)
    elif args.generate_template:
        print("Would generate:", args.generate_template)
    elif args.interactive:
        handle_interactive_menu()
    else:
        parser.print_help()
