import json
from src.generalFunctions import init
from src.generalFunctions import CustomJSONEncoder
from src.hubspotFunctions import test_get_contacts_and_deals, search_hubspot_contact_by_email_with_properties, get_all_contact_properties, get_hubspot_contacts_with_http

# Initialize clients
hubspot_client, mailerlite_api_key = init()

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
