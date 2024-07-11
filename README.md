# HubSpot MailerLite Integration

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Usage](#usage)
- [Technical Details](#technical-details)
  - [MailerLite API Overview](#mailerlite-api-overview)
    - [Data Structure](#data-structure)
    - [Key APIs](#key-apis)
    - [Usage Example](#usage-example)
  - [HubSpot API Overview](#hubspot-api-overview)
    - [HubSpot Data Structure](#hubspot-data-structure)
    - [HubSpot Key APIs](#hubspot-key-apis)
    - [HubSpot Usage Example](#hubspot-usage-example)
  - [Integration Logic](#integration-logic)
  - [Considerations](#considerations)

## Overview

This is a simple integration between HubSpot and MailerLite APIs.
The MailerLite integration for HubSpot doesn't sync all the data we need by default, so we need to create a custom integration to sync the data we need.

## Setup

First, make sure you have Python installed on your machine. This project was tested using version 3.11.

Clone the repository and run the following commands in the project directory:

Create a virtual environment:
```bash
python -m venv venv
```

Activate the virtual environment:
On Windows:
```bash
venv\Scripts\activate
```
On MacOS/Linux:
```bash
source venv/bin/activate
```

Install the requirements:
```bash
pip install -r requirements.txt
```

Create a `.env` file in the root directory and add the following variables:

```bash
HUBSPOT_API_KEY=your_hubspot_api_key
MAILERLITE_API_KEY=your_mailerlite_api_key
```

## Usage

To run the integration, you can execute the following command manually in the terminal or set it up as a cron job.

Navigate to the project directory and run:

```bash
python main.py
```

As a cron job, you can add the following line to the crontab file to run the integration every hour:

```bash
0 * * * * /path/to/venv/Scripts/python.exe /path/to/project/main.py
```
The numbers at the start of the cron job line represent the minute, hour, day of the month, month, and day of the week when the job should run. You can customize these values based on your requirements.

Or set it up using an interface like cPanel.

This will run the main.py file which will use the HubSpot and MailerLite APIs to sync the data.

## Technical Details

Based on the information gathered from the MailerLite and HubSpot developers' documentation, here's an overview of the data structures and APIs available for both services:

### MailerLite API Overview

#### Data Structure

This is a high-level overview of what I think are the most relevant entities in MailerLite:

- **[Subscribers](https://developers.mailerlite.com/docs/subscribers.html)**: The primary entity in MailerLite. Each subscriber has attributes such as `email`, `name`, `last_name`, `status` (active, unsubscribed, unconfirmed, bounced, junk), `subscribed_at`, `unsubscribed_at`, and custom fields.
- **[Campaigns](https://developers.mailerlite.com/docs/campaigns.html)**: Used to send email campaigns to subscribers. Each campaign has attributes like `subject`, `from`, `reply_to`, `sent_at`, `opened_at`, `clicked_at`, and more.
- **[Groups](https://developers.mailerlite.com/docs/groups.html)**: Used to organize subscribers into different groups. Each group has attributes like `name`, `description`, `created_at`, and `updated_at`.
- **[Segments](https://developers.mailerlite.com/docs/segments.html)**: Used to segment subscribers based on conditions. Each segment has attributes like `name`, `description`, `created_at`, `updated_at`, and `conditions`.
- **[Fields](https://developers.mailerlite.com/docs/fields.html)**: Custom fields that can be added to subscribers to store additional information. Each field has attributes like `name`, `type`, `created_at`, and `updated_at`.
- **[Forms](https://developers.mailerlite.com/docs/forms.html)**: Used to create subscription forms to capture new subscribers. Each form has attributes like `name`, `code`, `created_at`, and `updated_at`.
- **[Automations](https://developers.mailerlite.com/docs/automations.html)**: Used to create automated workflows based on subscriber actions. Each automation has attributes like `name`, `type`, `created_at`, and `updated_at`.
- **[Batches](https://developers.mailerlite.com/docs/batching.html)**: Used to manage batch operations like importing or exporting subscribers. Each batch has attributes like `status`, `type`, `created_at`, and `updated_at`.

#### Key APIs

- **List All Subscribers**: GET request to list all subscribers with optional filters like status and pagination support.
- **Create/Upsert Subscriber**: POST request to create a new subscriber or update an existing one. If the subscriber already exists, the provided information updates the subscriber non-destructively.

#### Usage Example

The client library doesn't seem to support pagination at the time of writing this so I'm using the requests library to make the API calls.

```python
# Get the API key from environment variable
mailerlite_api_key = os.getenv('MAILERLITE_API_KEY')

# Base URL for the Mailerlite subscribers API
base_url = "https://connect.mailerlite.com/api/subscribers"

# Initialize the MailerLite client
headers = {
  'Content-Type': 'application/json',
  'Authorization': f'Bearer {mailerlite_api_key}'
}

# Make a GET request to the Mailerlite API using the requests library.
# Pass in the base URL as well as the headers, and query parameters if needed.
response = requests.get(base_url, headers=headers, params=params)
subscribers = response.json()
```

### HubSpot API Overview

#### HubSpot Data Structure

HubSpot's API is extensive, covering various entities such as Contacts, Companies, Deals, and more. Each entity has its own set of properties and relationships. You can find
specific details in the [HubSpot API documentation](https://developers.hubspot.com/docs/api/crm/contacts).

#### HubSpot Key APIs

Here are some of the key endpoints that seem to be available:

- **Contacts**: Manage contact information, including creating new contacts, updating existing ones, and fetching contact information.
- **Deals**: Manage sales deals, including tracking deal stages and associated contact or company information.

#### HubSpot Usage Example

The 

```python
import os
from hubspot import HubSpot
from hubspot.crm.contacts import ApiException as ContactsApiException

# Get the API key from environment variable
hubspot_api_key = os.getenv('HUBSPOT_API_KEY')

# Initialize the HubSpot client
hubspot_client = HubSpot(api_key=hubspot_api_key)

# Get all contacts from HubSpot
try:
  hubspot_contacts = hubspot_client.crm.contacts.basic_api.get_page()
  contacts = hubspot_contacts.results
except ContactsApiException as e:
  print("Error:", e)

```

### Integration Logic

Given these data structures and APIs, the integration logic could involve:

- Fetching contacts from HubSpot using the Contacts API.
- For each contact, check if a corresponding subscriber exists in MailerLite.
- If the subscriber exists, update their information; if not, create a new subscriber in MailerLite.

This process ensures that your HubSpot contacts are synced with your MailerLite subscribers, allowing for consistent data across both platforms for marketing and communication strategies.

### Considerations

- **Rate Limits**: Both HubSpot and MailerLite have API rate limits. Ensure our integration handles rate limiting gracefully, possibly by implementing retries with exponential 
  backoff.
- **Authentication**: Both HubSpot and MailerLite require API keys for authentication at the time of writing this. This project uses a Private App API key for HubSpot and a MailerLite API key.
- **Data Mapping**: Data from HubSpot and MailerLite don't exactly match. Especially with custom fields, the integration needs to map fields correctly to avoid errors or exceptions.
