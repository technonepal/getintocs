import feedparser
import os

# List of RSS feeds to pull from
FEEDS = [
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml",
    "https://news.ycombinator.com/rss"
]

def fetch_news():
    news_items = []
    for url in FEEDS:
        try:
            feed = feedparser.parse(url)
            # Check if feed has entries to avoid errors with empty feeds
            if not feed.entries:
                continue
                
            for entry in feed.entries[:5]:  # Get top 5 from each source
                news_items.append({
                    "title": entry.title,
                    "link": entry.link,
                    "date": entry.published if 'published' in entry else "Recent",
                    "source": feed.feed.title if 'title' in feed.feed else "Tech News"
                })
        except Exception as e:
            print(f"Could not fetch {url}: {e}")
            
    return news_items

def update_html(news_data):
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
    
    # Generate the HTML for all cards
    cards_html = "".join([card_template.format(**item) for item in news_data])
    
    try:
        # Read the news.html file
        with open("news.html", "r", encoding="utf-8") as f:
            content = f.read()

        # IMPORTANT: These MUST match the comments in your HTML file
        start_marker = ""
        end_marker = ""
        
        # Check if markers exist to prevent crashing
        if start_marker not in content or end_marker not in content:
            print("Error: Markers or not found in news.html")
            return

        # Split and Reassemble the file content
        before = content.split(start_marker)[0]
        after = content.split(end_marker)[1]
            
        new_content = before + start_marker + cards_html + end_marker + after
        
        # Write the updated content back to the file
        with open("news.html", "w", encoding="utf-8") as f:
            f.write(new_content)
            print("Successfully updated news.html")
            
    except Exception as e:
        print(f"An error occurred while updating the file: {e}")

if __name__ == "__main__":
    data = fetch_news()
    if data:
        update_html(data)
    else:
        print("No news data fetched.")