# arxiv-summaries-workflow

This repo is public access to what I use to automate my [monthly arxiv paper skimming series](https://youtube.com/playlist?list=PLPefVKO3tDxP7iFzaSOkOZnXQ4Bkhi9YB&si=J0Rmcmy-oVyAZI7I) on youtube. I don't think anybody will really find a majority of these files useful but who knows. 

if you're looking to see the backlog of papers i've looked into each week in my videos, then check out the following two files:
- `papers_downloaded.csv`: includes every single paper that has shown up on the weekly paper videos since 2024/06/21. From reading the abstracts of these papers I selected which papers would make their way into the following file
- `papers_kept.csv`: includes every single paper that has shown up on the [monthly substack newsletter/podcast](https://evintunador.substack.com) since 2024/06/21. These are the papers that I actually bother starting to read, some percentage of which get deleted part of the way through, some get read but never discussed again, and some get read & talked about on the channel in one of my [paper breakdown videos](https://www.youtube.com/playlist?list=PLPefVKO3tDxMah1lcs9J43Q9xajehA023)

## Repo Contents

- `arxiv-link-downloader.py` - this script takes as input any number of arxiv links and downloads them as well as adds them to `links.txt`, `papers_seen.csv` and `papers_downloaded.csv`
- `arxiv-search.py` - this script opens up an app window with a list of paper titles and allows you to download these papers into `pdfs/` with the click of a button. It selects them according to search criteria specified in `config.py`; by default the search terms are ones that I prefer and it shows you the most recent papers you've not yet seen with a cap at 2000 total (i don't recommend sifting through that many in one sitting, it's mind-numbing). Whenever this is run to completion every single paper in the list gets added to `papers_seen.csv`. Whenever you download a file the script writes the ArXiv link into `links.txt` for use later and a bunch of info into `papers_downloaded.csv` in the hopes that i'll one day be able to train a model to select papers for me using these two csv files.
- `cleanup.py` - this will take any pdf files in `pdfs-to-summarize/` and send them along with corresponding .md files to your obsidian vault if you have that enabled in `config.py`. You need to specify the location of your obsidian vault in `config.py` in order for it to work. When sending files to obsidian, it also records the fact that you decided to keep them by adding lines to `papers_kept.csv`; if you want to use that csv but don't want to use obsidian then hop into `config.py` to change that setting. Finally, it deletes all of the files that are generated by all the other scripts.
- `config.py` - Where you can change a couple settings if you'd like. 
- `newsletter-podcast.py` - this will consume all PDFs in the `pdfs-to-summarize/` folder and use OpenAI's API to generate summaries which will go into `newsletter.txt`. It then turns this newsletter into an mp3 file for a podcast using OpenAI's TTS. You need to create a file `key_openai.txt` and paste in your individual (not organization) OpenAI API key in order for this to work
- `recording.py` - this file handles everything that happens during the actual video recordings. 
    1. Running it begins the hotkey listener
    2. Hitting the primary hotkey ("[" by default) the first time begins a timer, opens the link from the first line of `links.txt` in your default browser, and writes and writes the first timestamp to `timestamps.txt`
    3. Hitting the hotkey any following time both records the next timestamp and opens the next link
        - *note:* In `timestamps.txt` common phrases (such as "Neural Network") are shortened to acronyms (eg "NN"). Add/remove phrases in `config.py`. Delete all phrases from the config to remove this functionality
    4. Hitting the delete_hotkey ("]" by default) deletes the previously written timestamp. This is very useful in conjunction with the automatic video silence remover from my [auto-video-editing-suite](https://github.com/evintunador/auto-video-editing-suite) as it allows me to not include a given paper in the video if i get to it and find it to be boring
    5. Hit `Esc` to end the timer and script
- `timestamp_trimmer.py` - this will trim lines until they get below a specified character count (4,500 by default; Youtube's max description length is 5,000 characters) prioritizing those which have the shortest time length to be trimmed first
- `papers_seen.csv` - includes every single paper that had its title pass in front of my eyes BEFORE the weekly abstract reading video; this is basically every single paper that gets published to arxiv under the AI category and every tangentially related category. From reading these titles I use `arxiv-search.py` to select which papers will go in the following file
- `papers_downloaded.csv` - includes every single paper that has shown up on the [monthly paper videos](https://www.youtube.com/playlist?list=PLPefVKO3tDxP7iFzaSOkOZnXQ4Bkhi9YB) since 2024/06/21. From reading the abstracts of these papers I selected which papers would make their way into the following file by moving them into `pdfs-to-summarize/` during the video
- `papers_kept.csv` - includes every single paper that has shown up on the [monthly substack newsletter/podcast](https://evintunador.substack.com) since 2024/06/21. These are the papers that I actually bother starting to read, some percentage of which get deleted part of the way through, some read but never discussed again, and some read & talked about on the channel in one of my [paper breakdown videos](https://www.youtube.com/playlist?list=PLPefVKO3tDxMah1lcs9J43Q9xajehA023)

## SETUP

1. Clone the repository to your local machine.
2. Create a virtual environment and install the required Python packages by running `pip install -r requirements.txt`
3. Obtain an API key from OpenAI and save it in a file named `key_openai.txt` in the root directory of the repository.
4. Run `cleanup.py` to get rid of all the pdf and text files that I may or may not have left in here by accident on the most recent push. I'd also recommend deleting `papers_seen.csv`, `papers_downloaded.csv`, and `papers_kept.csv` assuming you plan to use them to train your own custom recommendation model like I do one day and don't want my data confounding yours.
5. If you don't use obsidian then open `config.py` and set `send-to-obsidian = False`. If you plan to send files to an Obsidian vault then open `config.py` and define directories for `your/obsidian/vault/location/here` and `your/obsidian/vault/location/here/attachments-folder`. If you robsidian vault location and the attachments location are the same then just set them both as the same. Also inside `config.py` you can edit `frontmatter_lines` to fit your own tagging system. By default the first line after the tags will be a link to the file and you'd have to jump into `cleanup.py` to change that
6. Maybe peruse `config.py` to check settings and try to gain a better understanding of this monstrocity I've created

## USAGE

1. Write out your search terms in `search_terms_include.txt` and `search_terms_exclude.txt` to fit your use-case. Each search term should be on its own line. If you just want all of today's newest papers then leave both blank. For me personally I exclude papers that I know I'm not going to be interested in, for example anything related to the medical field. Also by default it will only downloads papers published after the date in `most_recent_day_searched.txt` but if you'd like to disable that then open up `config.py` and set `restrict_to_most_recent = False`. 
2. Run `arxiv-search.py`, wait for it to finish printing out every title and link to console, and then it should create a little app window. Drag expand this window and then you'll see a bunch of buttons with names of papers. Click on a paper and it'll be downloaded to `pdfs/`
    - If no papers show up and you get a blank window that's either because
        - the arXiv API wrapper is bugging out. Just run it a couple times until it works, preferably waiting at least 15 minutes if not an hour between attempts
        - the conditions of your search are such that no results have returned. Try removing lines from `search_terms_exclude.txt`, adding terms to `search_terms_include.txt`, changing `most_recent_day_searched.txt` to an earlier date, or adjusting the `restrict_to_most_recent`, `max_results`, or `categories` variables in `config.py`.
3. Run `recording.py` and the link to the first paper in `links.txt` will open up in your default browser
    3b. Once you're ready to record, hit record and the primary hotkey ("[" by default but configurable in `config.py`) at the same time which will start the timer, record the first timestamp, and open the first link
    3c. Every successive hit of the primary hotkey will both open the corresponding links and record the timestamp
    3d. If you hit the `delete_hotkey` ("]" by default) then the recently recorded timestamp will be deleted
    3e. Hit `Esc` to end the script
4. If `timestamps.txt` is too long to fit into Youtube's description, run `timestamp_trimmer.py`
5. Run the `newsletter-podcast.py` script to generate a `newsletter.txt` and `podcast.mp3` based on all the pdf files in `pdfs-to-summarize/`. Basically it has chatGPT summarize the paper and then OpenAI's TTS model read that summary to create the podcast; look in `config.py` to adjust the prompt. I assumed that during step 3 you were dropping every pdf file you wanted to read into that folder
6. Once you're finished run `cleanup.py`. This will send the pdfs in `pdfs-to-summarize/` to your obsidian vault and create corresponding markdown notes for them, and then delete all files created by the previous scripts to clean up the repo

## Potential TODOs
- [ ] over-engineer arxiv-search.py to make it easier for me to go long periods of time without checking papers
- [ ] train a model (BERT based?) off of `papers_seen.csv`, `papers_downloaded.csv`, and `papers_kept.csv` to automatically grab for me the papers that i find interesing in a given week rather than having to read through the boring list myself