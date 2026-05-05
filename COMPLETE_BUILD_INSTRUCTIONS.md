# Phishing Analysis Tool - Complete AI Build Instructions

All instructions for building this project with AI in one file. Follow this exactly.

---

## PART 1: SETUP (Do this first)

### 1.1 GitHub Codespaces Setup (Recommended)

```bash
# In Codespaces terminal after opening repo:
mkdir -p phishing_tool
cd phishing_tool

# Create project structure
mkdir -p prompts_journal
mkdir -p test_data
mkdir -p reports

# Create empty files (will fill with AI-generated code)
touch main.py cli.py analysis.py templates.py report.py ui.py prompt_logger.py

# Create requirements.txt
cat > requirements.txt << 'EOF'
colorama==0.4.6
tabulate==0.9.0
python-dotenv==1.0.0
EOF

# Install dependencies
pip3 install -r requirements.txt

# Verify installation
python3 -c "import colorama; print('Ready!')"
```

### 1.2 Local Machine Setup

```bash
git clone https://github.com/YOUR_USERNAME/phishing-analysis-tool.git
cd phishing-analysis-tool/phishing_tool

python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

# Verify
python3 -c "import colorama; print('Ready!')"
```

---

## PART 2: TEST DATA (Create these files now)

### 2.1 Phishing Test Email

Create file: `test_data/phishing_example.txt`

```
From: "Bank Support" <support@your-bank.com>
Subject: URGENT: Verify Your Account Immediately
To: user@example.com
Date: Wed, 7 May 2025 14:23:00 -0500

Dear Valued Customer,

We have detected suspicious activity on your account. Your access will be REVOKED in 24 hours unless you verify your identity immediately.

Click the link below to verify your account:

https://verify-bank-account-security.com/login

Do not delay. Your account security depends on immediate action.

Best regards,
Bank Support Team
support@your-bank.com
```

### 2.2 Legitimate Test Email

Create file: `test_data/legitimate_example.txt`

```
From: noreply@github.com
Subject: You have a new notification on GitHub
To: user@example.com
Date: Wed, 7 May 2025 15:45:22 UTC

Hi user,

You received a notification on GitHub.

View it on GitHub: https://github.com/notifications

---

You're receiving this email because you're watching this repository.

Manage your notification settings: https://github.com/settings/notifications

GitHub
88 Colin P Kelly Jr St
San Francisco, CA 94107 USA
```

---

## PART 3: BUILD COMPONENTS WITH AI (Follow in this order)

### 3.1 COMPONENT 1: Terminal UI with Fish/Hook Theme

**What to do:**
1. Copy the prompt below exactly
2. Paste into ChatGPT/Claude/Copilot
3. Copy the code it generates
4. Paste into `ui.py`
5. Test: `python3 ui.py`

**PROMPT TO GIVE AI:**

```
Create a Python module called ui.py for colorful terminal output using colorama.

Requirements:

1. Import colorama (Fore, Back, Style, init)
2. Initialize colorama with init(autoreset=True)

3. Create function: create_banner() -> str
   - Returns ASCII art banner with fish on hook theme
   - Use colorama colors: Cyan for fish/water, Red for hook, Yellow for line
   - Include tool name "PHISHING ANALYSIS TOOL"
   - 8-10 lines tall
   - No emojis, only ASCII characters
   
   Example structure:
   ~~~TOOL NAME~~~
                _    _  _______  _______  ______      _             _______  _______ 
               | |  / )(_______)(_______)(_____ \    | |      /\   (_______)(_______)
               | | / /  _____    _____    _____) )    \ \    /  \   _____    _____   
               | |< <  |  ___)  |  ___)  |  ____/      \ \  / /\ \ |  ___)  |  ___)  
               | | \ \ | |_____ | |_____ | |       _____) )| |__| || |      | |_____ 
               |_|  \_)|_______)|_______)|_|      (______/ |______||_|      |_______)
                                                                                                        
                                       
                                                ==+                                                 
                                        ==::--=*==*#                                **+*####        
                                     =:---------==+*                           ==##=#%#+#%          
                                  ----=--:=------=  **                      -==--==**#**            
                        =--=-*-::-==-::::-::-------=+++                  -*----==*+##               
                    ==::-:*+:+==-::-:--=+++:::::::---===+++            -==-------###*               
                 -:-=#**%=%=*+#-+**=*=*-=:-:=:-==:-:-----=-=         -**==--=--=+*#    *            
              --:-%=#**@=*+=*++==*----==-+=+=-===+:---:----===    -:==--=-----=--==+***             
          --:.-::-*+%=%=++=%+*++=+==#=+=+=+=+=+=+=+===---=+*    -*:+-=---:--::++--+*+               
      =-::--::-==:-=#**+%**#*%+%+*##%%+#=**+=+++==+*--+==+=-+=---*=::=--=:-----==++*                
   =-::.-:=-:*#*==::+##*@*%-@+%=%=*%#*%%*#=#+*+*++%==*-+*+-++-+===*=--=----=-====+*                 
   ::::+*:=+--#%@@+:-**@*@*****+%+%===+*%=*=*=#=*#+*++#+*++*#*#++*++--===++-=-=+*#                  
   -=:-==+++--+*#*-:=+%##**++++++#=*+*##+*+*#*#+=*=+*+#*++#*+%**=#==--=-------=###                  
    ++=====+--##-+=-+*+%+#=#+****=+++*##+#+%=+=++**=#%=##++#++*++**=:::+-------=**#                 
      =+==-=---+==--+%=#+++++#-*+*++*=#+#**++++=#++#=+*+=++=*++*++=---=-------==#######             
         =+++=++=-:-=+#=+*+#+**+%=%+**+++*+**=+++#++*+=*+=*==-=+ #---=---------=*=+#                
           ++=====-::=*%%**=#=##*+==#****+*+****++*+*++==--=          +=-----------=++*##           
              +=*++-::::-**###*%**+**#+#+#***+**#*+=+*+=:-:--==#          *----==----=***+*#        
                +++=#=--:::--**++*-*=+=+++=+=+-===+===::------===             +-=======+****####    
                   .+++=---:--=*==-=:--===+======        -=-:--+--=*   +***        +=++**##*        
                   :::       .  --:::::::-=*                                             +++++*     
                   ---           =:::::-:---+                                                       
                    ===            -::-------+*                                                     
                    ===             -----+-----*%                                                   
                     +=               =++*%#%  #=*                                                  
                                       *+#%@                                                        
                                          #%                                                        
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                            
                                                            
                                                            
                                                            


4. Create function: print_colored(text: str, color: str, bold: bool = False) -> None
   - Prints text in specified color
   - Supported colors: CYAN, RED, YELLOW, GREEN, MAGENTA, WHITE, BLUE
   - If bold=True, use Style.BRIGHT

5. Create these status functions (all use print_colored):
   - print_success(message: str) - Green, bold
   - print_error(message: str) - Red, bold
   - print_info(message: str) - Cyan, normal
   - print_warning(message: str) - Yellow, bold

6. Create these output functions:
   - print_header(title: str) - Cyan bold title + magenta line separator
   - print_separator() - Print magenta dashes
   - print_risk_high() - RED bold "RISK LEVEL: HIGH"
   - print_risk_medium() - YELLOW bold "RISK LEVEL: MEDIUM"
   - print_risk_low() - GREEN bold "RISK LEVEL: LOW"

7. Create function: create_interactive_menu() -> str
   Returns formatted menu string:
   === PHISHING ANALYSIS TOOL ===
   1. Analyze email file
   2. Analyze URL
   3. Generate phishing template
   4. View recent reports
   5. Exit
   
   Use CYAN for header, BLUE for options, WHITE for text

8. Main execution: if __name__ == "__main__":
   Call create_banner() and print it
   Test a few print functions to show colors work

Use only standard colorama imports. No external fancy libraries.
Add docstrings to every function.
```

**After AI generates:**
- Save to `ui.py`
- Test: `python3 ui.py`
- You should see colorful output with fish ASCII art
- If it works, move to next component

**If it breaks:**
- Ask AI: "I got this error: [error message]. How do I fix it?"
- Don't delete code, test the fix separately

---

### 3.2 COMPONENT 2: Prompt Logger

**What to do:**
1. Copy the prompt below
2. Paste into ChatGPT/Claude/Copilot
3. Copy the code
4. Paste into `prompt_logger.py`
5. Test: `python3 prompt_logger.py`

**PROMPT TO GIVE AI:**

```
Create a Python module called prompt_logger.py to log AI-assisted code generation.

This tracks every prompt you give to AI and documents what you modify.

Requirements:

1. Import: datetime, pathlib (Path)

2. Create class: PromptLogger
   
   __init__(self, journal_dir="prompts_journal"):
   - Set self.journal_dir = Path(journal_dir)
   - Set self.journal_file = self.journal_dir / "PROMPT_LOG.md"
   - Create directory if it doesn't exist: self.journal_dir.mkdir(exist_ok=True)
   - If journal file doesn't exist, create it with a header

3. Method: _create_header(self)
   - Writes initial markdown header to journal file
   - Header should explain what this journal is for
   - Something like: "# AI Prompt Journal\nThis documents all AI-assisted code..."

4. Method: log_prompt(self, component_name, prompt_text, ai_response_summary, modifications_made, test_result, ai_tool="ChatGPT", code_file=None, status="Complete")
   - Takes parameters for each component
   - Creates formatted markdown entry with:
     * Date and time
     * AI tool used
     * Original prompt
     * What AI generated (summary)
     * Code file affected
     * What you modified
     * How you tested it
     * Status
   - Appends to journal_file
   - Returns True if successful, False if error
   - Include try-except for error handling

5. Method: _get_next_prompt_number(self) -> int
   - Counts existing "## Prompt #" entries in file
   - Returns count + 1
   - Handle errors gracefully

6. Method: get_journal_path(self) -> str
   - Returns absolute path to journal file as string

7. Main execution: if __name__ == "__main__":
   - Create PromptLogger instance
   - Call log_prompt() with test data
   - Print success message with journal path

Add docstrings to every method with parameter descriptions.
Use only stdlib (datetime, pathlib).
Include error handling for file operations.
```

**After AI generates:**
- Save to `prompt_logger.py`
- Test: `python3 prompt_logger.py`
- Check that file `prompts_journal/PROMPT_LOG.md` was created
- It should have an entry logged
- If it works, move to next component

---

### 3.3 COMPONENT 3: CLI Input Handler

**What to do:**
1. Copy the prompt below
2. Paste into ChatGPT/Claude/Copilot
3. Copy the code
4. Paste into `cli.py`
5. Test: `python3 -c "from cli import setup_parser; setup_parser()"`

**PROMPT TO GIVE AI:**

```
Create a Python module called cli.py for command-line interface handling using argparse.

Requirements:

1. Import argparse

2. Create function: setup_parser() -> argparse.ArgumentParser
   - Create ArgumentParser with description about phishing analysis tool
   - Add these arguments:
     * --analyze [file] : Analyze email file for phishing (required argument: file path)
     * --analyze-url [url] : Analyze URL for phishing (required argument: url)
     * --generate-template [tactic] : Generate template (required: spoofing/typosquatting/urgency)
     * --interactive : Launch interactive menu (no argument needed, just a flag)
     * --help : Show help (built-in with argparse)
   
   - Return the parser object (don't call parse_args yet)
   - Include help text for each argument explaining what it does

3. Create function: handle_interactive_menu() -> None
   - Shows menu (you can hardcode or call from ui module)
   - Gets user input for choice (1-5)
   - For this version, just show menu and accept input
   - Print "You selected: [choice]"
   - For option 5, print "Exiting..." and return
   - For other options, print placeholder like "Feature coming soon"
   
   Example flow:
   === PHISHING ANALYSIS TOOL ===
   1. Analyze email file
   2. Analyze URL
   3. Generate phishing template
   4. View recent reports
   5. Exit
   
   Choice: 1
   "You selected: 1"
   [loop back to menu or exit]

4. Function: validate_file_path(path: str) -> bool
   - Check if file exists
   - Return True if exists, False otherwise
   - Don't print errors (caller will handle)

5. Function: validate_url(url: str) -> bool
   - Check if url looks valid (very basic: starts with http or is a domain)
   - Return True if looks valid, False otherwise

6. Main execution: if __name__ == "__main__":
   - Parse arguments
   - If --analyze: print "Would analyze: [file]"
   - If --analyze-url: print "Would analyze URL: [url]"
   - If --generate-template: print "Would generate: [template]"
   - If --interactive: call handle_interactive_menu()
   - If no args: print help

Add docstrings to every function.
Include error messages that are user-friendly.
Use only argparse (stdlib).
```

**After AI generates:**
- Save to `cli.py`
- Test: `python3 -c "from cli import setup_parser; p = setup_parser(); print('Success')"`
- Test: `python3 cli.py --help` (should show help text)
- If works, move to next component

---

### 3.4 COMPONENT 4: Phishing Analysis Engine

**What to do:**
1. Copy the prompt below
2. Paste into ChatGPT/Claude/Copilot
3. Copy the code
4. Paste into `analysis.py`
5. Test: See instructions below

**PROMPT TO GIVE AI:**

```
Create a Python module called analysis.py for phishing detection.

Requirements:

1. Import: re (for regex)

2. Create function: check_sender_spoofing(email_text: str) -> dict
   - Extract "From:" line from email
   - Check for common domain spoofing patterns:
     * goog1e.com (1 instead of l)
     * amaz0n.com (0 instead of o)
     * m1crosoft.com (1 instead of i)
     * paypol.com (l instead of 1)
   - Return dict: {"detected": True/False, "risk_score": 0-10, "details": "explanation"}
   - If spoofing detected, risk_score should be 8-10
   - If not detected, risk_score should be 0-2
   - On error (malformed email), return {"detected": False, "risk_score": 0, "details": "Could not parse"}

3. Create function: check_urgency_language(email_text: str) -> dict
   - Look for urgency keywords: "immediately", "urgent", "NOW", "URGENT", "24 hours", "verify", "REVOKED"
   - Count how many appear
   - If 1-2 keywords: risk_score 4-5
   - If 3+ keywords: risk_score 7-10
   - If none: risk_score 0
   - Return dict with detected keywords list and risk_score

4. Create function: check_link_mismatch(email_text: str) -> dict
   - Find URLs in email (look for http:// or https://)
   - Check if URL domain matches sender domain
   - If sender is support@yourbank.com but URL is verify-bank-account.com, flag as mismatch
   - Return dict: {"mismatch_detected": True/False, "risk_score": 0-10, "details": "..."}
   - Mismatch = high risk (8-10)
   - Match = low risk (0-2)

5. Create function: analyze_email(email_text: str) -> dict
   - Call all three check functions above
   - Aggregate risk scores (average them)
   - Determine risk level: HIGH (7-10), MEDIUM (4-6), LOW (0-3)
   - Return dict:
     {
       "risk_level": "HIGH/MEDIUM/LOW",
       "risk_score": float (0-10),
       "indicators": ["list", "of", "detected", "indicators"],
       "explanations": ["why", "each", "matters"],
       "details": {
         "spoofing": {...from check_sender_spoofing...},
         "urgency": {...from check_urgency_language...},
         "link_mismatch": {...from check_link_mismatch...}
       }
     }

6. Error handling:
   - If email_text is empty, return {"risk_level": "UNKNOWN", "risk_score": 0, "indicators": [], "details": "Empty email"}
   - Use try-except for any parsing errors

Add docstrings to every function with examples.
Use only stdlib (re).
All functions return dictionaries with consistent structure.
```

**After AI generates:**
- Save to `analysis.py`
- Test it: `python3 << 'EOF'
from analysis import analyze_email
test_email = open('test_data/phishing_example.txt').read()
result = analyze_email(test_email)
print(result)
EOF`
- Should show HIGH risk (8+)
- Try with legitimate_example.txt too
- Should show LOW risk (0-3)

---

### 3.5 COMPONENT 5: Template Generator

**What to do:**
1. Copy the prompt below
2. Paste into ChatGPT/Claude/Copilot
3. Copy the code
4. Paste into `templates.py`
5. Test: `python3 -c "from templates import generate_template; print(generate_template('spoofing'))"`

**PROMPT TO GIVE AI:**

```
Create a Python module called templates.py to generate educational phishing templates.

Requirements:

1. Create function: generate_template(tactic: str) -> str
   Takes one parameter: tactic name
   Supported tactics: "spoofing", "typosquatting", "urgency", "social_engineering"
   
   Returns formatted string showing what that attack looks like.

2. For tactic="spoofing":
   Generate example showing CEO/authority impersonation
   Include:
   - Header: "EDUCATIONAL TEMPLATE: Email Spoofing"
   - Example showing fake "From:" field
   - Example showing what real domain would be
   - Explanation (5-10 lines): Why this works, how attacker fools users
   - Defense (3-5 lines): How to protect against this
   - Use plain text, no colors (colors applied by ui module)

3. For tactic="typosquatting":
   Generate example showing domain misspellings
   Include:
   - Header: "EDUCATIONAL TEMPLATE: Typosquatting"
   - Show examples: goog1e.com vs google.com, amaz0n.com vs amazon.com
   - Explanation: Why single-char changes are hard to spot
   - Defense: How to verify real domains

4. For tactic="urgency":
   Generate example showing time pressure tactics
   Include:
   - Header: "EDUCATIONAL TEMPLATE: Urgency-Based Attack"
   - Example email with urgency language: "24 hours", "REVOKED", "immediately"
   - Explanation: Why urgency bypasses critical thinking
   - Defense: Legitimate companies don't pressure you

5. For tactic="social_engineering":
   Generate example showing credential harvesting
   Include:
   - Header: "EDUCATIONAL TEMPLATE: Social Engineering"
   - Example fake form asking for password/SSN
   - Explanation: Why people fall for authority requests
   - Defense: Legitimate companies never ask for passwords via email

6. Invalid tactic handling:
   If tactic not recognized, return:
   "Error: Unknown template type '[tactic]'. Supported: spoofing, typosquatting, urgency, social_engineering"

7. Format all templates consistently:
   - All caps headers
   - Clear sections separated by dashes
   - Plain text (no markdown formatting, no colors)
   - 20-30 lines total per template

Add docstring to function with examples of each tactic type.
Use only stdlib.
All templates should be educational and explain the attack.
```

**After AI generates:**
- Save to `templates.py`
- Test each template:
  ```bash
  python3 -c "from templates import generate_template; print(generate_template('spoofing'))"
  python3 -c "from templates import generate_template; print(generate_template('typosquatting'))"
  python3 -c "from templates import generate_template; print(generate_template('urgency'))"
  ```
- Each should print educational template
- If works, move to next component

---

### 3.6 COMPONENT 6: Report Formatter

**What to do:**
1. Copy the prompt below
2. Paste into ChatGPT/Claude/Copilot
3. Copy the code
4. Paste into `report.py`
5. Test: See instructions below

**PROMPT TO GIVE AI:**

```
Create a Python module called report.py to format analysis results for display.

Requirements:

1. Create function: format_report(analysis_result: dict, email_file: str = None) -> str
   - Takes dict from analyze_email() function
   - Takes optional email filename
   - Returns formatted report as string (for printing)

2. Report structure and content:
   
   HEADER SECTION:
   PHISHING ANALYSIS REPORT
   ========================
   File: [filename if provided]
   Risk Level: [HIGH/MEDIUM/LOW] ([score]/10)
   
   INDICATORS SECTION:
   DETECTED INDICATORS:
   - [indicator 1]
   - [indicator 2]
   ...
   
   EXPLANATIONS SECTION:
   WHY THIS MATTERS:
   - [why indicator 1 matters]
   - [why indicator 2 matters]
   ...
   
   RECOMMENDATIONS SECTION:
   RECOMMENDATIONS:
   - Check sender domain carefully
   - [specific recommendation based on detected indicators]
   ...

3. Risk-specific recommendations:
   
   If HIGH risk:
   - "Do not click links or download attachments"
   - "Report to security team immediately"
   - "Delete email or forward to spam"
   
   If MEDIUM risk:
   - "Verify through official channel before interacting"
   - "Check sender domain in email headers"
   
   If LOW risk:
   - "Likely safe but exercise caution"
   - "Verify unexpected requests through official channels"

4. Formatting rules:
   - Use dashes as separators (no colors, just text)
   - Clear section headers with underlines
   - Indent bullet points with "- " prefix
   - Plain text format (no markdown, no colors, no special formatting)
   - 40-60 lines total

5. Error handling:
   If analysis_result is invalid or missing fields:
   Return error message: "Error: Invalid analysis result format"

6. Example output (what it should look like):

   PHISHING ANALYSIS REPORT
   ========================
   File: phishing_example.txt
   Risk Level: HIGH (8.5/10)

   DETECTED INDICATORS:
   - Sender spoofing (goog1e.com)
   - Urgency language (24 hours, REVOKED)
   - Link mismatch (domain doesn't match sender)

   WHY THIS MATTERS:
   - Spoofing exploits user inattention
   - Urgency bypasses critical thinking
   - Link mismatch is signature of phishing

   RECOMMENDATIONS:
   - Do not click links or download attachments
   - Report to security team immediately
   - Check sender domain in email headers

Add docstring with examples.
Use only stdlib.
Plain text output (caller will add colors).
```

**After AI generates:**
- Save to `report.py`
- Test it:
  ```bash
  python3 << 'EOF'
from analysis import analyze_email
from report import format_report

email = open('test_data/phishing_example.txt').read()
result = analyze_email(email)
report = format_report(result, 'phishing_example.txt')
print(report)
EOF
  ```
- Should print formatted report
- If works, move to final component

---

### 3.7 COMPONENT 7: Main Entry Point

**What to do:**
1. Copy the prompt below
2. Paste into ChatGPT/Claude/Copilot
3. Copy the code
4. Paste into `main.py`
5. Test: All commands should work

**PROMPT TO GIVE AI:**

```
Create main.py as the entry point for the phishing analysis tool.

Requirements:

1. Imports:
   - sys
   - argparse
   - All custom modules: cli, analysis, templates, report, ui, prompt_logger

2. Create function: main()
   - No parameters
   
   Logic:
   a) Print banner from ui.create_banner()
   
   b) Parse arguments using cli.setup_parser()
   
   c) If no arguments provided, print help and exit
   
   d) Handle each argument type:
      
      --analyze [file]:
      - Check if file exists using cli.validate_file_path()
      - If not exists: print error "File not found: [file]", return
      - Read file content
      - Call analysis.analyze_email(content)
      - Call report.format_report(result, file)
      - Print the report
      
      --analyze-url [url]:
      - For now, print placeholder: "URL analysis coming soon: [url]"
      - (This would need separate URL analysis logic)
      
      --generate-template [tactic]:
      - Check if tactic is valid
      - Call templates.generate_template(tactic)
      - Print the template
      
      --interactive:
      - Call cli.handle_interactive_menu()
      - This shows menu and handles user interaction

3. Error handling:
   - Wrap main() in try-except
   - Catch any exceptions
   - Print error message: "Error: [exception message]"
   - Exit gracefully (sys.exit(1))

4. Main execution guard:
   if __name__ == "__main__":
       main()

Add docstring explaining what main.py does.
Use only stdlib + the custom modules you created.
All error handling should print user-friendly messages.
Use ui module for colored output where appropriate.
```

**After AI generates:**
- Save to `main.py`
- Test EVERY command:
  ```bash
  # Test help
  python3 main.py --help
  
  # Test interactive menu (type "5" to exit)
  python3 main.py --interactive
  
  # Test email analysis (high-risk)
  python3 main.py --analyze test_data/phishing_example.txt
  
  # Test email analysis (low-risk)
  python3 main.py --analyze test_data/legitimate_example.txt
  
  # Test template generation
  python3 main.py --generate-template spoofing
  python3 main.py --generate-template typosquatting
  python3 main.py --generate-template urgency
  
  # Test error handling (file not found)
  python3 main.py --analyze nonexistent.txt
  ```

All should work without crashing.

---

## PART 4: DOCUMENTING YOUR WORK

### 4.1 Log Every AI Prompt

For each component you built, add an entry to `prompts_journal/PROMPT_LOG.md`

Template entry:

```markdown
## Prompt #[number]: [Component Name]

**Date:** [today]
**AI Tool:** [ChatGPT / Claude / Copilot]

**What I Asked:**
[Paste the exact prompt you gave to AI]

**Code File:** [filename.py]

**What I Modified:**
- [Change 1 and why you made it]
- [Change 2 and why you made it]
- [Add at least 2 modifications]

**How I Tested:**
python3 [test command]
Result: [what happened]

**Status:** Complete
```

### 4.2 Add Code Comments

In each Python file, add comments explaining YOUR understanding:

Example in analysis.py:

```python
def check_sender_spoofing(email_text: str) -> dict:
    """Check if sender domain looks spoofed."""
    
    # Original AI code didn't catch single-letter substitutions
    # I added goog1e, amaz0n patterns to improve detection
    
    typosquats = {
        'goog1e.com': 'google.com',
        'amaz0n.com': 'amazon.com',
        # ... etc
    }
    
    # This catches the most common phishing tricks
```

---

## PART 5: FINAL VERIFICATION CHECKLIST

Before you're done, verify everything works:

- [ ] `python3 main.py --help` - Shows help text
- [ ] `python3 main.py --interactive` - Shows menu, exit with option 5
- [ ] `python3 main.py --analyze test_data/phishing_example.txt` - Shows HIGH risk report
- [ ] `python3 main.py --analyze test_data/legitimate_example.txt` - Shows LOW risk report
- [ ] `python3 main.py --generate-template spoofing` - Shows spoofing template
- [ ] `python3 main.py --generate-template typosquatting` - Shows typosquatting template
- [ ] `python3 main.py --generate-template urgency` - Shows urgency template
- [ ] Terminal shows colorful output (cyan, red, yellow, green)
- [ ] Banner shows fish on hook ASCII art
- [ ] prompts_journal/PROMPT_LOG.md has 7 entries (one per component)
- [ ] All Python files have docstrings
- [ ] All Python files have comments explaining your modifications
- [ ] No errors when running any command

---

## WHAT YOU'VE BUILT

A complete phishing analysis CLI tool with:

- Colorful terminal UI with fish/hook ASCII art theme
- Email analysis for phishing indicators (spoofing, urgency, link mismatches)
- Educational templates showing how phishing attacks work
- Formatted reports explaining what each indicator means
- Automatic prompt logging to prove you used AI and documented modifications
- Test data to verify it works
- Professional error handling

This meets all assignment requirements:
- Runs in Codespaces
- Has interactive CLI features
- Uses AI for 7+ components
- Documents meaningful modifications

---

## NEXT STEPS

1. Setup environment (Part 1)
2. Create test data (Part 2)
3. Build each component in order (Part 3)
4. Test each component immediately after building
5. Document your work (Part 4)
6. Run final verification (Part 5)

When you're done, you'll have a working tool and proof of your understanding.

Good luck!
