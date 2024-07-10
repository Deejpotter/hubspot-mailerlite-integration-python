import json
from src.mailerliteFunctions import get_mailerlite_subscribers
from src.generalFunctions import init, CustomJSONEncoder
from src.hubspotFunctions import test_get_contacts_and_deals, search_hubspot_contact_by_email_with_properties, \
    get_all_contact_properties, get_hubspot_contacts_with_http

# Initialize clients
hubspot_client, mailerlite_api_key = init()

# Retrieve data from MailerLite, such as subscribers
ml_data = get_mailerlite_subscribers(mailerlite_api_key, 1)
# Save the MailerLite data to a JSON file
with open('files/mailerlite.json', 'w') as file:
    json.dump(ml_data, file, indent=4)


# Define all the custom properties for the contacts
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

# Call the test function for Barry Phillips
barry_email = "barry.phillips@optusnet.com.au"
barry_file_name = 'files/hubspotContactBarryPhillips.json'
barry_deal_file_name = 'files/hubspotDealsBarryPhillips.json'
test_get_contacts_and_deals(hubspot_client, barry_email, barry_file_name, barry_deal_file_name)


# Call the test function for Jamie Wickstein
jamie_email = "jamiewickstein1@gmail.com"
jamie_file_name = 'files/hubspotContactJamieWickstein.json'
jamie_deal_file_name = 'files/hubspotDealsJamieWickstein.json'
test_get_contacts_and_deals(hubspot_client, jamie_email, jamie_file_name, jamie_deal_file_name)

# Also get the custom properties for Jamie Wickstein
all_properties = get_all_contact_properties(hubspot_client)
# Save the properties to a JSON file
with open('files/hubspotContactProperties.json', 'w') as file:
    json.dump([prop.to_dict() for prop in all_properties], file, indent=4, cls=CustomJSONEncoder)

# Test if we can get the custom properties using the email for Jamie Wickstein
contact_infos = search_hubspot_contact_by_email_with_properties(hubspot_client, jamie_email, properties)
# Output to a new file
with open('files/hubspotContactJamieWicksteinWithProperties.json', 'w') as file:
    json.dump([contact.to_dict() for contact in contact_infos], file, indent=4, cls=CustomJSONEncoder)

# Now test to see if we can get all the custom properties for all the contacts
all_contacts = get_hubspot_contacts_with_http(hubspot_client, properties)
# Output to a new file
with open('files/hubspotAllContacts.json', 'w') as file:
    json.dump([contact.to_dict() for contact in all_contacts], file, indent=4, cls=CustomJSONEncoder)
