"""
Updated: 11/07/24
Author: Daniel Potter
Description: This script synchronizes data between HubSpot and MailerLite.
It retrieves all contacts from HubSpot and all subscribers from MailerLite, then updates or creates subscribers in MailerLite based on the HubSpot data.
It can be run as a standalone script or set up as a scheduled task to run periodically.
"""
from src.emailFunctions import send_email
from src.generalFunctions import init, process_all_data, get_all_data, CustomJSONEncoder

# Wrap the main code in a try-except block to catch any unhandled exceptions.
try:
    # Initialize clients for HubSpot and MailerLite.
    # This function should set up the necessary API clients and return them.
    hubspot_client, mailerlite_api_key = init()

    # Step 1: Retrieve all HubSpot contacts and MailerLite subscribers.
    # The data is returned as a tuple of two lists.
    (all_hubspot_contacts, all_mailerlite_subscribers) = get_all_data(hubspot_client, mailerlite_api_key)

    # Output the data to a file for debugging purposes.
    with open("allHubSpotContacts.json", "w") as f:
        f.write(CustomJSONEncoder().encode(all_hubspot_contacts))
    with open("allMailerLiteSubscribers.json", "w") as f:
        f.write(CustomJSONEncoder().encode(all_mailerlite_subscribers))

    # Step 2: Update or create MailerLite subscribers with HubSpot data.
    # Todo: Uncomment the following line to enable data processing once testing is complete.
    # process_all_data(all_hubspot_contacts, all_mailerlite_subscribers, mailerlite_api_key)

    print("Data synchronization completed successfully.")

except Exception as e:
    # Define an error message to print and send in an email alert.
    error_message = f"An uncaught exception occurred in the HubSpot to MailerLite synchronization script: {e}"
    # Print the error message to the console for debugging purposes.
    print(error_message)
    # Send an email alert with the error message to the specified recipient.
    # Todo: Currently not implemented properly, uncomment to enable.
    # send_email("Script Error Alert", error_message, "alert_recipient@example.com")
