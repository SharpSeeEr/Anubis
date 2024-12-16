from json import JSONDecodeError, loads
import requests
from anubis.utils.color_print import ColorPrint


def search_anubisdb(self, target: str) -> None:
    """
    Searches Anubis-DB for subdomains of a given target.

    Args:
        self: The calling class instance, which maintains `self.domains`.
        target (str): The target domain to search.

    Returns:
        None
    """
    try:
        print("Searching Anubis-DB")
        response = requests.get(f"https://jonlu.ca/anubis/subdomains/{target}", timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        
        try:
            subdomains = loads(response.text)
            if isinstance(subdomains, list):
                for subdomain in subdomains:
                    if subdomain not in self.domains:
                        self.domains.append(subdomain)
            else:
                ColorPrint.red("Unexpected response format from Anubis-DB")
        except JSONDecodeError:
            ColorPrint.red("Failed to parse JSON response from Anubis-DB")
    except requests.exceptions.RequestException as e:
        ColorPrint.red(f"Error connecting to Anubis-DB: {e}")


def send_to_anubisdb(self, target: list[str]) -> None:
    """
    Sends discovered subdomains to Anubis-DB for a single target.

    Args:
        self: The calling class instance, which maintains `self.domains`.
        target (list[str]): List containing a single target domain.

    Returns:
        None
    """
    if len(target) != 1:
        print("Cannot send multiple domains to Anubis-DB")
        return

    try:
        print("Sending to Anubis-DB")
        data = {'subdomains': self.domains}
        response = requests.post(f"https://jonlu.ca/anubis/subdomains/{target[0]}",
                                 json=data, timeout=10)
        
        if response.status_code == 200:
            print("Successfully sent results to Anubis-DB")
        else:
            ColorPrint.red(f"Error sending results to Anubis-DB - Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        ColorPrint.red(f"Error connecting to Anubis-DB: {e}")
