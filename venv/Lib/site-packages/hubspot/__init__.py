from .forms import Forms
from .contacts import Contacts
from .properties import Properties
from .files import Files
from .blog import Blog
from .pages import Pages
from .templates import Templates
import requests
from delorean import Delorean


class HubSpot:

    def __init__(self, **kwargs):
        self.client_secret = kwargs.get("client_secret")
        self.client_id = kwargs.get("client_id")
        self.app = False
        self.authorization = "hapikey"
        self.portal_id = kwargs.get("portal_id")

        if self.client_id is not None or self.client_secret is not None:
            if self.client_id is None or self.client_secret is None:
                raise SyntaxError(
                    "Both Client_id and client_secret are required for HubSpot app initilization"
                )
            self.app = True
            self.authorization = "access_token"
            self.refresh_token = kwargs.get("refresh_token")

            if self.refresh_token is None:
                raise SyntaxError(
                    "You must provide a refresh_token along with access_token"
                )

        self.auth_value = kwargs.get(self.authorization)

        if self.auth_value is None:
            raise SyntaxError(
                "You must include a hapi_key or access_token attribute when initalizing the API"
            )

        if self.portal_id is None:
            raise SyntaxError(
                "You did not provide the portal_id required parameter."
            )

        self.forms = Forms(self)
        self.contacts = Contacts(self)
        self.properties = Properties(self)
        self.files = Files(self)
        self.blog = Blog(self)
        self.pages = Pages(self)
        self.templates = Templates(self)

    def get_new_token(self):
        """
        Check if the access token has expired. If it has, use the refresh token
        to revalidate the portal.
        """

        url = "https://api.hubapi.com/auth/v1/refresh"

        data = {
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "grant_type": "refresh_token"
        }

        r = requests.post(url, data=data)

        if r.status_code != 200:
            return False

        data = r.json()

        self.access_token = data["access_token"]
        self.refresh_token = data["refresh_token"]

        params = {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires_at": int(data["expires_in"]) + int(Delorean().epoch())
        }

        return params
