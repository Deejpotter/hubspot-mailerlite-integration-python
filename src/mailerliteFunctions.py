import requests


# Function to retrieve MailerLite subscribers
def get_mailerlite_subscribers(api_key, page):
    url = f"https://api.mailerlite.com/api/v2/subscribers?page={page}"
    headers = {
        "Content-Type": "application/json",
        "X-MailerLite-ApiKey": api_key
    }

    # Make a GET request to the MailerLite API
    response = requests.get(url, headers=headers)

    # Return the JSON response
    return response.json()


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
