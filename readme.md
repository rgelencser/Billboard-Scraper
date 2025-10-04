Billboard Hot 100 Artist Scraper
This Python script is designed to scrape historical data from Wikipedia to compile a complete, alphabetized list of unique artists featured on the Billboard Year-End Hot 100 singles charts.

🎯 Features
Category Scraping: Automatically finds and follows all links to yearly Hot 100 lists from the main Wikipedia category page.

Data Extraction: Extracts the artist names from the standard "wikitable" format on each yearly list.

Deduplication: Uses a Python set to ensure the final output contains only unique artist names, regardless of how many times they appear on different year-end charts.

Sorting: Presents the final list of unique artists in alphabetical order.

Robustness: Includes basic error handling for HTTP requests (network issues, page not found) and data cleaning for removing common Wikipedia reference markers (e.g., [1], [A]).

⚙️ Prerequisites
You need Python 3 installed on your system, along with the following libraries:

requests for making HTTP requests to fetch webpage content.

beautifulsoup4 (BS4) for parsing the HTML content.

🛠 Installation
Save the Code: Ensure the provided Python script is saved as billboard_artist_scraper.py.

Install Dependencies: Open your terminal or command prompt and run the following command to install the required Python libraries:

pip install requests beautifulsoup4

🚀 Usage
To run the scraper, execute the script from your terminal:

python billboard_artist_scraper.py

Output
The script will print status updates to the console as it processes each year-end list page. Once complete, it will display a summary and the final, alphabetically sorted list of unique artists:

==================================================
Processing Complete. Total Unique Artists Found: 1234
==================================================

Alphabetically Sorted List of Unique Artists:
- ABBA
- A-ha
- Aerosmith
- ...

🧠 How It Works
It sends a request to the main Wikipedia category page: Category:Lists_of_Billboard_Year-End_Hot_100_singles.

It identifies all links within the category groups that point to the individual year-end lists.

For each list link:

It fetches the page content.

It locates the main data table (wikitable).

It iterates through the table rows, targeting the third column (index 2), which typically contains the Artist name.

It cleans the extracted artist name (removing footnotes like [A] or [1]).

It adds the cleaned name to a master set (all_artists) for automatic deduplication.

Finally, the master set is converted to a list, sorted alphabetically, and printed.