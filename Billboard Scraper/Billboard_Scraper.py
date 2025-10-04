import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
# Import the csv module for file output
import csv 

def scrape_billboard_artists():
    """
    Opens the Billboard Year-End Hot 100 category page, finds all list links,
    scrapes the artist names from each list, removes duplicates, sorts them,
    and saves the final list to a CSV file.
    """
    # The base URL for the Wikipedia category page (using the non-mobile version
    # for more stable HTML structure, though the mobile URL provided also works).
    category_url = "https://en.wikipedia.org/wiki/Category:Lists_of_Billboard_Year-End_Hot_100_singles"
    base_wiki_url = "https://en.wikipedia.org"
    
    # --- FIX START: Add a User-Agent header to avoid 403 Forbidden errors ---
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    # ------------------------------------------------------------------------
    
    # A set is used to automatically handle duplicate artist names.
    all_artists = set()
    
    print(f"Starting scraping process from: {category_url}")
    
    try:
        # Step 1: Fetch the category page content (now including HEADERS)
        response = requests.get(category_url, timeout=10, headers=HEADERS)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Selectors to find all links to the yearly/range lists
        # These links are typically found within the 'mw-category-group' divisions.
        category_links = soup.select('div.mw-category-group a')
        
        if not category_links:
            print("Error: Could not find any list links on the category page.")
            return

        print(f"Found {len(category_links)} link(s) to year-end lists.")
        
        # Step 2: Iterate through each year/range list link
        for link in category_links:
            relative_url = link.get('href')
            if relative_url and relative_url.startswith('/wiki/'):
                list_url = urljoin(base_wiki_url, relative_url)
                page_title = link.get('title')
                print(f"\n-> Processing page: {page_title} ({list_url})")
                
                try:
                    # Fetch the content of the list page (now including HEADERS)
                    list_response = requests.get(list_url, timeout=10, headers=HEADERS)
                    list_response.raise_for_status()
                    list_soup = BeautifulSoup(list_response.content, 'html.parser')
                    
                    # Step 3: Find tables and extract artist names
                    # We look for tables with the class 'wikitable'
                    tables = list_soup.find_all('table', {'class': 'wikitable'})
                    
                    if not tables:
                        print("Warning: No 'wikitable' found on this page.")
                        continue
                        
                    artists_on_page = set()
                    
                    for table in tables:
                        # Find all rows in the table body (excluding header rows)
                        rows = table.find_all('tr')[1:] 
                        
                        for row in rows:
                            # Get all data cells (td) in the row
                            cells = row.find_all('td')
                            
                            # Standard Billboard lists usually have 'Rank', 'Title', 'Artist'
                            # The Artist name is typically in the 3rd column (index 2)
                            if len(cells) > 2:
                                # Get the text from the 3rd cell (index 2)
                                artist_cell = cells[2]
                                artist_name = artist_cell.get_text(strip=True)
                                
                                # Clean up common reference markers (e.g., [A], [1])
                                # and potential trailing spaces/newlines
                                cleaned_artist = re.sub(r'\[\w+\]|\n', '', artist_name).strip()
                                
                                if cleaned_artist:
                                    artists_on_page.add(cleaned_artist)

                    print(f"  Extracted {len(artists_on_page)} unique artists from this page.")
                    all_artists.update(artists_on_page)
                    
                except requests.RequestException as e:
                    print(f"Error fetching list URL {list_url}: {e}")
                    
    except requests.RequestException as e:
        # Check if the error is specifically 403, and provide a helpful message.
        if "403 Client Error: Forbidden" in str(e):
             print(f"\nFatal Error: The request was blocked (403 Forbidden).")
             print("This usually happens when a website detects scraping.")
             print("We added a 'User-Agent' header to the requests to fix this, please try running again!")
        else:
            print(f"Fatal Error fetching category URL {category_url}: {e}")
        return
        
    # Step 4 & 5: Process the final list
    
    # Convert the set back to a list
    final_artists_list = list(all_artists)
    
    # Sort the list alphabetically
    final_artists_list.sort()
    
    print("\n" + "="*50)
    print(f"Processing Complete. Total Unique Artists Found: {len(final_artists_list)}")
    print("="*50)
    
    # Step 6: Print the result -> NOW SAVE TO CSV
    output_filename = "billboard_artists.csv"
    
    try:
        # Open the file for writing ('w'), ensuring no extra blank rows (newline='')
        with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            
            # Write the header row
            csv_writer.writerow(['Unique Artist Name'])
            
            # Write each artist name as a new row
            for artist in final_artists_list:
                csv_writer.writerow([artist])
                
        print(f"\nSuccessfully saved {len(final_artists_list)} unique artists to '{output_filename}'")

    except IOError as e:
        print(f"\nError writing to CSV file '{output_filename}': {e}")


if __name__ == "__main__":
    scrape_billboard_artists()
