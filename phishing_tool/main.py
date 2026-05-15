"""Main entry point for the Phishing Analysis Tool."""
import sys
from pathlib import Path

try:
    from . import ui, cli, analysis, templates, report, prompt_logger, url_security
except ImportError:  # pragma: no cover - support running as a script
    import ui
    import cli
    import analysis
    import templates
    import report
    import prompt_logger
    import url_security


def main() -> None:
    """Run the CLI entry point for the phishing analysis tool."""
    try:
        print(ui.create_banner())
        parser = cli.setup_parser()
        args = parser.parse_args()
        if not any([args.analyze, args.analyze_url, args.generate_template, args.interactive, getattr(args, 'list_templates', False)]):
            parser.print_help()
            return
        if args.analyze:
            if not cli.validate_file_path(args.analyze):
                ui.print_error(f"File not found: {args.analyze}")
                return
            content = open(args.analyze, encoding="utf-8").read()
            result = analysis.analyze_email(content)
            # Show colored output but save a plain-text copy without ANSI codes
            formatted = report.format_report(result, args.analyze, plain_text=False)
            print(formatted)
            plain_for_save = report.format_report(result, args.analyze, plain_text=True)
            saved_path = report.save_report(plain_for_save, f"email_{Path(args.analyze).stem}")
            ui.print_success(f"Report saved to: {saved_path}")
            return
        elif args.analyze_url:
            url_result = url_security.analyze_url_security(args.analyze_url)
            formatted = url_security.generate_url_security_report(
                url_result, args.analyze_url)
            print(formatted)
            # Save plain-text copy of the URL report
            try:
                plain_url = report.format_url_report(url_result, args.analyze_url, plain_text=True)
            except Exception:
                plain_url = formatted
            saved_path = report.save_report(
                plain_url, f"url_{url_result['domain'].replace('.', '_')}")
            ui.print_success(f"Report saved to: {saved_path}")
            return
        elif args.generate_template:
            # Support optional saving of templates to GENERATED_EMAILS/
            save_flag = getattr(args, "save_template", False)
            name = getattr(args, "template_name", None)
            out = templates.generate_template(args.generate_template, save=save_flag, name=name)
            print(out)
        elif getattr(args, "list_templates", False):
            entries = templates.list_generated_templates()
            if not entries:
                ui.print_info("No generated templates found in GENERATED_EMAILS/")
                return
            ui.print_header("Generated Templates")
            for idx, e in enumerate(entries, 1):
                print(f"{idx}. {e['name']}  (created: {e['created_iso']})")
        elif args.interactive:
            cli.handle_interactive_menu()
    except Exception as e:
        ui.print_error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
