"""Main entry point for the Phishing Analysis Tool."""

import sys

try:
    from . import cli, ui
except ImportError:  # pragma: no cover - support running as a script
    import cli
    import ui


def main() -> None:
    """Run the CLI entry point for the phishing analysis tool."""
    try:
        print(ui.create_banner())
        parser = cli.setup_parser()
        args = parser.parse_args()
        if any([args.analyze, args.analyze_url, args.generate_template, args.interactive]):
            cli.run_from_args(args)
        else:
            cli.handle_interactive_menu()
    except Exception as exc:
        ui.print_error(f"Error: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
