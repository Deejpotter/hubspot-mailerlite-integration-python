import json
from hubspot.crm.contacts import ApiException as ContactsApiException
from hubspot.crm.deals import ApiException as DealsApiException
from hubspot.crm.quotes import ApiException as QuotesApiException
from hubspot.crm.contacts import PublicObjectSearchRequest, Filter, FilterGroup
from hubspot.crm.properties import ApiException as PropertiesApiException
from src.generalFunctions import CustomJSONEncoder


def get_all_hubspot_contacts(hubspot_client, properties):
    """
    Retrieves all HubSpot contacts using the HubSpot Python client library using pagination.

    Context:
    List

GET
/crm/v3/objects/contacts

Read a page of contacts. Control what is returned via the properties query param.

Requirements
Scopes
crm.objects.contacts.read
Limits
Standard API rate limits
Auth Methods
Parameters
int32
Query param
The maximum number of results to display per page.

DEFAULT VALUE
10
10
string
Query param
The paging cursor token of the last successfully read resource will be returned as the paging.next.after JSON property of a paged response containing more results.

+ Set test value
array
Query param
A comma separated list of the properties to be returned in the response. If any of the specified properties are not present on the requested object(s), they will be ignored.

+ Add test value
array
Query param
A comma separated list of the properties to be returned along with their history of previous values. If any of the specified properties are not present on the requested object(s), they will be ignored. Usage of this parameter will reduce the maximum number of objects that can be read by a single request.

+ Add test value
array
Query param
A comma separated list of object types to retrieve associated IDs for. If any of the specified associations do not exist, they will be ignored.

+ Add test value
boolean
Query param
Whether to return only results that have been archived.

DEFAULT VALUE
false
Request
cURLNodePHPRubyPythonC#
Copy all
1
import hubspot
2
from pprint import pprint
3
from hubspot.crm.contacts import ApiException
4
​
5
client = hubspot.Client.create(access_token="YOUR_ACCESS_TOKEN")
6
​
7
try:
8
    api_response = client.crm.contacts.basic_api.get_page(limit=10, archived=False)
9
    pprint(api_response)
10
except ApiException as e:
11
    print("Exception when calling basic_api->get_page: %s\n" % e)
Response
Example
Schema
HTTP 200
JSON
Copy all
1
{
2
  "paging": {
3
    "next": {
4
      "link": "?after=NTI1Cg%3D%3D",
5
      "after": "NTI1Cg%3D%3D"
6
    }
7
  },
8
  "results": [
9
    {
10
      "associations": {
11
        "additionalProp1": {
12
          "paging": {
13
            "next": null,
14
            "prev": {
15
              "before": "string",
16
              "link": "string"
17
            }
18
          },
19
          "results": [
20
            {
21
              "id": "string",
22
              "type": "string"
23
            }
24
          ]
25
        },
26
        "additionalProp2": {
27
          "paging": {
28
            "next": null,
29
            "prev": {
30
              "before": "string",
31
              "link": "string"
32
            }
33
          },
34
          "results": [
35
            {
36
              "id": "string",
37
              "type": "string"
38
            }
39
          ]
40
        },
41
        "additionalProp3": {
42
          "paging": {
43
            "next": null,
44
            "prev": {
45
              "before": "string",
46
              "link": "string"
47
            }
48
          },
49
          "results": [
50
            {
51
              "id": "string",
52
              "type": "string"
53
            }
54
          ]
55
        }
56
      },
57
      "createdAt": "2024-07-11T10:06:53.528Z",
58
      "archived": true,
59
      "archivedAt": "2024-07-11T10:06:53.528Z",
60
      "propertiesWithHistory": {
61
        "additionalProp1": [
62
          {
63
            "sourceId": "string",
64
            "sourceType": "string",
65
            "sourceLabel": "string",
66
            "updatedByUserId": 0,
67
            "value": "string",
68
            "timestamp": "2024-07-11T10:06:53.528Z"
69
          }
70
        ],
71
        "additionalProp2": [
72
          {
73
            "sourceId": "string",
74
            "sourceType": "string",
75
            "sourceLabel": "string",
76
            "updatedByUserId": 0,
77
            "value": "string",
78
            "timestamp": "2024-07-11T10:06:53.528Z"
79
          }
80
        ],
81
        "additionalProp3": [
82
          {
83
            "sourceId": "string",
84
            "sourceType": "string",
85
            "sourceLabel": "string",
86
            "updatedByUserId": 0,
87
            "value": "string",
88
            "timestamp": "2024-07-11T10:06:53.528Z"
89
          }
90
        ]
91
      },
92
      "id": "string",
93
      "properties": {
94
        "additionalProp1": "string",
95
        "additionalProp2": "string",
96
        "additionalProp3": "string"
97
      },
98
      "updatedAt": "2024-07-11T10:06:53.528Z"
99
    }
100
  ]
101
}
    """
    try:
        # For each page of contacts, retrieve the contacts and add them to the list of all contacts. Then get the next page. Finally, return the list of all contacts.
        # Initialise an empty list to store all contacts.
        all_contacts = []

    except ContactsApiException as e:
        print("Error:", e)
        return None


# Contact endpoints
def get_hubspot_contacts_with_http(hubspot_client, properties=None, limit=10):
    """
    Retrieves all HubSpot contacts using the HubSpot Python client library.
    :param hubspot_client: The HubSpot client instance.
    :type hubspot_client: HubSpot
    :param properties: A list of properties to retrieve for the contacts.
    :type properties: list
    :param limit: The maximum number of contacts to retrieve.
    :type limit: int
    """
    try:
        # Fetch the first page of contacts
        hubspot_contacts = hubspot_client.crm.contacts.basic_api.get_page(properties=properties, limit=limit)
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
def test_get_contacts_and_deals(hubspot_client, input_email, contact_file_name='output/hubspotContactBarryPhillips.json',
                                deal_file_name='output/hubspotContactBarryPhillips.json'):
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
