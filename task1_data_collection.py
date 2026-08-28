import requests
import json
import os
import time
from datetime import datetime

TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

headers = {
    "User-Agent": "TrendPulse/1.0"
}

category_keywords = {
    "technology": [
        "AI", "software", "tech", "code", "computer",
        "data", "cloud", "API", "GPU", "LLM"
    ],
    "worldnews": [
        "war", "government", "country", "president",
        "election", "climate", "attack", "global"
    ],
    "sports": [
        "NFL", "NBA", "FIFA", "sport", "game",
        "team", "player", "league", "championship"
    ],
    "science": [
        "research", "study", "space", "physics",
        "biology", "discovery", "NASA", "genome"
    ],
    "entertainment": [
        "movie", "film", "music", "Netflix",
        "game", "book", "show", "award", "streaming"
    ]
}


def fetch_top_story_ids():
    try:
        response = requests.get(
            TOP_STORIES_URL,
            headers=headers,
            timeout=20
        )
        response.raise_for_status()
        return response.json()[:500]

    except requests.RequestException as error:
        print("Failed to fetch top story IDs:", error)
        return []


def fetch_story(story_id):
    try:
        response = requests.get(
            ITEM_URL.format(story_id),
            headers=headers,
            timeout=20
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException as error:
        print(f"Failed to fetch story {story_id}: {error}")
        return None


def title_matches(title, keywords):
    title = title.lower()

    return any(
        keyword.lower() in title
        for keyword in keywords
    )


def main():

    story_ids = fetch_top_story_ids()

    if not story_ids:
        print("No story IDs found.")
        return

    # Fetch each Hacker News story only once.
    fetched_stories = []

    for story_id in story_ids:

        story = fetch_story(story_id)

        if not story:
            continue

        if story.get("type") != "story":
            continue

        if not story.get("title"):
            continue

        fetched_stories.append(story)

    print(
        f"Successfully fetched "
        f"{len(fetched_stories)} story details."
    )

    all_stories = []

    # Now group the already-fetched stories by category.
    for category, keywords in category_keywords.items():

        category_count = 0

        for story in fetched_stories:

            if category_count >= 25:
                break

            title = story.get("title", "")

            if title_matches(title, keywords):

                record = {
                    "post_id": story.get("id"),
                    "title": title,
                    "category": category,
                    "score": story.get("score", 0),
                    "num_comments": story.get(
                        "descendants", 0
                    ),
                    "author": story.get("by", "unknown"),
                    "collected_at": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                }

                all_stories.append(record)
                category_count += 1

        print(
            f"{category}: collected "
            f"{category_count} stories"
        )

        # Required by assignment:
        # one 2-second wait per category.
        time.sleep(2)

    os.makedirs("data", exist_ok=True)

    today = datetime.now().strftime("%Y%m%d")

    output_file = f"data/trends_{today}.json"

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            all_stories,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"Collected {len(all_stories)} stories. "
        f"Saved to {output_file}"
    )


if __name__ == "__main__":
    main()
