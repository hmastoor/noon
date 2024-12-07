import json
# from llm_utils import llm, get_embedding
from llm_utils_groq import llm, get_embedding
from time import time


def passes_criterion(lawyer_profile: dict, query: str) -> bool:
    """
    Evaluate if a lawyer passes a given criterion based on their profile text.

    Args:
        lawyer_profile (dict): The lawyer's profile containing the URL and text.
        query (str): Criterion to evaluate against.

    Returns:
        bool: True if lawyer passes the criterion, False otherwise.
    """
    text = lawyer_profile.get('profile_text', '')

    system_prompt = """
    You are an expert legal evaluator tasked with determining if a lawyer meets a specific criterion.

    Your goal is to read the lawyer's profile and evaluate whether they meet the provided criterion. You must:
    - Focus only on the information presented in the lawyer's profile.
    - Clearly indicate if the lawyer meets the criterion or not by responding with:
      - <thinking>...</thinking>: A detailed thought process explaining why the lawyer does or does not meet the criterion.
      - <answer>Pass</answer> or <answer>Fail</answer>: Your final answer based on the evaluation of the lawyer's profile in relation to the provided criterion.

    Please do not deviate from this format.
    """.strip()

    user_prompt = f"""
    Query: {query}

    Lawyer's Profile:
    {text}

    Based on the lawyer's profile, determine whether they pass the criterion specified in the query. Answer with 'Pass' if they meet the criterion, and 'Fail' if they do not. Provide reasoning in the <thinking> section.
    """.strip()

    if not text:
        return False

    response = llm(system_prompt=system_prompt, user_prompt=user_prompt)
    print('Raw response: ', response)

    # Clean the response by removing <thinking> tags and extracting content between <answer> tags
    clean_response = response.replace('<thinking>', '').replace('</thinking>', '').strip()

    try:
        # Extract the content between <answer> tags
        start_idx = clean_response.index('<answer>') + len('<answer>')
        end_idx = clean_response.index('</answer>')
        answer_content = clean_response[start_idx:end_idx].strip()

        # Check if the extracted answer is 'Pass'
        return answer_content.lower() == 'pass'
    except ValueError:
        # If we can't find <answer>...</answer> tags, return False
        print("Error: Unable to find <answer> tags in response.")
        return False


def main(query: str) -> list:
    """
    Takes in a string as a query and returns the list of lawyers whose profiles match the query.

    Args:
        query (str): The search query.

    Returns:
        list: A list of lawyers matching the query.
    """
    # Read lawyer profiles from the JSON file
    with open('lawyer_profiles.json', 'r') as file:
        profiles = json.load(file)

    results = []
    start_time = time()

    # Check each lawyer's profile against the query
    for profile in profiles[:10]:
        if passes_criterion(profile, query):
            results.append(profile['url'])

    end_time = time()
    print(f"Query completed in {end_time - start_time:.2f} seconds")
    return results


if __name__ == '__main__':
    while True:
        user_query = input('Enter your search term (or type "exit" to quit): ')
        if user_query.lower() == "exit":
            print("Exiting the program.")
            break  # Exit the loop if the user types "exit"

        results = main(user_query)
        print(f"Found {len(results)} matching lawyers:")
        for result in results:
            print(result)
