from openai import OpenAI
import PyPDF2
from config import prompts
from time import time, sleep
from datetime import datetime
import os
from halo import Halo
from pathlib import Path
from pydub import AudioSegment

def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
        return infile.read()
    
def chatbot(conversation, model="gpt-3.5-turbo-16k", temperature=0.7):
    max_retry = 3
    retry = 0
    while True:
        try:
            spinner = Halo(text='Thinking...', spinner='dots')
            spinner.start()
            
            response = client.chat.completions.create(model=model, messages=conversation, temperature=temperature)
            text = response.choices[0].message.content

            spinner.stop()
            
            return text#, response['usage']['total_tokens']
        except Exception as oops:
            print(f'\n\nError communicating with OpenAI: "{oops}"')
            if 'maximum context length' in str(oops):
                a = conversation.pop(0)
                print('\n\nDEBUG: Trimming oldest message')
                continue
            retry += 1
            if retry >= max_retry:
                print(f"\n\nExiting due to excessive errors in API: {oops}")
                exit(1)
            print(f'\n\nRetrying in {2 ** (retry - 1) * 5} seconds...')
            sleep(2 ** (retry - 1) * 15)

def cut_off_string(input_string, cutoff_string):
    # Find the position of the cutoff string
    cutoff_index = input_string.find(cutoff_string)
    
    # If the cutoff string is found, slice the input string up to that point
    if cutoff_index != -1:
        return input_string[:cutoff_index + len(cutoff_string)], input_string[cutoff_index + len(cutoff_string):]
    else:
        # If the cutoff string is not found, return the original string
        # You can also choose to handle this case differently
        return input_string, ''
    
if __name__ == '__main__':
    # instantiate chatbot, variables
    SECRET_KEY = open_file('key_openai.txt').strip()
    client = OpenAI(api_key=SECRET_KEY)

    # Get today's date
    today = datetime.now().strftime('%Y-%m-%d')

    # Write the message
    with open('newsletter.txt', 'w') as outfile:
        outfile.write(f"Welcome to Tunadorable's weekly AI newsletter, where we summarize his favorite articles of the week that he plans to read."
                      f"\nThis article was written by gpt-3.5-turbo-16k on {today}.")

    # Get list of all PDF files in the input folder
    pdf_files = [f for f in os.listdir('pdfs-to-summarize/') if f.endswith('.pdf')]

    summaries = ''
    # iterate over pdf files and create summaries to add to the newsletter
    for pdf_file in pdf_files:
        # title of each summary
        summaries += f"\n\n\n\n# {pdf_file.replace('.pdf', '')}"

        # Check if the report already exists in the output folder
        filename = 'txt-summaries/' + pdf_file.replace('.pdf', '.txt')
        if os.path.exists(filename):
            continue

        # Open the PDF file
        try:
            with open('pdfs-to-summarize/' + pdf_file, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                paper = ''
                for page_num in list(range(0,len(pdf_reader.pages))):
                    page = pdf_reader.pages[page_num]
                    try:
                        paper += page.extract_text()
                    except KeyError as e:
                        print(f"Skipping page due to missing information: {e}")
                        continue  # Skip the current iteration and move to the next page
        except PyPDF2.errors.PdfReadError:
            print(f"Error reading file: {pdf_file}")
            continue
        
        # make sure it's not too long for GPT3.5's context window
        if len(paper) > 22000:
            paper = paper[0:22000]
        
        # the actual API calls
        ALL_MESSAGES = [{'role':'system', 'content': paper}]
        for p in prompts:
            ALL_MESSAGES.append({'role':'user', 'content': p})
            answer = chatbot(ALL_MESSAGES)#, tokens
            #print(answer)
            ALL_MESSAGES.append({'role':'assistant', 'content': answer})
            summaries += f'\n{answer}'

    # Write the message
    with open('newsletter.txt', 'a') as outfile:
        outfile.write(f"{summaries}\n\n\n\nThanks for reading/listening, that's all for this week."
                      f"\nPlease consider checking out Tunadorable's youtube channel where he provides commentary on the above papers."
                      f"\nhttps://youtube.com/@Tunadorable"
                      f"\n\nHere is the most up-to-date version of the python scripts I currently use to create this newsletter:"
                      f"\nhttps://github.com/evintunador/arxiv-summaries-workflow")
    
    ### now for the podcast
    # Path for saving individual MP3 files
    audio_files_path = Path(__file__).parent / "audio_files"
    audio_files_path.mkdir(exist_ok=True)

    cutoff_str = "\n\n\n\n"
    remaining_text = open_file('newsletter.txt').strip()
    segment_files = []
    first_segment = True

    while remaining_text:
        segment_text, remaining_text = cut_off_string(remaining_text, cutoff_str)
        
        if not segment_text.strip():
            continue
    
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=segment_text[:4096]
        )
        
        segment_file_path = f"audio_files/temp_segment_{len(segment_files)}.mp3"
        
        response.stream_to_file(segment_file_path)
        # Use the recommended method for streaming the response to a file
        #with response.with_streaming_response() as response_stream:
            #with open(segment_file_path, 'wb') as out_file:
                #out_file.write(response_stream.content)

        segment_files.append(segment_file_path)

        if first_segment:
            # Initialize full_audio with the first audio segment
            full_audio = AudioSegment.from_mp3(segment_file_path)
            first_segment = False
        else:
            # Concatenate the rest of the audio files
            segment_audio = AudioSegment.from_mp3(segment_file_path)
            full_audio += segment_audio

    # Save the concatenated audio
    final_audio_path = "newsletter_podcast.mp3"
    full_audio.export(final_audio_path, format="mp3")

    # Clean up the individual segment files
    for segment_file in segment_files:
        os.remove(segment_file)
