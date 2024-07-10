import json
from datetime import datetime
import os
from dotenv import load_dotenv
from hubspot import HubSpot


def init():
    """
    Initializes environment variables and clients for HubSpot and MailerLite.

    :return: A tuple containing the HubSpot client and MailerLite API key.
    """
    # Load environment variables from the .env file
    load_dotenv()

    # Access the API keys from the environment variables
    hubspot_api_key = os.getenv('HUBSPOT_API_KEY')
    mailerlite_api_key = os.getenv('MAILERLITE_API_KEY')

    # Instantiate the HubSpot client using the API key
    hubspot_client = HubSpot(access_token=hubspot_api_key)

    return hubspot_client, mailerlite_api_key


# Custom JSON encoder to handle datetime objects
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            # Convert datetime objects to ISO 8601 string format
            return obj.isoformat()
        return super().default(obj)

