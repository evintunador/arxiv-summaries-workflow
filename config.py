### arxiv-search.py
restrict_to_most_recent = True
max_results = 1000

### generate_newsletter.py 
# Mess around with these prompts to tease out specific information you're looking for
prompts = [ # don't forget commas if you add more prompts to the list
"You are an expert scientific researcher. Please provide clear, concise descriptions and explanations of the core assertions, mechanics, results, potential critiques, and implications elucidated here. Specificity is preferred over broad or vague statements. Be concise."#,
#"You are an expert scientific researcher with a wide range of cross-disciplinary background knowledge. List all of the prerequisite knowledge required in order to understand the concepts laid out here. Please answer extremely concisely in a simple bulleted format. Entries should include both individual concepts as well as the names of disciplines and sub-disciplines. Also, please provide a complete citation for this paper to the best of your ability given the information provided. Only include a url if it is listed in the content of the paper." 
]

### cleanup.py
# Change to False if you don't use obsidian
send_to_obsidian = True
# vault_location is wherever you want the .md summaries to go, and attachments_location is wherever you want the pdf files to go
# For people who use obsidian 'correctly' this might be the exact same folder
obsidian_vault_location = '/Users/tunadorable/Vault' #'your/obsidian/vault/location/here'
obsidian_vault_attachments_location = '/Users/tunadorable/Vault/attachments' #'your/obsidian/vault/location/here/attachments-folder'
# lines to add to the beginning of each summary.md file in obsidian. I've left mine in as examples
frontmatter_lines = ['#pdf', '#needsToBeTagged', '#needsVideo', '#unread', ''] 

### timestamps.py
# True or False
# Defaults to True because when I bulk open files in safari it displays them in reverse-chronological order
display_reverse_alphabetical = True
# The hotkey used to start the next yt chapter
hotkey = 'w'
# sorry i'm not changing the end process hotkey from esc to anything else. feel free to push an update if that's a feature you want
