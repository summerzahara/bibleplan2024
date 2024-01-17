from flask import Flask, render_template
import requests
from icecream import ic
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

url = "https://api.scripture.api.bible"
bible_id = "65eec8e0b60e656b-01"
reading = "Exodus 1-5"
api_key = os.environ["API_KEY"]


@app.route('/')
def home():  # put application's code here
    headers = {
        "api-key": api_key
    }
    bible = requests.get(f"{url}/v1/bibles/{bible_id}", headers=headers)
    bible.raise_for_status()
    data = bible.json()

    books = requests.get(f"{url}/v1/bibles/{bible_id}/books", headers=headers)
    books.raise_for_status()
    current_book = books.json()["data"]
    current_reading = reading.split(" ")
    ic(current_reading)
    for book in current_book:
        if book["name"] == current_reading[0]:
            display_book = book["name"]
            display_book_id = book["id"]
            ic(display_book, display_book_id)

    chapters = requests.get(f"{url}/v1/bibles/{bible_id}/books/{display_book_id}/chapters", headers=headers)
    chapters.raise_for_status()
    chaps = chapters.json()["data"]
    # ic(chaps)
    my_chaps = current_reading[1].split("-")
    ic(my_chaps)
    chapter_ids = []
    for chapter in chaps:
        if int(chapter["number"]) in range(int(my_chaps[0]), int(my_chaps[1])+1):
            chapter_ids.append(chapter["id"])
    ic(chapter_ids)

    chapter_text = {}

    for c_id in chapter_ids:
        text = requests.get(f"{url}/v1/bibles/{bible_id}/chapters/{c_id}", headers=headers)
        text.raise_for_status()
        display_text = text.json()["data"]
        chapter_text[f"{display_text['number']}"] = display_text["content"]
        ic(display_text["content"].split("<span>"))
    # ic(chapter_text)






    return render_template('index.html', data=data, books=current_book, to_read=current_reading, texts=chapter_text)




if __name__ == '__main__':
    app.run()
