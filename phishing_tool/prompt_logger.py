from datetime import datetime
from pathlib import Path


class PromptLogger:
    """Logger for AI prompts and modifications.

    Args:
        journal_dir (str): Directory to store the prompt journal.
    """

    def __init__(self, journal_dir: str = "prompts_journal"):
        self.journal_dir = Path(journal_dir)
        self.journal_file = self.journal_dir / "PROMPT_LOG.md"
        self.journal_dir.mkdir(parents=True, exist_ok=True)
        if not self.journal_file.exists():
            self._create_header()

    def _create_header(self) -> None:
        """Create the initial header in the journal file."""
        header = (
            "# AI Prompt Journal\n"
            "This document records AI prompts, generated responses, and manual modifications.\n\n"
        )
        try:
            self.journal_file.write_text(header, encoding="utf-8")
        except Exception:
            # best-effort; caller can inspect file system
            pass

    def _get_next_prompt_number(self) -> int:
        """Return the next prompt number by counting entries in the file.

        Returns:
            int: Next prompt number (1-based)
        """
        try:
            text = self.journal_file.read_text(encoding="utf-8")
            count = text.count("## Prompt #")
            return count + 1
        except Exception:
            return 1

    def log_prompt(
        self,
        component_name: str,
        prompt_text: str,
        ai_response_summary: str,
        modifications_made: str,
        test_result: str,
        ai_tool: str = "ChatGPT",
        code_file: str = None,
        status: str = "Complete",
    ) -> bool:
        """Append a prompt entry to the journal file.

        Returns True on success, False on error.
        """
        entry_num = self._get_next_prompt_number()
        timestamp = datetime.utcnow().isoformat() + "Z"
        parts = [
            f"## Prompt #{entry_num}: {component_name}",
            f"**Date:** {timestamp}",
            f"**AI Tool:** {ai_tool}",
            "",
            "**What I Asked:**",
            prompt_text,
            "",
            "**AI Response (summary):**",
            ai_response_summary,
            "",
            "**Code File:**",
            code_file or "(none)",
            "",
            "**What I Modified:**",
            modifications_made,
            "",
            "**How I Tested:**",
            test_result,
            "",
            f"**Status:** {status}",
            "\n\n",
        ]
        try:
            with self.journal_file.open("a", encoding="utf-8") as fh:
                fh.write("\n".join(parts))
            return True
        except Exception:
            return False

    def get_journal_path(self) -> str:
        """Return the absolute path to the journal file."""
        return str(self.journal_file.resolve())


if __name__ == "__main__":
    pl = PromptLogger()
    ok = pl.log_prompt(
        component_name="Test Prompt Logger",
        prompt_text="Test prompt for prompt_logger",
        ai_response_summary="AI responded with test summary.",
        modifications_made="Created file and added header.",
        test_result="Ran prompt_logger and created PROMPT_LOG.md",
        code_file="prompt_logger.py",
    )
    if ok:
        print("Prompt logged to:", pl.get_journal_path())
    else:
        print("Failed to write prompt log")
