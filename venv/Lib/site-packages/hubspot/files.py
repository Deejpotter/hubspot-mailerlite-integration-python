import simplejson as json
import requests
import math
from .hsapi import HSApi, HAPIError


class Files(HSApi):

    BASE_URL = "https://api.hubapi.com/content/api/v2/files"
    FOLDERS = "https://api.hubapi.com/content/api/v2/folders"

    def upload_new_file(self, filename, folders=None, overwrite="false"):
        params = self.add_authentication({})

        data = {"overwrite": overwrite}

        if folders is not None:
            data['folder_paths'] = folders

        files = {"files": open(filename, 'rb')}

        r = requests.post(self.BASE_URL, params=params, data=data, files=files)

        if r.status_code in [200, 201]:
            response = r.json()
            return response['objects'][0]
        else:
            raise HAPIError(
                message="New File Post Failed",
                response=r.text,
                code=r.status_code
            )

    def delete_all(self, type="files"):

        all_meta = self.get_all_metadata(type=type)

        all_deleted = True

        base_url = self.BASE_URL if type == "files" else self. FOLDERS

        for file in all_meta:
            url = base_url + "/{fileid}".format(fileid=file["id"])

            r = requests.delete(url, params=self.add_authentication({}))

            if r.status_code in range(200, 299):
                continue

            all_deleted = False

        return all_deleted


    def get_all_metadata(self, type="files", params=None):

        allowed_params = [
            "alt_key",
            "archived",
            "created",
            "deleted_at",
            "extension",
            "folder_id",
            "id",
            "name",
            "type",
            "parent_folder_id"
        ]

        if params is not None:
            params = {key: value for (key, value) in params.items() if any(key.startswith(param) for param in allowed_params)}
        else:
            params = {}

        params['limit'] = 20

        metadata = []

        url = self.BASE_URL if type == "files" else self.FOLDERS

        total = self.get_total(url, params)

        for page in range(1, (math.ceil(total / 20) + 1)):
            metadata.extend(self.get_page(url, page, params))

        return metadata

    def get_total(self, url, params):

        params = self.add_authentication(params)
        r = requests.get(url, params=params)

        if r.status_code == 200:
            response = r.json()
            return response["total_count"]
        else:
            raise HAPIError(
                message="Get Total Files failed",
                response=r.text,
                code=r.status_code
            )

    def get_page(self, url, page, params):

        params['offset'] = params['limit'] * (page - 1)

        params = self.add_authentication(params)

        r = requests.get(url, params=params)

        if r.status_code == 200:
            response = r.json()
            return response["objects"]
        else:
            raise HAPIError(
                message="Get page failed",
                response=r.text,
                code=r.status_code
            )

    def get_folder_path(self, id):

        if id is None:
            return None

        url = self.FOLDERS + "/{id}/".format(id=id)

        params = self.add_authentication({})
        r = requests.get(url, params=params)

        if r.status_code == 200:
            response = r.json()
            return response["full_path"]
        else:
            raise HAPIError(
                message="Get folder path failed",
                response=r.text,
                code=r.status_code
            )

    def create_folder(self, name, parent_id=None):

        data = {"name": name}

        if parent_id is not None:
            data["parent_folder_id"] = parent_id

        r = requests.post(self.FOLDERS, params=self.add_authentication({}), data=json.dumps(data))

        if r.status_code in range(200, 300):
            response = r.json()
            return response


        return False