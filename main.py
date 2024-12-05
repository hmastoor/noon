import csv
from llm_utils import llm, get_embedding
from scraping_utils import parse_page
from time import time


def passes_criterion(lawyer_url: str, query: str) -> bool:
    """
    Evaluate if a lawyer passes a given criterion based on their profile.

    Args:
        lawyer_url (str): URL of the lawyer's profile
        query (str): Criterion to evaluate against

    Returns:
        bool: True if lawyer passes the criterion, False otherwise
    """
    text = parse_page(lawyer_url)

    system_prompt = """
    You are evaluating a lawyer whether they pass a given criterion.

    Respond in the following format:
    <thinking>...</thinking>, within which you include your detailed thought process.
    <answer>...</answer>, within which you include your final answer. "Pass" or "Fail".
    """.strip()

    user_prompt = f"""
    Here is the query: {query}
    Here is the lawyer's profile: {text}
    """.strip()

    if text is None:
        return False

    # response = llm(system_prompt=system_prompt, user_prompt=user_prompt)
    # print(text)
    return query.lower() in text.lower()  # Simple keyword match
    # return response.split('<answer>')[1].split('</answer>')[0].strip() == 'Pass'


def main(query: str) -> list:
    """
    Takes in a string as a query and returns the list of lawyers.

    Args:
        query (str): The search query.

    Returns:
        list: A list of lawyers matching the query.
    """
    # TODO: Implement the search functionality
    # Iterate over the lawyer profiles and filter them based on the user's query
    lawyer_urls = []
    with open('lawyers.csv', 'r') as file:
        lawyer_urls = file.readlines()

    results = []
    start_time = time()

    # Check each lawyer's profile against the query
    for url in lawyer_urls:
        url = url.strip()  # Clean up the URL
        if passes_criterion(url, query):
            results.append(url)

    end_time = time()
    print(f"Query completed in {end_time - start_time:.2f} seconds")
    return results


if __name__ == '__main__':
    user_query = input('Enter your search term: ')
    results = main(user_query)
    print(f"Found {len(results)} matching lawyers:")
    for result in results:
        print(result)
