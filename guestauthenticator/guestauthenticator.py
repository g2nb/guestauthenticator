from jupyterhub.auth import Authenticator
from random import randint
from traitlets import Unicode
from tornado.concurrent import run_on_executor


class GuestAuthenticator(Authenticator):
    guest_prefix = Unicode(
        "anonymous_",
        help="Prefix all guest account names share",
        config=True
    )

    @run_on_executor
    def authenticate(self, handler, data):
        return self.guest_user + str(randint(1, 100000000))
