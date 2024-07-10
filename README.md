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

First, make sure you have Python installed on your machine.

Clone the repository and run:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

Create a `.env` file in the root directory and add the following variables:

```bash
HUBSPOT_API_KEY=your_hubspot_api_key
MAILERLITE_API_KEY=your_mailerlite_api_key
```

## Usage

To run the integration, you can execute the following command manually in the terminal or set it up as a cron job.

In the terminal, run:

```bash
python path/to/project/main.py
```

As a cron job, you can add the following line to the crontab file to run the integration every hour:

```bash
0 * * * * /path/to/python /path/to/project/main.py
```

Or set it up using an interface like cPanel.

This will run the main.py file which will use the HubSpot and MailerLite APIs to sync the data.

## Technical Details

Based on the information gathered from the MailerLite and HubSpot developers' documentation, here's an overview of the data structures and APIs available for both services:

### MailerLite API Overview

#### Data Structure

- **[Subscribers](https://github.com/mailerlite/mailerlite-php?tab=readme-ov-file#subscriber)**: The primary entity in MailerLite. Each subscriber has attributes such as `email`, `name`, `last_name`, `status` (active, unsubscribed, unconfirmed, bounced, junk), `subscribed_at`, `unsubscribed_at`, and custom fields.
- **[Campaigns](https://github.com/mailerlite/mailerlite-php?tab=readme-ov-file#campaign)**: Used to send email campaigns to subscribers. Each campaign has attributes like `subject`, `from`, `reply_to`, `sent_at`, `opened_at`, `clicked_at`, and more.
- **[Groups](https://github.com/mailerlite/mailerlite-php?tab=readme-ov-file#group-api)**: Used to organize subscribers into different groups. Each group has attributes like `name`, `description`, `created_at`, and `updated_at`.
- **[Segments](https://github.com/mailerlite/mailerlite-php?tab=readme-ov-file#segment-api)**: Used to segment subscribers based on conditions. Each segment has attributes like `name`, `description`, `created_at`, `updated_at`, and `conditions`.
- **[Fields](https://github.com/mailerlite/mailerlite-php?tab=readme-ov-file#field-api)**: Custom fields that can be added to subscribers to store additional information. Each field has attributes like `name`, `type`, `created_at`, and `updated_at`.
- **[Forms](https://github.com/mailerlite/mailerlite-php?tab=readme-ov-file#form-api)**: Used to create subscription forms to capture new subscribers. Each form has attributes like `name`, `code`, `created_at`, and `updated_at`.
- **[Automations](https://github.com/mailerlite/mailerlite-php?tab=readme-ov-file#automation-api)**: Used to create automated workflows based on subscriber actions. Each automation has attributes like `name`, `type`, `created_at`, and `updated_at`.
- **[Webhooks](https://github.com/mailerlite/mailerlite-php?tab=readme-ov-file#webhook-api)**: Used to set up webhooks for real-time notifications of subscriber actions. Each webhook has attributes like `url`, `events`, `created_at`, and `updated_at`.
- **[CampaignLanguages](https://github.com/mailerlite/mailerlite-php?tab=readme-ov-file#campaign-language-api)**: Used to set the language for campaigns. Each language has attributes like `code`, `name`, `created_at`, and `updated_at`.
- **[Timezones](https://github.com/mailerlite/mailerlite-php?tab=readme-ov-file#timezone-api)**: Used to set the timezone for subscribers. Each timezone has attributes like `name`, `offset`, `created_at`, and `updated_at`.
- **[Batches](https://github.com/mailerlite/mailerlite-php?tab=readme-ov-file#batch-api)**: Used to manage batch operations like importing or exporting subscribers. Each batch has attributes like `status`, `type`, `created_at`, and `updated_at`.

#### Key APIs

- **List All Subscribers**: GET request to list all subscribers with optional filters like status and pagination support.
- **Create/Upsert Subscriber**: POST request to create a new subscriber or update an existing one. If the subscriber already exists, the provided information updates the subscriber non-destructively.

#### Usage Example

Find the php client library for MailerLite [here](https://github.com/mailerlite/mailerlite-python).

```python
# Get the API key from environment variable
mailerlite_api_key = os.getenv('MAILERLITE_API_KEY')

# Initialize the MailerLite client
headers = {
  'Content-Type': 'application/json',
  'Authorization': f'Bearer {mailerlite_api_key}'
}

# Get all subscribers
response = requests.get('https://api.mailerlite.com/api/v2/subscribers', headers=headers)
subscribers = response.json()
```

### HubSpot API Overview

#### HubSpot Data Structure

HubSpot's API is extensive, covering various entities such as Contacts, Companies, Deals, and more. Each entity has its own set of properties and relationships. You can find
specific details in the HubSpot API documentation.

#### HubSpot Key APIs

Here are some of the key endpoints that seem to be available:

- **Contacts**: Manage contact information, including creating new contacts, updating existing ones, and fetching contact information.
- **Deals**: Manage sales deals, including tracking deal stages and associated contact or company information.

#### HubSpot Usage Example

Find the php client library for HubSpot [here](https://github.com/HubSpot/hubspot-api-python).

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
