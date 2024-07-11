import time

import requests


# Function to retrieve Mailerlite subscribers using direct API calls
def get_all_mailerlite_subscribers(api_key):
    """
    Retrieves all subscribers from Mailerlite using direct API calls.
    Uses cursor-based pagination to fetch all subscribers.
    :param api_key: The Mailerlite API key.
    :type api_key: str
    :return: A list of all subscribers as JSON objects.
    :rtype: list
    """

    # Initialise an empty list to store all subscribers.
    all_subscribers = []
    # Number of subscribers per request. Maximum is 100.
    per_page = 100
    # Initialise the cursor to None for the first request.
    cursor = None
    # Base URL for the Mailerlite subscribers API
    base_url = "https://connect.mailerlite.com/api/subscribers"

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    while True:
        # Initialise the query parameters for the request. Create a dictionary with the limit key set to the per_page value.
        params = {'limit': per_page}
        # If the cursor is not None, also add the cursor key to the dictionary.
        if cursor:
            params['cursor'] = cursor

        # Make a GET request to the Mailerlite API using the requests library.
        # Pass in the base URL, headers, and query parameters.
        response = requests.get(base_url, headers=headers, params=params)
        # Get the response data as a JSON object for easier processing.
        response_data = response.json()

        # Check for rate limiting and handle it.
        # If the status code is 429, it means the rate limit has been exceeded and we should wait for 60 seconds.
        if response.status_code == 429:
            print("Rate limit exceeded. Waiting for 60 seconds...")
            time.sleep(60)
            continue

        # If the status code is 401, it means unauthorized access. Check the API key is correct and being passed correctly.
        if response.status_code == 401:
            print("Unauthorized access. Please check your API key.")
            break

        # If the status code is not 200, there was some other error. Print the error message and break the loop.
        if response.status_code != 200:
            print(f"Error: {response_data.get('message', 'Unknown error')}")
            break

        # Add the current page of subscribers to the list by extracting the 'data' key from the response.
        subscribers = response_data.get("data", [])
        # Then add the subscribers to the all_subscribers list using the extend method.
        all_subscribers.extend(subscribers)

        # Print the number of subscribers retrieved on this page for debugging purposes.
        print(f"Retrieved {len(subscribers)} subscribers")

        # Get the next cursor value from the 'meta' key in the response data.
        cursor = response_data.get("meta", {}).get("next_cursor")

        # If there is no next cursor, we have reached the end of the subscribers list so we can break the loop.
        if not cursor:
            break

    # Finally, return the list of all subscribers.
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
