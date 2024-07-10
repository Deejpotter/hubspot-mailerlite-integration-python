import json
import os
from src.mailerliteFunctions import get_mailerlite_subscribers, update_mailerlite_subscriber
from src.generalFunctions import init, CustomJSONEncoder
from src.hubspotFunctions import get_hubspot_contacts_with_http

# Initialize clients for HubSpot and MailerLite
# This function should set up the necessary API clients and return them
hubspot_client, mailerlite_api_key = init()

# Define the custom properties we want to retrieve from HubSpot
# This list includes all the properties that are relevant to our integration
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

# Step 1: Retrieve all contacts from HubSpot with the specified properties
# This function should interact with the HubSpot API to fetch all contacts with the given properties
all_contacts = get_hubspot_contacts_with_http(hubspot_client, properties)

# Save the retrieved contacts to a JSON file for reference or backup
# This allows us to have a local copy of the data for debugging or analysis
with open('files/hubspotAllContacts.json', 'w') as file:
    json.dump([contact.to_dict() for contact in all_contacts], file, indent=4, cls=CustomJSONEncoder)

# Step 2: Retrieve subscribers from MailerLite
# Fetch the first page of subscribers from MailerLite using the provided API key
ml_subscribers = get_mailerlite_subscribers(mailerlite_api_key, 1)

# Step 3: Update MailerLite subscribers with HubSpot data
# Iterate over each subscriber and update their profile with the corresponding data from HubSpot
for subscriber in ml_subscribers:
    email = subscriber['email']

    # Find the corresponding contact in HubSpot
    contact = next((c for c in all_contacts if c.email == email), None)

    if contact:
        # Prepare the data to update the subscriber in MailerLite
        update_data = {
            "fields": {
                "createdAt": contact.createdAt,
                "updatedAt": contact.updatedAt,
                "archived": contact.archived,
                "abandoned_cart_counter": contact.abandoned_cart_counter,
                "abandoned_cart_date": contact.abandoned_cart_date,
                "abandoned_cart_products": contact.abandoned_cart_products,
                "abandoned_cart_products_categories": contact.abandoned_cart_products_categories,
                "abandoned_cart_products_skus": contact.abandoned_cart_products_skus,
                "abandoned_cart_subtotal": contact.abandoned_cart_subtotal,
                "abandoned_cart_url": contact.abandoned_cart_url,
                "address": contact.address,
                "city": contact.city,
                "company": contact.company,
                "country": contact.country,
                "createdate": contact.createdate,
                "current_abandoned_cart": contact.current_abandoned_cart,
                "firstname": contact.firstname,
                "hs_createdate": contact.hs_createdate,
                "hs_email_domain": contact.hs_email_domain,
                "hs_language": contact.hs_language,
                "hs_object_id": contact.hs_object_id,
                "hs_persona": contact.hs_persona,
                "last_product_bought": contact.last_product_bought,
                "last_products_bought": contact.last_products_bought,
                "last_products_bought_product_1_image_url": contact.last_products_bought_product_1_image_url,
                "last_products_bought_product_1_name": contact.last_products_bought_product_1_name,
                "last_products_bought_product_1_price": contact.last_products_bought_product_1_price,
                "last_products_bought_product_1_url": contact.last_products_bought_product_1_url,
                "last_products_bought_product_2_image_url": contact.last_products_bought_product_2_image_url,
                "last_products_bought_product_2_name": contact.last_products_bought_product_2_name,
                "last_products_bought_product_2_price": contact.last_products_bought_product_2_price,
                "last_products_bought_product_2_url": contact.last_products_bought_product_2_url,
                "last_products_bought_product_3_image_url": contact.last_products_bought_product_3_image_url,
                "last_products_bought_product_3_name": contact.last_products_bought_product_3_name,
                "last_products_bought_product_3_price": contact.last_products_bought_product_3_price,
                "last_products_bought_product_3_url": contact.last_products_bought_product_3_url,
                "last_total_number_of_products_bought": contact.last_total_number_of_products_bought,
                "lastmodifieddate": contact.lastmodifieddate,
                "lastname": contact.lastname,
                "lifecyclestage": contact.lifecyclestage,
                "opportunity": contact.opportunity,
                "mobilephone": contact.mobilephone,
                "numemployees": contact.numemployees,
                "phone": contact.phone,
                "products_bought": contact.products_bought,
                "salutation": contact.salutation,
                "state": contact.state,
                "total_number_of_products_bought": contact.total_number_of_products_bought,
                "website": contact.website,
                "zip": contact.zip,
                "last_order_order_number": contact.last_order_order_number
            }
        }

        # Update the subscriber in MailerLite with the new data
        update_mailerlite_subscriber(mailerlite_api_key, subscriber['id'], update_data)

# Save the updated MailerLite subscribers to a JSON file for reference or backup
# This allows us to have a local copy of the updated data for debugging or analysis
with open('files/updated_mailerlite_subscribers.json', 'w') as file:
    json.dump(ml_subscribers, file, indent=4)

