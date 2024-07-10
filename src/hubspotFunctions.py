import json
from hubspot.crm.contacts import ApiException as ContactsApiException
from hubspot.crm.deals import ApiException as DealsApiException
from hubspot.crm.quotes import ApiException as QuotesApiException
from hubspot.crm.contacts import PublicObjectSearchRequest, Filter, FilterGroup
from hubspot.crm.properties import ApiException as PropertiesApiException
from src.generalFunctions import CustomJSONEncoder


# Contact endpoints
def get_hubspot_contacts_with_http(hubspot_client, properties=None):
    """
    Retrieves all HubSpot contacts using the HubSpot Python client library.
    :param hubspot_client: The HubSpot client instance.
    :type hubspot_client: HubSpot
    :param properties: A list of properties to retrieve for the contacts.
    :type properties: list
    """
    try:
        # Fetch the first page of contacts
        hubspot_contacts = hubspot_client.crm.contacts.basic_api.get_page(properties=properties)
        return hubspot_contacts.results
    except ContactsApiException as e:
        print("Error:", e)
        return None


def get_limited_hubspot_contacts_with_http(hubspot_client, limit=10):
    """
    Retrieves a limited number of HubSpot contacts using the HubSpot Python client library.
    """
    try:
        # Fetch a limited number of contacts
        hubspot_contacts = hubspot_client.crm.contacts.basic_api.get_page(limit=limit)
        return hubspot_contacts.results
    except ContactsApiException as e:
        print("Error:", e)
        return None


def search_hubspot_contact_by_email(hubspot_client, email):
    """
    Searches for a HubSpot contact by email and retrieves specific properties.
    """
    try:
        # Define the filter for the search
        email_filter = Filter(property_name="email", operator="EQ", value=email)
        filter_group = FilterGroup(filters=[email_filter])

        # Define the search request with the filter and specific properties
        search_request = PublicObjectSearchRequest(
            filter_groups=[filter_group]
        )

        # Execute the search
        search_results = hubspot_client.crm.contacts.search_api.do_search(search_request)
        return search_results.results
    except ContactsApiException as e:
        print("Error:", e)
        return None


def search_hubspot_contact_by_email_with_properties(hubspot_client, email, properties):
    """
    Searches for a HubSpot contact by email and retrieves specific properties.

    :param hubspot_client: The HubSpot client instance.
    :type hubspot_client: HubSpot
    :param email: The email of the contact to search for.
    :type email: str
    :param properties: A list of properties to retrieve for the contact.
    :type properties: list
    :return: A list of contacts matching the email with specified properties.
    :rtype: list
    """
    try:
        # Define the filter for the search
        email_filter = Filter(property_name="email", operator="EQ", value=email)
        filter_group = FilterGroup(filters=[email_filter])

        # Define the search request with the filter and specific properties
        search_request = PublicObjectSearchRequest(
            filter_groups=[filter_group],
            properties=properties
        )

        # Execute the search
        search_results = hubspot_client.crm.contacts.search_api.do_search(search_request)
        return search_results.results
    except ContactsApiException as e:
        print("Error:", e)
        return None


def get_all_contact_properties(hubspot_client):
    """
    Retrieves all property names for the contact object type.

    :param hubspot_client: The HubSpot client instance.
    :return: A list of all property names for contacts.
    """
    try:
        # Retrieve all properties for the contact object type
        api_response = hubspot_client.crm.properties.core_api.get_all(object_type="contact", archived=False)
        return api_response.results
    except PropertiesApiException as e:
        print("Exception when calling core_api->get_all: %s\n" % e)
        return None


def get_contacts_and_deals(hubspot_client):
    """
    Retrieves all contacts and their associated deals from HubSpot.
    """
    # Get all contacts using the HubSpot client
    contacts = get_hubspot_contacts_with_http(hubspot_client)
    if contacts is None:
        return None

    # Iterate over each contact to get their associated deals
    for contact in contacts:
        contact_id = contact.id
        deal_ids = get_hubspot_deals_with_http(hubspot_client)

        deals = []
        for deal_id in deal_ids:
            deal_details = get_deal_details_by_id(hubspot_client, deal_id)
            if deal_details is not None:
                deals.append(deal_details)

        # Attach the deals to the contact
        contact.deals = deals

    return contacts


# Deal endpoints
def get_deal_details_by_id(hubspot_client, deal_id):
    """
    Fetches HubSpot deal details by deal ID.
    """
    try:
        # Get deal details by deal ID
        deal_details = hubspot_client.crm.deals.basic_api.get_by_id(deal_id)
        return deal_details
    except DealsApiException as e:
        print("Error:", e)
        return None


def get_hubspot_deals_with_http(hubspot_client):
    """
    Retrieves all HubSpot deals using the HubSpot Python client library.
    """
    try:
        # Fetch the first page of deals
        hubspot_deals = hubspot_client.crm.deals.basic_api.get_page()
        return hubspot_deals.results
    except DealsApiException as e:
        print("Error:", e)
        return None


def get_limited_hubspot_deals_with_http(hubspot_client, limit=10):
    """
    Retrieves a limited number of HubSpot deals using the HubSpot Python client library.
    """
    try:
        # Fetch a limited number of deals
        hubspot_deals = hubspot_client.crm.deals.basic_api.get_page(limit=limit)
        return hubspot_deals.results
    except DealsApiException as e:
        print("Error:", e)
        return None


def get_associated_deals(client, contact_id):
    """
    Retrieves deals associated with a HubSpot contact by contact ID.
    The contact ID is the unique identifier for a contact in HubSpot and can be obtained by searching for a contact by email then extracting the ID.
    The contact ID can then be used to retrieve other associated objects like deals.
    """
    try:
        # Get associations for the contact
        associations = client.crm.associations.v4.basic_api.get_page('contacts', contact_id, 'deals')

        # Extract deal IDs from the associations using the to_object_id property to convert the association to an id
        deal_ids = [association.to_object_id for association in associations.results]

        deals = []
        for deal_id in deal_ids:
            # Get deal details by deal ID
            deal = client.crm.deals.basic_api.get_by_id(deal_id)
            deals.append(deal.to_dict())

        return deals
    except DealsApiException as e:
        print(f"Error: {e}")
        return None


# Quote endpoints
def get_limited_hubspot_quotes_with_http(hubspot_client, limit=10):
    """
    Retrieves a limited number of HubSpot quotes using the HubSpot Python client library.
    """
    try:
        # Fetch a limited number of quotes
        hubspot_quotes = hubspot_client.crm.quotes.basic_api.get_page(limit=limit)
        return hubspot_quotes.results
    except QuotesApiException as e:
        print("Error:", e)
        return None


# Define a function to test the data retrieval for a Contact and their associated Deals
def test_get_contacts_and_deals(hubspot_client, input_email, contact_file_name='files/hubspotContactBarryPhillips.json',
                                deal_file_name='files/hubspotContactBarryPhillips.json'):
    contacts = search_hubspot_contact_by_email(hubspot_client, input_email)

    # Save the contact data to a file
    with open(contact_file_name, 'w') as open_file:
        # Serialize the contact data to JSON using the custom encoder
        json.dump([contact.to_dict() for contact in contacts], open_file, indent=4, cls=CustomJSONEncoder)

    # Check if the contact was found
    if contacts:
        # Directly access the 'id' property of the first contact
        contact_id = contacts[0].id

        # Retrieve deals associated with the contact
        deals = get_associated_deals(hubspot_client, contact_id)

        # Save the associated deals to a file
        with open(deal_file_name, 'w') as open_file:
            # Serialize the deal data to JSON using the custom encoder
            json.dump(deals, open_file, indent=4, cls=CustomJSONEncoder)
    else:
        print(f"No contact found with the email: {input_email}")


# Create a test function to get all the properties of an object type
def get_all_properties_of_object_type(hubspot_client, object_type):
    """
    Retrieves all properties of a specific object type in HubSpot.
    """
    try:
        api_response = hubspot_client.crm.properties.core_api.get_all(object_type="objectType", archived=False)
        print(api_response)
    except ApiException as e:
        print("Exception when calling core_api->get_all: %s\n" % e)
