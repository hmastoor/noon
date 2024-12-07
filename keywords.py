import csv
import json
from sklearn.feature_extraction.text import CountVectorizer
from scraping_utils import parse_page


def extract_keywords(profile_text, num_keywords=10):
    """
    Extract keywords from the lawyer profile text using a basic CountVectorizer.

    Args:
        profile_text (str): The full text of the lawyer's profile.
        num_keywords (int): Number of keywords to extract.

    Returns:
        list: List of extracted keywords.
    """
    vectorizer = CountVectorizer(stop_words='english', max_features=num_keywords)
    X = vectorizer.fit_transform([profile_text])
    keywords = vectorizer.get_feature_names_out()
    return set(keywords)


def process_lawyer_profiles_with_keywords(csv_file):
    """
    Process lawyer profiles, extract keywords, and store them in a JSON file.

    Args:
        csv_file (str): The CSV file containing lawyer profile URLs.

    Returns:
        None
    """
    lawyer_profiles = []
    
    # Read the lawyer URLs from the CSV file
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        lawyer_urls = [row[0] for row in reader]
    
    for url in lawyer_urls:
        profile_text = parse_page(url)
        if profile_text:
            keywords = extract_keywords(profile_text)
            lawyer_profiles.append({
                "url": url,
                "text": profile_text,
                "keywords": list(keywords)
            })

    # Store the profiles and their extracted keywords in a JSON file
    with open("lawyer_profiles_with_keywords.json", "w") as f:
        json.dump(lawyer_profiles, f)

    print(f"Processed {len(lawyer_profiles)} profiles and stored keywords.")


process_lawyer_profiles_with_keywords('lawyers.csv')