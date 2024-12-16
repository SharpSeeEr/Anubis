import re
import requests
from bs4 import BeautifulSoup  # Use BeautifulSoup for parsing HTML


def _clean_links(links):
    """
    Removes duplicates and cleans up domain names.
    Args:
        links (list): List of domain strings.
    Returns:
        list: Deduplicated and cleaned list of domains.
    """
    return list(set(link.strip().lower() for link in links if link.strip()))


def search_crtsh(self, target: str) -> None:
    """
    Searches crt.sh for subdomains of the given target.

    Args:
        self: The calling class instance, which maintains `self.domains`.
        target (str): The target domain to search for.

    Returns:
        None
    """
    print("Searching crt.sh")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    params = {'q': f'%.{target}'}
    url = 'https://crt.sh/'

    try:
        # Make the request with a timeout
        res = requests.get(url, headers=headers, params=params, timeout=10)
        
        if res.status_code != 200:
            self.handle_exception(
                None,
                f"crt.sh returned a non-200 status code: {res.status_code}"
            )
            return

        # Parse the response HTML
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Extract subdomains using a more structured approach
        subdomain_finder = re.compile(r'\b(?:[a-z0-9-]+\.)*' + re.escape(target) + r'\b')
        raw_links = soup.find_all(text=subdomain_finder)
        parsed_links = _clean_links(raw_links)

        # Add unique subdomains to self.domains
        for domain in parsed_links:
            if domain not in self.domains and domain.endswith(f".{target}"):
                self.domains.append(domain)
                if self.options.get("--verbose", False):
                    print(f"Crt.sh Found Domain: {domain}")

    except requests.exceptions.RequestException as e:
        self.handle_exception(e, "Error connecting to crt.sh")
    except Exception as e:
        self.handle_exception(e, "Error parsing crt.sh response")
