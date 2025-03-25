"""
The module handles identity and access management for Google services.
"""

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build, Resource
from typing import List

def build_resource_for_service_account(path: str, scopes: List[str], service_name: str, version: str) -> Resource:

    """
    Builds and returns a Google API client Resource object for a specified service using service account credentials
    from a JSON key file.

    args:
        path (str): The file path to the service account key JSON file.
        scopes (List[str]): A list of OAuth 2.0 scopes to authorize for the credentials.
        service_name (str): The name of the Google API service.
        version (str): The version of the API to use.

    returns:
        Resource: A Resource object that can be used to interact with the specified Google API service.

    raises:
        google.auth.exceptions.GoogleAuthError: If loading the credentials or building the resource fails.
    """

    print(f"Loading credentials for Google Service Account from the file: {path}")
    return (build(credentials=Credentials.from_service_account_file(filename=path, scopes=scopes),
                  serviceName=service_name,
                  version=version))

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