"""Main entry point for the Phishing Analysis Tool."""
import sys

try:
    from . import ui, cli, analysis, templates, report, prompt_logger
except ImportError:  # pragma: no cover - support running as a script
    import ui
    import cli
    import analysis
    import templates
    import report
    import prompt_logger


def main() -> None:
    """Run the CLI entry point for the phishing analysis tool."""
    try:
        print(ui.create_banner())
        parser = cli.setup_parser()
        args = parser.parse_args()
        if not any([args.analyze, args.analyze_url, args.generate_template, args.interactive]):
            parser.print_help()
            return
        if args.analyze:
            if not cli.validate_file_path(args.analyze):
                ui.print_error(f"File not found: {args.analyze}")
                return
            content = open(args.analyze, encoding="utf-8").read()
            result = analysis.analyze_email(content)
            formatted = report.format_report(result, args.analyze)
            print(formatted)
        elif args.analyze_url:
            ui.print_info(f"URL analysis coming soon: {args.analyze_url}")
        elif args.generate_template:
            out = templates.generate_template(args.generate_template)
            print(out)
        elif args.interactive:
            cli.handle_interactive_menu()
    except Exception as e:
        ui.print_error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
