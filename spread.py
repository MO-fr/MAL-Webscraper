#python spread.py 

import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
# Define the URL
url = "https://myanimelist.net/anime/season"

# Open the URL and read the page content
page = urlopen(url)
html = page.read().decode("utf-8")

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Find all the anime blocks
anime_items = soup.find_all("div", class_="seasonal-anime")

anime_data = []
for item in anime_items:
    # Extract titles and URLs

    title_tag = item.find("h2", class_="h2_anime_title") or item.find("h3", class_="h3_anime_subtitle")

    if title_tag:
        title = title_tag.get_text(strip=True)
        link_tag = title_tag.find("a")
        href = link_tag['href'] if link_tag else "N/A"
    else:
        title = "N/A"
        href = "N/A"




    # Extract ratings
    ratings_fr = item.find("div", class_=[
        "scormem-item score score-label score-4",
        "scormem-item score score-label score-5",
        "scormem-item score score-label score-6",
        "scormem-item score score-label score-7",
        "scormem-item score score-label score-8",
        "scormem-item score score-label score-na"
    ])
    ratings = ratings_fr.get_text(strip=True) if ratings_fr else "Try again kiddo"

    # Extract number of members
    members_tag = item.find("div", class_="scormem-item member")
    members = members_tag.get_text(strip=True) if members_tag else "N/A"

    # Convert members count
    if "K" in members:
        members = int(float(members.replace("K", "")) * 1000)
    elif "M" in members:
        members = int(float(members.replace("M", "")) * 1000000)
    else:
        try:
            members = int(members)
        except ValueError:
            members = 0  # Default to 0 if conversion fails

    # Append the data
    anime_data.append({"Title of anime": title, "Ratings": ratings, "Members": members, "URL": href})

# Create a DataFrame
df = pd.DataFrame(anime_data)

# Save to CSV
df.to_csv("anime_season_data.csv", index=False)

# Ensure this is aligned with the rest of your code
print("Data saved to 'anime_season_data.csv'")

""""response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
print(response.text)"""
