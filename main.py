import json

from hubspot.crm.contacts import SimplePublicObjectWithAssociations

from src.mailerliteFunctions import get_all_mailerlite_subscribers, update_mailerlite_subscriber
from src.generalFunctions import init, CustomJSONEncoder, process_all_data
from src.hubspotFunctions import get_hubspot_contacts_with_http

# Initialize clients for HubSpot and MailerLite.
# This function should set up the necessary API clients and return them.
hubspot_client, mailerlite_client = init()

# Define the custom properties we want to retrieve from HubSpot.
# This list includes all the properties that are relevant to our integration.
properties = [
    "_zap_search_was_found_status", "createdAt", "updatedAt", "archived",
    "abandoned_cart_counter", "abandoned_cart_date", "abandoned_cart_products",
    "abandoned_cart_products_categories", "abandoned_cart_products_skus",
    "abandoned_cart_subtotal", "abandoned_cart_url", "address", "city",
    "company", "country", "createdate", "current_abandoned_cart", "email",
    "firstname", "hs_createdate", "hs_email_domain", "hs_language",
    "hs_object_id", "hs_persona", "last_product_bought", "last_products_bought",
    "last_products_bought_product_1_image_url", "last_products_bought_product_1_name",
    "last_products_bought_product_1_price", "last_products_bought_product_1_url",
    "last_products_bought_product_2_image_url", "last_products_bought_product_2_name",
    "last_products_bought_product_2_price", "last_products_bought_product_2_url",
    "last_products_bought_product_3_image_url", "last_products_bought_product_3_name",
    "last_products_bought_product_3_price", "last_products_bought_product_3_url",
    "last_total_number_of_products_bought", "lastmodifieddate", "lastname",
    "lifecyclestage", "opportunity", "mobilephone", "numemployees", "phone",
    "products_bought", "salutation", "state", "total_number_of_products_bought",
    "website", "zip", "last_order_order_number"
]

# Step 1: Retrieve all contacts from HubSpot with the specified properties.
# This function should interact with the HubSpot API to fetch all contacts with the given properties.
all_hubspot_contacts: list[SimplePublicObjectWithAssociations] = get_hubspot_contacts_with_http(hubspot_client, properties)

# Save the retrieved contacts to a JSON file for reference or backup.
# This allows us to have a local copy of the data for debugging or analysis.
with open('files/hubspotAllContacts.json', 'w') as file:
    json.dump([contact.to_dict() for contact in all_hubspot_contacts], file, indent=4, cls=CustomJSONEncoder)


# Step 2: Retrieve subscribers from MailerLite.
# Fetch the first page of subscribers from MailerLite using the provided API key.
ml_subscribers = get_all_mailerlite_subscribers(mailerlite_client)
ml_subscribers_dict = {subscriber['email']: subscriber for subscriber in ml_subscribers}

# Save the retrieved MailerLite subscribers to a JSON file for reference.
with open('files/mailerliteSubscribers.json', 'w') as file:
    json.dump(ml_subscribers, file, indent=4)


# Step 3: Update or create MailerLite subscribers with HubSpot data.
process_all_data(all_hubspot_contacts, ml_subscribers_dict, mailerlite_client)


# Save the updated MailerLite subscribers to a JSON file for reference or backup.
# This allows us to have a local copy of the updated data for debugging or analysis.
# This could be replaced with logging instead if needed.
with open('files/updated_mailerlite_subscribers.json', 'w') as file:
    json.dump(ml_subscribers, file, indent=4)

