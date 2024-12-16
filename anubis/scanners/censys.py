import os
from censys.certificates import CensysCertificates, CensysException
from anubis.utils.color_print import ColorPrint


def search_censys(self, target: str) -> None:
    """
    Searches Censys for certificate information related to the target.

    Args:
        self: The calling class instance, which maintains `self.domains`.
        target (str): The target domain to search for in Censys.

    Returns:
        None
    """
    print("Searching Censys")
    
    # Retrieve API keys from environment variables
    CENSYS_ID = os.getenv("CENSYS_ID")
    CENSYS_SECRET = os.getenv("CENSYS_SECRET")
    
    if not CENSYS_ID or not CENSYS_SECRET:
        ColorPrint.red(
            "To run a Censys scan, you must set your CENSYS_ID and CENSYS_SECRET environment variables."
        )
        return
    
    try:
        # Initialize Censys API client
        c = CensysCertificates(CENSYS_ID, CENSYS_SECRET)
        query = f"{target}"  # Refine query to target the specific domain
        
        # Fetch certificates
        certificates = c.search(query)
        
        if not certificates:
            ColorPrint.yellow(f"No certificates found for {target}")
            return
        
        # Process and print certificates
        for cert in certificates:
            domain = cert.get("parsed.subject.common_name", "Unknown")
            issuer = cert.get("parsed.issuer.common_name", "Unknown")
            ColorPrint.green(f"Domain: {domain}, Issuer: {issuer}")
            if domain not in self.domains:
                self.domains.append(domain)
    
    except CensysException as e:
        ColorPrint.red(f"Censys API error: {e}")
    except Exception as e:
        ColorPrint.red(f"An error occurred during the Censys scan: {e}")
