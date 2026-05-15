# AI Prompt Journal

Daniel Santos: You had a vague AI workshop project. I challenged assumptions to uncover the real requirements: build a Python application using AI assistance, with documented code modifications and evidence you understand it.
We landed on a Phishing Analysis Tool (CLI in GitHub Codespaces) because it:

Fits cybersecurity major
Avoids GUI complexity for group work
Is safely defensible
Impresses graders

I created one comprehensive instruction file with:

7 copy-paste prompts for AI
Setup steps
Test data
Documentation framework
Verification checklist

Used claude to build me instruction for copilot

verison 1.0.0

# 1st Prompt

Daniel Santos: 

right we need to clean up all useless code and duplicates first then we need to create a seprate menu for each option, for option 1 anazyle email file i need to to list out the file in test_data and number then which ever file is selected then anazlye that file and generate report which you will save to a new folder called reports reports will store all reports and when option 4 view recent reports is selected then list those reports and number them. when option2 is selected open a new menu which take a url input and checks its for scam then generate report and add to reports folder. 


1.1.0

# 2nd Prompt

daniel santos 

we need to imprement a way to allow the user the test there own emails from there own mail clients


1.1.1

# 3rd Prompt

daniel santos

update the ui logo to these lines strcitly,  make a gradeint of red to yellow across the logo and make sure its centered with in the teminal

1.1.2

# 4th Prompt

daniel santos 

not a good enough gradient each line needs to be a diffrent shade, also the logo need to be push left by a few tabs also leave a spcae at the top by two line

1.1.3

# 5th Prompt

Daniel Santos 

we need to implement a way to check URL secuirty in a reliable way can we Accept a domain name (for example, google.com)
Perform a DNS lookup
Show whether the domain can be resolved
Optionally display the resolved IP address. if they dont match the real companies dns then we can call it a scam also if theres any special charecters also flag it as a risk the should also show the real ip and real website url ready to copy and paste 


1.2.0

# 6th Prompt


Daniel Santos 

We should use colour to mark risk level with each report when the create the report file for each rerport the risk level line should be highlighted in a colour depending on the integer so anything below or equal to 2 should be red, then 3-4 should be orange, 5- 6 should be yellow 7-8 chiuld be blue 9-10 should be green 

1.2.1

# 7th Prompt

daniel santos 

next we have two report folders where reports are stored fix this by gettinf rid of one and fixing pathing, i want a delete option when in the view recent report menu like a delte all of select which to delte and then you can select which reports to delte, also the analyze email needs to be more stream line keep anaylzing emails to one option it should take egenrated emails and a users own emails, rename test_data to DROP_EMAILS_HERE, for some reason the colours for risk level are not working in the view recent reports menu but are working in the anaylze email file and analylize URL so check why and fix, 

version 1.3.0


# 8th Prompt

daniel santos

ok good now recheck all file and folder to check for any usless code that is not being used or is extra to improve preformace but dont dont get rid of any crucial code or code that will collpase the build, create a readme file with specific and straigh foward instructions or how to add this to your own computer / customers computer explain each featue and how to use, provide spaces for screen shots, provide instructions for linuxmac and windowns, include version author = owner of repo, we are on version 1.3.1

version 1.3.1


# 9th Prompt

daniel santos


# 10th Prompt

Jonathan Bam

Read the README and make it work on my machine and give me the command to run the program

# 11th Prompt

Jonathan Bam

i want a simple config system so we don’t hardcode everything. create a config file (like config.json or .env) where we can set things like: default reports folder name, logs folder name, risk thresholds, and any api keys if we add them later. update the code so it reads from this config at startup and falls back to safe defaults if the file is missing or broken. document each config option in the readme so someone new can customize the tool without touching the code.


# 12th Prompt

Jonathan Bam

Add new tactic types to the generate_template function in templates.py: 
'pretexting', 'vishing', and 'smishing'. Follow the exact same format 
as the existing tactics with EDUCATIONAL TEMPLATE header, examples, 
explanation, and defense sections.


# 13th Prompt

Jonathan Bam

Improve the generate_template function to validate inputs more robustly. 
Strip whitespace, raise a ValueError with a helpful message for unknown 
tactics instead of returning an error string, and add a get_supported_tactics() 
helper function that returns a list of all valid tactic names.


# 14th Prompt

Jonathan Bam

Add a list_generated_templates() function to templates.py that scans the 
GENERATED_EMAILS directory and returns a list of saved template filenames 
with their creation timestamps, sorted newest first.

# 15th Prompt

Jonathan Bam

Refactor the save block in generate_template to avoid filename collisions 
by checking if the file already exists before writing, and use local 
timezone instead of UTC in the timestamp.