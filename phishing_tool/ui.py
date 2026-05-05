from colorama import Fore, Style, init

init(autoreset=True)


def create_banner() -> str:
    """Return an ASCII art banner with a fish-on-hook theme.

    Returns:
        str: Multi-line banner string using color placeholders.
    """
    banner_lines = [
        Fore.CYAN + Style.BRIGHT + "      .-''''-.",
        Fore.CYAN + "     (  .--.  )",
        Fore.CYAN + "    (  (    )  )    " + Fore.YELLOW + "~ ~ ~",
        Fore.CYAN + "   |  |  ()  |  |   " + Fore.RED + "<==\"",
        Fore.CYAN + "    (  (    )  )",
        Fore.CYAN + "     '._'--'_.'",
        "",
        Fore.CYAN + Style.BRIGHT + "       PHISHING ANALYSIS TOOL",
    ]
    return "\n".join(banner_lines)


def print_colored(text: str, color: str, bold: bool = False) -> None:
    """Print `text` in the specified `color`.

    Args:
        text (str): Text to print.
        color (str): One of CYAN, RED, YELLOW, GREEN, MAGENTA, WHITE, BLUE.
        bold (bool): If True, print in bright style.
    """
    color_map = {
        "CYAN": Fore.CYAN,
        "RED": Fore.RED,
        "YELLOW": Fore.YELLOW,
        "GREEN": Fore.GREEN,
        "MAGENTA": Fore.MAGENTA,
        "WHITE": Fore.WHITE,
        "BLUE": Fore.BLUE,
    }
    col = color_map.get(color.upper(), Fore.WHITE)
    style = Style.BRIGHT if bold else Style.NORMAL
    print(style + col + text)


def print_success(message: str) -> None:
    """Print a success message in green and bold."""
    print_colored(message, "GREEN", bold=True)


def print_error(message: str) -> None:
    """Print an error message in red and bold."""
    print_colored(message, "RED", bold=True)


def print_info(message: str) -> None:
    """Print an informational message in cyan."""
    print_colored(message, "CYAN", bold=False)


def print_warning(message: str) -> None:
    """Print a warning message in yellow and bold."""
    print_colored(message, "YELLOW", bold=True)


def print_header(title: str) -> None:
    """Print a cyan bold header with a magenta separator."""
    print_colored(title, "CYAN", bold=True)
    print_colored("-" * len(title), "MAGENTA")


def print_separator() -> None:
    """Print a magenta dashed separator."""
    print_colored("-" * 60, "MAGENTA")


def print_risk_high() -> None:
    """Print a high risk indicator in red bold."""
    print_colored("RISK LEVEL: HIGH", "RED", bold=True)


def print_risk_medium() -> None:
    """Print a medium risk indicator in yellow bold."""
    print_colored("RISK LEVEL: MEDIUM", "YELLOW", bold=True)


def print_risk_low() -> None:
    """Print a low risk indicator in green bold."""
    print_colored("RISK LEVEL: LOW", "GREEN", bold=True)


def create_interactive_menu() -> str:
    """Return the formatted interactive menu string.

    Returns:
        str: Formatted menu ready to print.
    """
    header = Style.BRIGHT + Fore.CYAN + "=== PHISHING ANALYSIS TOOL ==="
    options = (
        Fore.BLUE + "1. " + Fore.WHITE + "Analyze email file\n"
        + Fore.BLUE + "2. " + Fore.WHITE + "Analyze URL\n"
        + Fore.BLUE + "3. " + Fore.WHITE + "Generate phishing template\n"
        + Fore.BLUE + "4. " + Fore.WHITE + "View recent reports\n"
        + Fore.BLUE + "5. " + Fore.WHITE + "Exit\n"
    )
    return header + "\n" + options


if __name__ == "__main__":
    print(create_banner())
    print_header("Quick Demos")
    print_info("Information message example")
    print_success("Success example")
    print_warning("Warning example")
    print_error("Error example")
