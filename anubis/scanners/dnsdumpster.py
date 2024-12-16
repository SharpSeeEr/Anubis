import re
import requests
from bs4 import BeautifulSoup


def search_dnsdumpster(self, target: str) -> None:
    """
    Searches DNSDumpster for subdomains of the given target domain.

    Args:
        self: The calling class instance, which maintains `self.domains`.
        target (str): The target domain to search for.

    Returns:
        None
    """
    print("Searching DNSDumpster")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://dnsdumpster.com/',
    }

    try:
        # Start a session for automatic cookie handling
        with requests.Session() as session:
            # Step 1: Get the CSRF token
            get_csrf_res = session.get('https://dnsdumpster.com', headers=headers, timeout=10)
            get_csrf_res.raise_for_status()

            # Parse CSRF token from the HTML page
            soup = BeautifulSoup(get_csrf_res.text, 'html.parser')
            csrf_token_input = soup.find('input', {'name': 'csrfmiddlewaretoken'})
            if not csrf_token_input:
                raise ValueError("CSRF token not found on DNSDumpster page")
            csrf_token = csrf_token_input['value']

            # Step 2: Post target data with the CSRF token
            data = {
                'csrfmiddlewaretoken': csrf_token,
                'targetip': target,
                'user': 'free',
            }
            res = session.post('https://dnsdumpster.com/', headers=headers, data=data, timeout=20)
            res.raise_for_status()

            # Step 3: Extract subdomains from the response
            soup = BeautifulSoup(res.text, 'html.parser')
            subdomain_pattern = re.compile(r'(?:[a-z0-9-]+\.)*' + re.escape(target))
            raw_links = soup.find_all(text=subdomain_pattern)

            # Clean and deduplicate links
            for domain in set(link.strip().lower() for link in raw_links if link.strip()):
                if domain not in self.domains and domain.endswith(f".{target}"):
                    self.domains.append(domain)
                    if self.options.get("--verbose", False):
                        print(f"DNSDumpster Found Domain: {domain}")

    except requests.exceptions.RequestException as e:
        self.handle_exception(e, "Error connecting to DNSDumpster")
    except Exception as e:
        self.handle_exception(e, "Error parsing DNSDumpster response")
