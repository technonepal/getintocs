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
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:  # Get top 5 from each source
            news_items.append({
                "title": entry.title,
                "link": entry.link,
                "date": entry.published if 'published' in entry else "Recent",
                "source": feed.feed.title
            })
    return news_items

def update_html(news_data):
    # Template for a single news card based on your style.css
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
    
    # Read your news.html and replace the content between markers
    with open("news.html", "r", encoding="utf-8") as f:
        content = f.read()

    # Use a placeholder in your news.html like and start_marker = "" end_marker = ""
    # Define markers
    start_marker = "<!-- START_NEWS -->"
    end_marker = "<!-- END_NEWS -->"
    
    new_content = content.split(start_marker)[0] + start_marker + cards_html + end_marker + content.split(end_marker)[1]
    
    with open("news.html", "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    data = fetch_news()

    update_html(data)
