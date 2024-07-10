from hubspot.hsapi import HSApi
import simplejson as json
import requests


class Pages(HSApi):

    BASE_URL = "https://api.hubapi.com/content/api/v2"

    def get_by_name(self, name):
        url = self.BASE_URL + "/pages"

        params = self.add_authentication({"name": name})

        r = requests.get(url, params=params)

        if r.status_code is 200:
            return r.json()
        else:
            return False

    def get_by_id(self, id):
        url = self.BASE_URL + "/pages/{id}".format(id=id)

        params = self.add_authentication({})

        r = requests.get(url, params=params)

        if r.status_code is 200:
            return r.json()
        else:
            return False

    def get_all(self, offset=0):
        url = self.BASE_URL + "/pages"

        params = self.add_authentication({"offset": offset})

        r = requests.get(url, params=params)

        if r.status_code is 200:
            return r.json()
        else:
            return False

    def update(self, id, data):
        url = self.BASE_URL + "/pages/{id}".format(id=id)

        params = self.add_authentication({})

        data = json.dumps(data)

        r = requests.put(url, params=params, data=data)

        if r.status_code is 200:
            return True
        else:
            return False

    def create(self, data):
        url = self.BASE_URL + "/pages"

        params = self.add_authentication({})

        data = json.dumps(data)

        r = requests.post(url, params=params, data=data)

        if r.status_code is 200:
            return True
        else:
            return False

    def format_post(self, data):
        translated_data = {
            "campaign": data['campaign'],
            "campaign_name": data['campaign_name'],
            "footer_html": data['footer_html'],
            "head_html": data['head_html'],
            "is_draft": data['is_draft'],
            "meta_description": data['meta_description'],
            "meta_keywords": data['meta_keywords'],
            "name": data['name'],
            "password": data['password'],
            "publish_date": data['publish_date'],
            "slug": data['slug'],
            "subcategory": data['subcategory'],
            "template_path": data['template_path'],
            "widget_containers": data['widget_containers'],
            "widgets": data['widgets']
        }

        translated_data = dict((k, v) for k, v in translated_data.items() if v)
        return translated_data