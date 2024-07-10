import simplejson as json
import requests
from .hsapi import HSApi


class Contacts(HSApi):
    BASE_URL = "https://api.hubapi.com/contacts/v1/contact/"

    @classmethod
    def get_name(self):
        return "Contacts"

    def get_contact_by_email(self, email, **kwargs):
        url = self.BASE_URL + "/email/{email}/profile".format(email=email)
        params = self.add_authentication({})
        r = requests.get(url, params=params)

        if r.status_code == 200:
            return r.json()
        else:
            return r.text

    def update_contact(self, contact_id, fields):
        headers = {'content-type': 'application/json'}

        #Set id to VID if arg was a string
        if isinstance(contact_id, basestring):
            contact_id = self.get_contact_by_email(contact_id)["vid"]

        url = self.BASE_URL + "vid/{vid}/profile".format(contact_id)

        if not isinstance(fields, dict):
            raise SyntaxError("Fields should be a dictionary")

        properties = []

        """
        Convert the dictionary passed in as fields into properties
        """
        for field, value in fields.iteritems():
            properties.append({"property": field, "value": value})

        properties = {"properties": properties}

        params = self.add_authentication({})

        r = requests.post(
            url,
            data=json.dumps(properties),
            params=params,
            headers=headers
        )

        if r.status_code is 204:
            return True
        else:
            return r.text

    def batch_update(self, contact_batch):
        headers = {'content-type': 'application/json'}

        url = self.BASE_URL + "batch"
        
        batch = []

        for contact in contact_batch:
            if isinstance(contact, dict): 
                property_list = []               
                for field, value in contact.items():
                    property_list.append({"property": field, "value": value})
                batch.append({"email": contact.get('email'), "properties": property_list})
                del(property_list)
            else:
                raise SyntaxError("Contact should be a dictionary")

        params = self.add_authentication({})

        r = requests.post(
            url,
            data=json.dumps(batch),
            params=params,
            headers=headers
        )

        if r.status_code is 204:
            return True
        else:
            return r.text