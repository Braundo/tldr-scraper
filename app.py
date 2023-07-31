from flask import Flask, render_template
import os
import requests
import datetime
from bs4 import BeautifulSoup
import atexit
import re

app = Flask(__name__)

def is_weekend():
    # Get the current day of the week (0: Monday, 6: Sunday)
    today = datetime.datetime.now().weekday()
    # Check if it's a weekend (Saturday or Sunday)
    return today == 5 or today == 6

def get_latest_friday():
    # Get today's date
    today = datetime.date.today()
    # Calculate the difference in days from the current day to the last Friday (weekday 4)
    days_until_friday = (today.weekday() - 4) % 7
    # Subtract the difference to get the last Friday's date
    last_friday = today - datetime.timedelta(days=days_until_friday)
    return last_friday

def generate_links_html():
    if is_weekend():
        # If today is a weekend, use the most recent Friday's date
        date = get_latest_friday().strftime("%Y-%m-%d")
    else:
        # Use today's date
        date = datetime.date.today().strftime("%Y-%m-%d")

    urls = ["https://tldr.tech/tech", "https://tldr.tech/ai", "https://tldr.tech/webdev"]  # Add the new URL here
    links = []

    for url in urls:
        response = requests.get(f"{url}/{date}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            for link in soup.find_all("a", class_="font-bold"):
                headline = link.text.strip()
                # Check for (x minute read) in the headline and extract time_to_read
                match = re.search(r"\((\d+) minute read\)", headline)
                if match:
                    time_to_read = match.group(1)
                    headline = headline.replace(match.group(0), "").strip()
                else:
                    time_to_read = None

                # Skip articles with the text "(Sponsor)"
                if "(Sponsor)" not in headline:
                    links.append((headline, time_to_read, link["href"]))
        else:
            return None

    return date, links

@app.route('/')
def index():
    links_html = generate_links_html()
    if links_html:
        date, links = links_html
        with open(f"{date}_links.txt", "w") as file:
            for headline, time_to_read, url in links:
                file.write(f"{headline}: {url}\n")
        return render_template("index.html", date=date, links=links, dark_mode=True)
    else:
        return "Failed to fetch data."

def delete_text_files():
    links_html = generate_links_html()
    if links_html:
        date, _ = links_html
        try:
            os.remove(f"{date}_links.txt")
        except FileNotFoundError:
            pass


atexit.register(delete_text_files)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
