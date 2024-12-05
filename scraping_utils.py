import requests
from bs4 import BeautifulSoup


def parse_page(url: str) -> str:
    """
    Parse the content of a web page and extract its text.

    Args:
        url (str): The URL of the web page to parse.

    Returns:
        str: The extracted text content of the web page.

    Raises:
        requests.RequestException: If there's an error fetching the page.
    """
    # try:
    #     response = requests.get(url.strip())
    #     response.raise_for_status()
    #     soup = BeautifulSoup(response.content, 'lxml')
    #     return soup.body.get_text()
    # except requests.RequestException as e:
    #     raise requests.RequestException(f"Error fetching the page: {e}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url.strip(), headers=headers)
        # response.raise_for_status()  # Raises an HTTPError if the response code was unsuccessful
        # soup = BeautifulSoup(response.content, 'lxml')

        # Check if the "not authorized" message exists on the page
        if response.status_code == 403 or 'You are not authorized' in response.text:
            print(f"Skipping {url} due to authorization error.")
            return None  # skip that page

        response.raise_for_status()  # Raises an HTTPError if the response code was unsuccessful
        soup = BeautifulSoup(response.content, 'lxml')
        return soup.body.get_text()  # Extracts text from the body of the HTML page
    except requests.RequestException as e:
        raise requests.RequestException(f"Error fetching the page {url}: {e}")
