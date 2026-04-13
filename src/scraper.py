import requests
from bs4 import BeautifulSoup

def scrape_landing_page(url):
    """Extracts high-impact DOM nodes from the target URL."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return {"error": f"Site blocked (Status: {response.status_code})"}
        
        soup = BeautifulSoup(response.content, 'html.parser')
        h1 = soup.find('h1').text.strip() if soup.find('h1') else "Welcome"
        p_text = soup.find('p').text.strip()[:200] if soup.find('p') else "Premium product."
        
        return {"headline": h1, "sub_headline": p_text, "cta_button": "Learn More"}
    except Exception as e:
        return {"error": str(e)}