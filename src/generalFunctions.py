import json
from datetime import datetime
import os

from mailerlite import Client
from dotenv import load_dotenv
from hubspot import HubSpot
from src.mailerliteFunctions import update_mailerlite_subscriber


def init():
    """
    Initializes environment variables and clients for HubSpot and MailerLite.

    :return: A tuple containing the HubSpot client and the MailerLite client.
    """
    # Load environment variables from the .env file
    load_dotenv()

    # Access the API keys from the environment variables
    hubspot_api_key = os.getenv('HUBSPOT_API_KEY')
    mailerlite_api_key = os.getenv('MAILERLITE_API_KEY')

    # Instantiate the HubSpot client using the API key
    hubspot_client = HubSpot(access_token=hubspot_api_key)

    mailerlite_client = Client({
        'api_key': mailerlite_api_key
    })

    return hubspot_client, mailerlite_client


# Custom JSON encoder to handle datetime objects
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            # Convert datetime objects to ISO 8601 string format
            return obj.isoformat()
        return super().default(obj)


# Process all the data from HubSpot to MailerLite
def process_all_data(all_hubspot_contacts, ml_subscribers_dict, mailerlite_api_key):
    """
    Takes all the data from HubSpot and updates or creates subscribers in MailerLite.
    :param all_hubspot_contacts: A list of all contacts from HubSpot.
    :type all_hubspot_contacts: list[SimplePublicObjectWithAssociations]
    :param ml_subscribers_dict: A dictionary of all subscribers from MailerLite.
    :type ml_subscribers_dict: dict
    :param mailerlite_api_key: The API key for MailerLite.
    :type mailerlite_api_key: str
    :return: None
    """
    # Loop through all the contacts from HubSpot.
    for contact in all_hubspot_contacts:
        # Get the email address of the current contact.
        email = contact.properties.get('email')

        # If the email is found in the MailerLite subscribers dictionary.
        if email in ml_subscribers_dict:
            # Create a new object with the updated data from the relevant contact.
            update_data = {
                "fields": {
                    "createdAt": contact.properties.get('createdAt'),
                    "updatedAt": contact.properties.get('updatedAt'),
                    "archived": contact.properties.get('archived'),
                    "abandoned_cart_counter": contact.properties.get('abandoned_cart_counter'),
                    "abandoned_cart_date": contact.properties.get('abandoned_cart_date'),
                    "abandoned_cart_products": contact.properties.get('abandoned_cart_products'),
                    "abandoned_cart_products_categories": contact.properties.get('abandoned_cart_products_categories'),
                    "abandoned_cart_products_skus": contact.properties.get('abandoned_cart_products_skus'),
                    "abandoned_cart_subtotal": contact.properties.get('abandoned_cart_subtotal'),
                    "abandoned_cart_url": contact.properties.get('abandoned_cart_url'),
                    "address": contact.properties.get('address'),
                    "city": contact.properties.get('city'),
                    "company": contact.properties.get('company'),
                    "country": contact.properties.get('country'),
                    "createdate": contact.properties.get('createdate'),
                    "current_abandoned_cart": contact.properties.get('current_abandoned_cart'),
                    "firstname": contact.properties.get('firstname'),
                    "hs_createdate": contact.properties.get('hs_createdate'),
                    "hs_email_domain": contact.properties.get('hs_email_domain'),
                    "hs_language": contact.properties.get('hs_language'),
                    "hs_object_id": contact.properties.get('hs_object_id'),
                    "hs_persona": contact.properties.get('hs_persona'),
                    "last_product_bought": contact.properties.get('last_product_bought'),
                    "last_products_bought": contact.properties.get('last_products_bought'),
                    "last_products_bought_product_1_image_url": contact.properties.get(
                        'last_products_bought_product_1_image_url'),
                    "last_products_bought_product_1_name": contact.properties.get(
                        'last_products_bought_product_1_name'),
                    "last_products_bought_product_1_price": contact.properties.get(
                        'last_products_bought_product_1_price'),
                    "last_products_bought_product_1_url": contact.properties.get('last_products_bought_product_1_url'),
                    "last_products_bought_product_2_image_url": contact.properties.get(
                        'last_products_bought_product_2_image_url'),
                    "last_products_bought_product_2_name": contact.properties.get(
                        'last_products_bought_product_2_name'),
                    "last_products_bought_product_2_price": contact.properties.get(
                        'last_products_bought_product_2_price'),
                    "last_products_bought_product_2_url": contact.properties.get('last_products_bought_product_2_url'),
                    "last_products_bought_product_3_image_url": contact.properties.get(
                        'last_products_bought_product_3_image_url'),
                    "last_products_bought_product_3_name": contact.properties.get(
                        'last_products_bought_product_3_name'),
                    "last_products_bought_product_3_price": contact.properties.get(
                        'last_products_bought_product_3_price'),
                    "last_products_bought_product_3_url": contact.properties.get('last_products_bought_product_3_url'),
                    "last_total_number_of_products_bought": contact.properties.get(
                        'last_total_number_of_products_bought'),
                    "lastmodifieddate": contact.properties.get('lastmodifieddate'),
                    "lastname": contact.properties.get('lastname'),
                    "lifecyclestage": contact.properties.get('lifecyclestage'),
                    "opportunity": contact.properties.get('opportunity'),
                    "mobilephone": contact.properties.get('mobilephone'),
                    "numemployees": contact.properties.get('numemployees'),
                    "phone": contact.properties.get('phone'),
                    "products_bought": contact.properties.get('products_bought'),
                    "salutation": contact.properties.get('salutation'),
                    "state": contact.properties.get('state'),
                    "total_number_of_products_bought": contact.properties.get('total_number_of_products_bought'),
                    "website": contact.properties.get('website'),
                    "zip": contact.properties.get('zip'),
                    "last_order_order_number": contact.properties.get('last_order_order_number')
                }
            }
            # If the email is found in the MailerLite subscribers dictionary, update the subscriber.
            update_mailerlite_subscriber(mailerlite_api_key, ml_subscribers_dict[email]['id'], update_data)

        # If the email is not found in the MailerLite subscribers dictionary, create a new subscriber.
        elif email not in ml_subscribers_dict:
            # Prepare the data to create a new subscriber in MailerLite
            create_data = {
                "email": email,
                "fields": {
                    "createdAt": contact.properties.get('createdAt'),
                    "updatedAt": contact.properties.get('updatedAt'),
                    "archived": contact.properties.get('archived'),
                    "abandoned_cart_counter": contact.properties.get('abandoned_cart_counter'),
                    "abandoned_cart_date": contact.properties.get('abandoned_cart_date'),
                    "abandoned_cart_products": contact.properties.get('abandoned_cart_products'),
                    "abandoned_cart_products_categories": contact.properties.get('abandoned_cart_products_categories'),
                    "abandoned_cart_products_skus": contact.properties.get('abandoned_cart_products_skus'),
                    "abandoned_cart_subtotal": contact.properties.get('abandoned_cart_subtotal'),
                    "abandoned_cart_url": contact.properties.get('abandoned_cart_url'),
                    "address": contact.properties.get('address'),
                    "city": contact.properties.get('city'),
                    "company": contact.properties.get('company'),
                    "country": contact.properties.get('country'),
                    "createdate": contact.properties.get('createdate'),
                    "current_abandoned_cart": contact.properties.get('current_abandoned_cart'),
                    "firstname": contact.properties.get('firstname'),
                    "hs_createdate": contact.properties.get('hs_createdate'),
                    "hs_email_domain": contact.properties.get('hs_email_domain'),
                    "hs_language": contact.properties.get('hs_language'),
                    "hs_object_id": contact.properties.get('hs_object_id'),
                    "hs_persona": contact.properties.get('hs_persona'),
                    "last_product_bought": contact.properties.get('last_product_bought'),
                    "last_products_bought": contact.properties.get('last_products_bought'),
                    "last_products_bought_product_1_image_url": contact.properties.get(
                        'last_products_bought_product_1_image_url'),
                    "last_products_bought_product_1_name": contact.properties.get(
                        'last_products_bought_product_1_name'),
                    "last_products_bought_product_1_price": contact.properties.get(
                        'last_products_bought_product_1_price'),
                    "last_products_bought_product_1_url": contact.properties.get('last_products_bought_product_1_url'),
                    "last_products_bought_product_2_image_url": contact.properties.get(
                        'last_products_bought_product_2_image_url'),
                    "last_products_bought_product_2_name": contact.properties.get(
                        'last_products_bought_product_2_name'),
                    "last_products_bought_product_2_price": contact.properties.get(
                        'last_products_bought_product_2_price'),
                    "last_products_bought_product_2_url": contact.properties.get('last_products_bought_product_2_url'),
                    "last_products_bought_product_3_image_url": contact.properties.get(
                        'last_products_bought_product_3_image_url'),
                    "last_products_bought_product_3_name": contact.properties.get(
                        'last_products_bought_product_3_name'),
                    "last_products_bought_product_3_price": contact.properties.get(
                        'last_products_bought_product_3_price'),
                    "last_products_bought_product_3_url": contact.properties.get('last_products_bought_product_3_url'),
                    "last_total_number_of_products_bought": contact.properties.get(
                        'last_total_number_of_products_bought'),
                    "lastmodifieddate": contact.properties.get('lastmodifieddate'),
                    "lastname": contact.properties.get('lastname'),
                    "lifecyclestage": contact.properties.get('lifecyclestage'),
                    "opportunity": contact.properties.get('opportunity'),
                    "mobilephone": contact.properties.get('mobilephone'),
                    "numemployees": contact.properties.get('numemployees'),
                    "phone": contact.properties.get('phone'),
                    "products_bought": contact.properties.get('products_bought'),
                    "salutation": contact.properties.get('salutation'),
                    "state": contact.properties.get('state'),
                    "total_number_of_products_bought": contact.properties.get('total_number_of_products_bought'),
                    "website": contact.properties.get('website'),
                    "zip": contact.properties.get('zip'),
                    "last_order_order_number": contact.properties.get('last_order_order_number')
                }
            }

        # Otherwise, print a message indicating that the email was not found in the MailerLite subscribers dictionary.
        else:
            print(f"No contact found with the email: {email}")

