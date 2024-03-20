import requests
from bs4 import BeautifulSoup
from langchain.document_loaders import GitbookLoader
# enter a gitbook URL
start_url = "GITBOOK_URL" 
loader = GitbookLoader(start_url, load_all_paths=True)

def scrape_and_follow_next(start_url, all_pages_data=[]):
    """Scrapes a page, appends content, and follows the 'Next' link."""
    response = requests.get(start_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find and extract content (adjust selectors as needed)
    content_div = soup.find('main', class_='flex-1 relative py-8 lg:px-12 break-anywhere page-api-block:xl:max-2xl:pr-0 page-api-block:max-w-[1654px] page-api-block:mx-auto') 
    if content_div:
        page_content = content_div.text
        all_pages_data.append(page_content)
        print(f"Found content")

    # Find the "Next" page link (adjust selectors as needed)
    next_page_link = soup.select_one('a:contains("Next")')  
    if next_page_link:
        next_page_url = loader.base_url + next_page_link['href']
        print(f"Next page: {next_page_url}")
        scrape_and_follow_next(next_page_url, all_pages_data)

# Start scraping
all_pages_data = []
 
scrape_and_follow_next(start_url, all_pages_data)

# Combine content from all pages
combined_content = '\n'.join(all_pages_data)

# Extract page name from the base URL
page_name = loader.base_url.rsplit('/', 1)[-1]

# Create the filename 
filename = f"{page_name}.md"

# Save the content to a markdown file
with open(filename, 'w', encoding='utf-8') as file:
    file.write(combined_content)

print(f"Page content saved to {filename}")
