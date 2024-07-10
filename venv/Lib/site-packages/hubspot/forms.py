import simplejson as json
import requests
from .hsapi import HSApi


class Forms(HSApi):

    BASE_URL = "https://api.hubapi.com/contacts/v1/forms"

    def submit(self, guid, fields, context):

        if not isinstance(fields, dict):
            raise SyntaxError("Field Data should be in a dictionary format")

        if not isinstance(context, dict):
            raise SyntaxError("Context data should be in dictionary format")
        elif not fields.get("email"):
            if not (context.get("hutk") or context.get("ipAddress")):
                raise SyntaxError(
                    "Not enough data to identify a lead, please include an email address"
                    " in the field dictionary or a hubspot user token"
                )
        fields['hs_context'] = json.dumps(context)

        url = "https://forms.hubspot.com/uploads/form/v2/{portalid}/{formid}"

        r = requests.post(url.format(
            portalid=self.credentials.portal_id,
            formid=guid),
            data=fields,
        )

        if r.status_code == 204:
            return True
        else:
            return r.text

    def create(self, name, fields, **kwargs):
        if not isinstance(fields, dict):
            raise SyntaxError("Field Data should be in a dictionary format")

        properties = self.credentials.properties
        property_list = properties.get_all()
        form_fields = []

        for field, options in fields.items():
            prop = properties.get(field, target=property_list)
            if prop is not False:
                form_fields.append(prop)
            else:
                options["name"] = field
                form_fields.append(options)

        form_data = {
            "name": name,
            "action": "",
            "method": "POST",
            "cssClass": "hs-form stacked",
            "redirect": "",
            "submitText": "Sign Up",
            "followUpId": "",
            "leadNurturingCampaignId": "",
            "notifyRecipients": "",
            "embeddedCode": "",
            "fields": form_fields
        }

        for key, value in kwargs.items():
            form_data[key] = value

        params = self.add_authentication({})
        r = requests.post(self.BASE_URL, params=params, data=json.dumps(form_data))

        if r.status_code == 200:
            return r.json()["guid"]
        elif r.status_code == 409:
            return r.json()
        else:
            raise SyntaxError(
                "Create form post request responded with {code} {text}".format(
                    code=r.status_code,
                    text=r.text
                )
            )

    def get(self, guid):
        url = self.BASE_URL + "/{guid}".format(guid=guid)

        params = self.add_authentication({})

        r = requests.get(url, params=params)

        if r.status_code == 200:
            return r.json()
        else:
            return False
