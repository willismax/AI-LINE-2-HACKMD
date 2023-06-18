import requests
from bs4 import BeautifulSoup
from PyHackMD import API
import pyimgur
import datetime

# from config import (
#     HACKMD_API_TOKEN, TODO_NOTE_ID, TEMP_NOTE_ID, IMGUR_CLIENT_ID, TEMP_NOTE_ID, AI_NOTE_ID
# ) 
import openai
# from config import OPENAI_API_KEY

def extract_url_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("h1")
    first_subtitle = soup.find("h2")
    first_paragraph = soup.find("p")

    if title:
        title = title.text
    if first_subtitle:
        first_subtitle = first_subtitle.text
    if first_paragraph:
        first_paragraph = first_paragraph.text

    return title, first_subtitle, first_paragraph


#TODO
# def generate_content_summary_and_hashtags(content, openai_api_key):
#     openai = OpenAI(api_key=openai.api_key)

#     # Generate summary
#     summary = "This is an example summary."

#     # Extract hashtags
#     hashtags = ["#example1", "#example2"]

#     return summary, hashtags

#TODO    
# def process_summary_and_create_hackmd(url, title, first_subtitle, first_paragraph, summary, hashtags):
#     # Create new HackMD note
#     api = API(HACKMD_API_TOKEN)
#     summary_title = f"{title} - {first_subtitle}"
#     summary_content = f"# {summary_title}\n\n{summary}\n\n[原文連結]({url})\n\n{' '.join(hashtags)}"

#     new_note = api.create_note(summary_content)
#     api.update_note(new_note['noteId'], summary_title)

#     # Add the new note to the corresponding hashtag HackMD files
#     for hashtag in hashtags:
#         list_page_note = api.get_note_by_title(hashtag)

#         if not list_page_note:
#             list_page_content = f"# {hashtag}\n\n"
#             list_page_note = hackmd_api.create_new_note(list_page_content)
#             hackmd_api.update_note_title(list_page_note['noteId'], hashtag)

#         list_page_content = hackmd_api.get_note_content(list_page_note['noteId'])
#         list_page_content += f"- [{summary_title}]({new_note['noteUrl']})\n"
#         hackmd_api.update_note_content(list_page_note['noteId'], list_page_content)

#     return new_note