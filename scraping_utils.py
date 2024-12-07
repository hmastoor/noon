import requests
from bs4 import BeautifulSoup
import json
from llm_utils_groq import get_embedding  # Your existing embedding function


def parse_page(url: str) -> str:
    """
    Parse the content of a web page and extract its text.

    Args:
        url (str): The URL of the web page to parse.

    Returns:
        str: The extracted and cleaned text content of the web page.

    Raises:
        requests.RequestException: If there's an error fetching the page.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url.strip(), headers=headers) 
        # Check for authorization error
        if response.status_code == 403 or 'You are not authorized' in response.text:
            print(f"Skipping {url} due to authorization error.")
            return None  # skip that page

        response.raise_for_status()  # Raise an exception for bad status codes

        soup = BeautifulSoup(response.content, 'lxml')

        # Clean the HTML content by removing scripts, styles, and other unwanted elements
        for script in soup(['script', 'style']):
            script.decompose()  # remove the tags and their content

        # Extract clean text from the body
        clean_text = soup.body.get_text(separator=' ', strip=True)
        
        return clean_text

    except requests.RequestException as e:
        raise requests.RequestException(f"Error fetching the page {url}: {e}")


def process_lawyer_profiles(csv_file: str, output_file: str = 'lawyer_profiles.json'):
    """
    Process a list of lawyer URLs from a CSV file, parse their profiles, clean the text, and store the results in a JSON file.

    Args:
        csv_file (str): The path to the CSV file containing lawyer URLs.
        output_file (str): The path to the output JSON file.
    """
    profiles = []

    # Read URLs from the CSV file
    with open(csv_file, 'r') as file:
        lawyer_urls = file.readlines()

    for url in lawyer_urls:
        profile_text = parse_page(url.strip())
        if profile_text:
            profiles.append({
                'url': url.strip(),
                'profile_text': profile_text
            })

    # Save the cleaned profiles to a JSON file
    with open(output_file, 'w') as json_file:
        json.dump(profiles, json_file, indent=4)
    print(f"Profiles have been saved to {output_file}")


process_lawyer_profiles('lawyers.csv')


def process_lawyer_profiles_with_embeddings(csv_file='lawyers.csv'):
    """
    Pre-process lawyer profiles, generate embeddings, and store them in a JSON file.

    Args:
        csv_file (str): Path to the CSV file containing lawyer profile URLs.

    Returns:
        None
    """
    lawyer_profiles = []
    
    # Read the CSV file with lawyer URLs
    with open(csv_file, 'r') as f:
        lawyer_urls = [line.strip() for line in f.readlines()]
    
    for url in lawyer_urls:
        try:
            # Fetch the profile text for the current URL
            profile_text = parse_page(url)
            
            if profile_text:
                # Get embedding for the profile
                profile_embedding = get_embedding([profile_text])[0]
                
                # Append the profile and its embedding to the list
                lawyer_profiles.append({
                    "url": url,
                    "text": profile_text,
                    "embedding": profile_embedding
                })
            else:
                print(f"Skipping {url} due to failed parsing.")
        except Exception as e:
            print(f"Error processing {url}: {e}")

    # Store the profiles and their embeddings in a JSON file
    with open("lawyer_profiles_with_embeddings.json", "w") as f:
        json.dump(lawyer_profiles, f, indent=4)

    print(f"Processed {len(lawyer_profiles)} profiles and stored embeddings.")


# Run the function to process the profiles
process_lawyer_profiles_with_embeddings()
