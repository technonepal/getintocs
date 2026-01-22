import feedparser
import os

# List of RSS feeds to pull from
FEEDS = [
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml",
    "https://news.ycombinator.com/rss"
]

# Files to update
TARGET_FILES = ["news.html", "index.html"]

def fetch_news():
    news_items = []
    for url in FEEDS:
        try:
            feed = feedparser.parse(url)
            if not feed.entries:
                continue
            for entry in feed.entries[:3]:  # Get top 3 from each
                news_items.append({
                    "title": entry.title,
                    "link": entry.link,
                    "date": getattr(entry, "published", "Recent"), 
                    "source": getattr(feed.feed, "title", "Tech News")
                })
        except Exception as e:
            print(f"Could not fetch {url}: {e}")
    return news_items

def update_files(news_data):
    # Template for a single news card
    card_template = """
    <div class="col-md-6 col-lg-4 mb-4">
        <div class="card news-card h-100">
            <div class="card-body">
                <span class="badge bg-primary mb-2">{source}</span>
                <h5>{title}</h5>
                <p class="text-muted small">{date}</p>
                <a href="{link}" target="_blank" class="btn btn-outline-primary btn-sm">Read More</a>
            </div>
        </div>
    </div>
    """
    cards_html = "".join([card_template.format(**item) for item in news_data])
    
    start_marker ="<!-- NEWS_START -->"
    end_marker = "<!-- NEWS_END -->"

    for file_name in TARGET_FILES:
        try:
            if not os.path.exists(file_name):
                print(f"Skipping {file_name}: File not found.")
                continue

            with open(file_name, "r", encoding="utf-8") as f:
                content = f.read()

            if start_marker not in content or end_marker not in content:
                print(f"Skipping {file_name}: Markers not found.")
                continue

            before, middle = content.split(start_marker, 1)
            middle, after = middle.split(end_marker, 1)
            new_content = before + start_marker + cards_html + end_marker + after

            
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(new_content)
                print(f"Successfully updated {file_name}")

        except Exception as e:
            print(f"Error updating {file_name}: {e}")

if __name__ == "__main__":
    data = fetch_news()
    if data:
        update_files(data)

