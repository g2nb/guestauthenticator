from jupyterhub.auth import Authenticator
from jupyterhub.handlers.login import LoginHandler
from jupyterhub.utils import url_path_join
from random import randint
from traitlets import Unicode
from tornado import gen


class GuestHandler(LoginHandler):
    """Treat any request to login as a guest as if it were a login form submission"""

    async def get(self):
        return await self.post()


class GuestAuthenticator(Authenticator):
    """Authenticator for automatically logging in and creating a guest account for the user"""

    guest_prefix = Unicode(
        "guest_",
        help="Prefix all guest account names share",
        config=True
    )

    @gen.coroutine
    def authenticate(self, handler, data):
        """Create an account using the guest prefix and a random large integer"""
        return { "name": self.guest_prefix + str(randint(1, 100000000)) }

    def login_url(self, base_url):
        """Don't show the standard login form, automatically create a guest account instead"""
        return url_path_join(base_url, 'create')

    def get_handlers(self, app):
        """Create a guest account using the provided handler"""
        return [('/create', GuestHandler)]
