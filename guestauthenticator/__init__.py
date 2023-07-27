"""
Anonymously sign into JupyterHub as a guest account

@author Thorin Tabor
"""

from .guestauthenticator import GuestAuthenticator

__all__ = [GuestAuthenticator]
