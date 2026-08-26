"""
TrendPulse - Task 1: Fetch Data from Hacker News API

This script:
1. Fetches the first 500 Hacker News top-story IDs.
2. Fetches each story's JSON details.
3. Assigns stories to one of five categories using title keywords.
4. Keeps up to 25 stories per category.
5. Saves the collected data to data/trends_YYYYMMDD.json.
"""

import json
import os
import time
from datetime import datetime

import requests


TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

HEADERS = {"User-Agent": "TrendPulse/1.0"}

CATEGORY_KEYWORDS = {
    "technology": [
        "ai", "software", "tech", "code", "computer",
        "data", "cloud", "api", "gpu", "llm"
    ],
    "worldnews": [
        "war", "government", "country", "president", "election",
        "climate", "attack", "global"
    ],
    "sports": [
        "nfl", "nba", "fifa", "sport", "game", "team",
        "player", "league", "championship"
    ],
    "science": [
        "research", "study", "space", "physics", "biology",
        "discovery", "nasa", "genome"
    ],
    "entertainment": [
        "movie", "film", "music", "netflix", "game",
        "book", "show", "award", "streaming"
    ],
}

MAX_IDS = 500
MAX_PER_CATEGORY = 25


def get_top_story_ids():
    """Fetch the first 500 top-story IDs from Hacker News."""
    try:
        response = requests.get(
            TOP_STORIES_URL,
            headers=HEADERS,
            timeout=20
        )
        response.raise_for_status()
        return response.json()[:MAX_IDS]
    except requests.RequestException as error:
        print(f"Failed to fetch top story IDs: {error}")
        return []


def get_story(story_id):
    """Fetch one Hacker News story. Return None if the request fails."""
    try:
        response = requests.get(
            ITEM_URL.format(story_id),
            headers=HEADERS,
            timeout=20
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        print(f"Failed to fetch story {story_id}: {error}")
        return None


def title_matches(title, keywords):
    """Return True when a title contains at least one category keyword."""
    title_lower = title.lower()
    return any(keyword.lower() in title_lower for keyword in keywords)


def main():
    story_ids = get_top_story_ids()

    if not story_ids:
        print("No story IDs were received. Nothing to collect.")
        return

    collected_stories = []
    used_post_ids = set()

    # Process one category at a time.
    # Sleep once per category, not after each individual story request.
    for category, keywords in CATEGORY_KEYWORDS.items():
        category_count = 0

        for story_id in story_ids:
            if category_count >= MAX_PER_CATEGORY:
                break

            if story_id in used_post_ids:
                continue

            story = get_story(story_id)

            if not story:
                continue

            if story.get("type") != "story" or not story.get("title"):
                continue

            if title_matches(story["title"], keywords):
                collected_stories.append(
                    {
                        "post_id": story.get("id"),
                        "title": story.get("title"),
                        "category": category,
                        "score": story.get("score", 0),
                        "num_comments": story.get("descendants", 0),
                        "author": story.get("by", "unknown"),
                        "collected_at": datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                    }
                )
                used_post_ids.add(story_id)
                category_count += 1

        print(f"{category}: collected {category_count} stories")
        time.sleep(2)

    os.makedirs("data", exist_ok=True)

    date_string = datetime.now().strftime("%Y%m%d")
    output_file = f"data/trends_{date_string}.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(collected_stories, file, indent=4, ensure_ascii=False)

    print(
        f"Collected {len(collected_stories)} stories. "
        f"Saved to {output_file}"
    )

    if len(collected_stories) < 100:
        print(
            "Note: Fewer than 100 matching stories were available in the "
            "current top 500 using the required keyword rules."
        )


if __name__ == "__main__":
    main()
