from hubspot.hsapi import HSApi
import simplejson as json
import requests


class Templates(HSApi):

    URL = "https://api.hubapi.com/content/api/v2"

    def get_by_path(self, path):
        url = self.URL + "/templates"

        params = self.add_authentication({"path": path})

        r = requests.get(url, params=params)

        if r.status_code is 200:
            return r.json()
        else:
            return False

    def get(self, offset=0):
        url = self.URL + "/templates"

        params = self.add_authentication({"offset": offset})

        r = requests.get(url, params=params)

        if r.status_code is 200:
            return r.json()
        else:
            return False

    def create(self, data):
        url = self.URL + "/templates"

        params = self.add_authentication({})

        data = json.dumps(data)

        r = requests.post(url, params=params, data=data)

        if r.status_code is 200:
            return True
        else:
            return False

    def update(self, id, data):
        url = self.URL + "/templates/{id}".format(id=id)

        params = self.add_authentication({})

        data = json.dumps(data)

        r = requests.put(url, params=params, data=data)

        if r.status_code is 200:
            return True
        else:
            return False

    def format_post(self, data):
        translated_data = {
            "category_id": data['category_id'],
            "folder": data['folder'],
            "template_type": data['template_type'],
            "path": data['path'],
            "source": data['source']
        }

        translated_data = dict((k, v) for k, v in translated_data.items() if v)
        return translated_data