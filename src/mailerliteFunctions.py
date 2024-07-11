import time

import requests


# Function to retrieve MailerLite subscribers
def get_all_mailerlite_subscribers(client):
    """
    Retrieves all subscribers from MailerLite using the provided API key.
    Starts with the first page and continues until all subscribers are fetched.
    :param client: The MailerLite client.
    :type client: Client
    :return: A list of all subscribers as JSON objects.
    rtype list
    """

    # Initialise an empty list to store all subscribers.
    all_subscribers = []
    # Number of subscribers per request
    per_page = 100
    # Initialize cursor
    cursor = None

    while True:
        # Make a GET request to the Mailerlite API using the client
        # If the cursor is None, send the first request without a cursor
        if cursor is None:
            response = client.subscribers.list(limit=per_page)
        else:
            response = client.subscribers.list(limit=per_page, cursor=cursor)

        # Check for rate limiting and handle it
        if response.get("error", {}).get("code") == 429:
            print("Rate limit exceeded. Waiting for 60 seconds...")
            time.sleep(60)
            continue

        # Check for unauthorized access
        if response.get("error", {}).get("code") == 401:
            print("Unauthorized access. Please check your API key.")
            break

        # Check for other possible errors
        if "error" in response:
            print(f"Error: {response['error']['message']}")
            break

        # Add the current page of subscribers to the list
        all_subscribers.extend(response.get("data", []))

        # Debugging information
        print(f"Retrieved {len(response.get('data', []))} subscribers")

        # Check if there's a next cursor
        cursor = response.get("meta", {}).get("next_cursor")
        if not cursor:
            break

    return all_subscribers


def create_mailerlite_subscriber(api_key, email, name):
    """
    Creates a new subscriber in MailerLite.

    :param api_key: The API key for MailerLite.
    :param email: The email address of the new subscriber.
    :param name: The name of the new subscriber.
    :return: The new subscriber as a JSON object, or None if an error occurred.
    """
    url = "https://api.mailerlite.com/api/v2/subscribers"
    headers = {
        "Content-Type": "application/json",
        "X-MailerLite-ApiKey": api_key
    }
    payload = {
        "email": email,
        "name": name
    }

    try:
        # Make a POST request to the MailerLite API
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Return the new subscriber
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

    return None


def update_mailerlite_subscriber(api_key, subscriber_id, email):
    """
    Updates an existing subscriber in MailerLite.

    :param api_key: The API key for MailerLite.
    :param subscriber_id: The ID of the subscriber to update.
    :param email: The new email address for the subscriber.
    :return: The updated subscriber as a JSON object, or None if an error occurred.
    """
    url = f"https://api.mailerlite.com/api/v2/subscribers/{subscriber_id}"
    headers = {
        "Content-Type": "application/json",
        "X-MailerLite-ApiKey": api_key
    }
    payload = {
        "email": email
    }

    try:
        # Make a PUT request to the MailerLite API
        response = requests.put(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Return the updated subscriber as a JSON object
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

    return None
