import shutil

from colorama import Fore, Style, init

init(autoreset=True)


def create_banner() -> str:
    """Return the banner logo with a red-to-yellow per-line gradient.

    Returns:
        str: Multi-line banner string with top spacing and left-shifted layout.
    """
    logo_lines = [
        "",
        "",
        "                                            ████       █ ",
        "                                       ██████      █████ ",
        "                                   ████   ████    ██  █  ",
        "                                 █████          ██   █   ",
        "                      ██████  ███████         ██         ",
        "              ████████████  █████████        █           ",
        "          ██████████████  ███████████                    ",
        "        ███     ██████  ██████    ███               ███  ",
        "           █████████  ██████      ████████    ███████████",
        "      ████████████  █████          █████████         ██  ",
        "   ██████████████ █████                 █████████        ",
        " ███      █████  █████                                   ",
        "        ██████ █████                                                              /",
        "   █████████  ████                      _    _  _______  _______  ______         (             _______  _______                   ",
        " ███  █████  ████                      | |  / )(_______)(_______)(_____ \\       | |      /\\   (_______)(_______)                  ",
        "     █████ ████                        | | / /  _____    _____    _____) )       \\ \\    /  \\   _____    _____                     ",
        "    ██ ██ ████                         | |< <  |  ___)  |  ___)  |  ____/     /|  \\ \\  / /\\ \\ |  ___)  |  ___)                    ",
        "   █   █ ████                          | | \\ \\ | |_____ | |_____ | |         ( |__/  )| |__| || |      | |_____                   ",
        "         ███                           |_|  \\_)|_______)|_______)|_|         (______/ |______||_|      |_______)                  ",
        "        ████                                             ",
        "        ███                                █             ",
        "        ███                             ██               ",
        "        ███                         █████                ",
        "        ████                   ████████                  ",
        "        █████                    █████                   ",
        "         █████                 █████                     ",
        "          ██████           ███████                       ",
        "            ███████████████████                          ",
        "                ███████████                              ",
    ]
    terminal_width = shutil.get_terminal_size((120, 24)).columns
    content_width = max(len(line) for line in logo_lines)
    centered_padding = max((terminal_width - content_width) // 2, 0)
    left_padding = max(centered_padding - 24, 0)

    def rgb_foreground(red: int, green: int, blue: int) -> str:
        """Build a 24-bit ANSI foreground color escape sequence."""
        return f"\033[38;2;{red};{green};{blue}m"

    colored_lines = []
    for index, line in enumerate(logo_lines):
        if not line.strip():
            colored_lines.append("")
            continue
        shade_position = index / max(len(logo_lines) - 1, 1)
        green_value = int(255 * shade_position)
        colored_lines.append(
            " " * left_padding
            + Style.BRIGHT
            + rgb_foreground(255, green_value, 0)
            + line
        )
    return "\n\n" + "\n".join(colored_lines)


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
    print()
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
    header = Style.BRIGHT + Fore.CYAN + "\n=== PHISHING ANALYSIS TOOL ===\n"
    options = (
        Fore.BLUE + "[1] " + Fore.WHITE + "Analyze email\n"
        + Fore.BLUE + "[2] " + Fore.WHITE + "Analyze URL\n"
        + Fore.BLUE + "[3] " + Fore.WHITE + "Generate phishing template\n"
        + Fore.BLUE + "[4] " + Fore.WHITE + "View recent reports\n"
        + Fore.BLUE + "[5] " + Fore.WHITE + "Exit\n"
    )
    return header + "\n" + options


if __name__ == "__main__":
    print(create_banner())
    print_header("Quick Demos")
    print_info("Information message example")
    print_success("Success example")
    print_warning("Warning example")
    print_error("Error example")
