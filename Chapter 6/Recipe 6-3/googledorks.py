import requests
import time

# Google Custom Search JSON API configuration
API_KEY = 'YOUR_GOOGLE_API_KEY'
CSE_ID = 'YOUR_CUSTOM_SEARCH_ENGINE_ID'
SEARCH_URL = "https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cse_id}"

# List of Google dorks
dorks = [
    'site:example.com filetype:pdf',
    'intitle:"index of" site:example.com',
    'inurl:admin site:example.com',
    'filetype:sql site:example.com',
    # ... add other dorks here ...
]

def get_search_results(query):
    """Fetch the Google search results."""
    response = requests.get(SEARCH_URL.format(query=query, api_key=API_KEY, cse_id=CSE_ID))
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code)
        return {}

def main():
    with open("dork_results.txt", "a") as outfile:
        for dork in dorks:
            print(f"Running dork: {dork}")
            results = get_search_results(dork)
            
            if 'items' in results:
                for item in results['items']:
                    print(item['title'])
                    print(item['link'])
                    outfile.write(item['title'] + "\n")
                    outfile.write(item['link'] + "\n")
                    outfile.write("-" * 50 + "\n")
            else:
                print("No results found or reached API limit!")
            
            # To not hit the rate limit, introduce a delay between requests
            time.sleep(20)

if __name__ == '__main__':
    main()
