# from scraping_utils import parse_page

# # Test a single lawyer profile URL from your CSV
# test_url = 'https://www.davispolk.com/lawyers/leslie-altus'
# profile_text = parse_page(test_url)

# # Print out the profile content to verify the scraping
# print(profile_text)

from scraping_utils import parse_page
from llm_utils import llm
from main import passes_criterion

# Test a specific lawyer profile URL and query
test_url = 'https://www.davispolk.com/lawyers/leslie-altus'
test_query = 'lawyers named leslie'

# Check if the lawyer passes the criterion
result = passes_criterion(test_url, test_query)
print(f"Does the lawyer pass the criterion? {result}")
