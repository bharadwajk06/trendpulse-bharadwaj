
import requests
import json
import os
import time
from datetime import datetime


# Hacker News API links
top_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
item_url = "https://hacker-news.firebaseio.com/v0/item/{}.json"
# Header required for API requests
headers = {"User-Agent": "TrendPulse/1.0"}
# Keywords used to identify each category
categories = {
    "technology": ["AI", "software", "tech", "code", "computer","data", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president","election", "climate", "attack", "global"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game","team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics","biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix","game", "book", "show", "award", "streaming"]}

# Step 1: Get the first 500 top story IDs
try:
    response = requests.get(top_url, headers=headers, timeout=20)
    response.raise_for_status()
    story_ids = response.json()[:500]
except requests.RequestException as error:
    print("Error getting top stories:", error)
    story_ids = []

# Step 2: Get details of each story
stories = []
for story_id in story_ids:

    try:
        response = requests.get(item_url.format(story_id),headers=headers,timeout=20)
        response.raise_for_status()
        story = response.json()
        # Keep only valid stories
        if story and story.get("type") == "story":
            stories.append(story)
    except requests.RequestException as error:
        print("Error getting story", story_id)
print("Story details fetched:", len(stories))

# Step 3: Put stories into categories
final_stories = []

for category in categories:
    count = 0
    for story in stories:
        # Maximum 25 stories in one category
        if count >= 25:
            break
        title = story.get("title", "")
        title_lower = title.lower()
        # Check whether any keyword is present in the title
        matched = False
        for keyword in categories[category]:

            if keyword.lower() in title_lower:
                matched = True
                break

        # Add matching story
        if matched:

            new_story = {"post_id": story.get("id"),"title": title,"category": category,"score": story.get("score", 0),"num_comments": story.get("descendants", 0),"author": story.get("by", "unknown"),"collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            final_stories.append(new_story)

            count = count + 1

    print(category, ":", count, "stories collected")

    # Wait 2 seconds after each category
    time.sleep(2)

# Step 4: Create the data folder
os.makedirs("data", exist_ok=True)

# Step 5: Create today's file name
today = datetime.now().strftime("%Y%m%d")

file_name = "data/trends_" + today + ".json"


# Step 6: Save stories to JSON
with open(file_name, "w", encoding="utf-8") as file:

    json.dump(final_stories,file,indent=4,ensure_ascii=False)

# Print final result
print()
print("Collected", len(final_stories), "stories.")
print("Saved to", file_name)
