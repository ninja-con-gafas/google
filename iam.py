"""
The module handles identity and access management for Google services.
"""

def read_api_key(path: str) -> str:

    """
    Read API key from a text file.

    args:
        path (str): Path to the API key text file.

    returns:
        str: API key
    """

    print(f"Reading Gemini Developer API key from the file: {path}")
    with open(path) as api_key:
        return api_key.read()