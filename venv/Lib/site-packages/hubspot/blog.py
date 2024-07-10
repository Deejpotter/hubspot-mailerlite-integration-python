from hubspot.hsapi import HSApi
import simplejson as json
import requests


class Blog:

    def __init__(self, parent):
        self.cms = CMS(parent)
        self.cos = COS(parent)


class CMS(HSApi):
    BASE_URL = "https://api.hubapi.com/blog/v1"

    def get_posts(self, guid, offset):
        url = self.BASE_URL + "/{guid}/posts.json".format(guid=guid)

        params = self.add_authentication({"offset": offset})

        r = requests.get(url, params=params)

        if r.status_code is 200:
            return r.json()
        else:
            return False

    def get_blog_list(self):
        url = self.BASE_URL + "/list.json"

        params = self.add_authentication({})

        r = requests.get(url, params=params)

        if r.status_code is 200:
            return r.json()
        else:
            return False

    @staticmethod
    def to_cos(data, target_portal, blog_title):
        author_id = target_portal.blog.cos.get_author_id(data['authorEmail'])
        blog = target_portal.blog.cos.get_blog(blog_title)
        translated_data = {
            "blog_author_id": author_id,
            "content_group_id": blog['objects'][0]['id'],
            "is_draft": data['draft'],
            "meta_description": data['metaDescription'],
            "meta_keywords": data['metaKeywords'],
            "name": data['title'],
            "post_body": data['body'],
            "post_summary": data['summary'],
            "publish_date": data['publishTimestamp'],
        }
        translated_data = dict((k, v) for k, v in translated_data.items() if v)
        return translated_data


class COS(HSApi):
    BASE_URL = "https://api.hubapi.com/content/api/v2"

    def get_blog_posts(self, offset, name=None):
        url = self.BASE_URL + "/blog-posts"

        if name is not None:
            params = self.add_authentication({"offset": offset, "name": name})
        else:
            params = self.add_authentication({"offset": offset})

        r = requests.get(url, params=params)

        if r.status_code is 200:
            return r.json()
        else:
            return False

    def update(self, id, data):
        url = self.BASE_URL + "/blog-posts/{id}".format(id=id)

        params = self.add_authentication({})

        data = json.dumps(data)

        r = requests.put(url, params=params, data=data)

        if r.status_code is 200:
            print(r.text)
            return True
        else:
            print(r.status_code)
            return False

    def create(self, data):
        url = self.BASE_URL + "/blog-posts"

        params = self.add_authentication({})

        data = json.dumps(data)

        r = requests.post(url, params=params, data=data)

        if r.status_code is 200:
            return True
        else:
            return False

    def get_author_id(self, email):
        url = self.BASE_URL + "/blog-authors"

        params = self.add_authentication({"email": email})

        r = requests.get(url, params=params)

        if r.status_code is 200:
            return r.json()['objects'][0]['id']
        else:
            return False

    def get_blog(self, name):
        url = self.BASE_URL + "/blogs"

        params = self.add_authentication({"name": name})

        r = requests.get(url, params=params)

        if r.status_code is 200:
            return r.json()
        else:
            return False