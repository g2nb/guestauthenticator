# guestauthenticator

**guestauthenticator** is an Authenticator plugin for JupyterHub. It allows users 
to sign into the hub anonymously. An accompanying clean-up script may then be 
configued as a JupyterHub service. This script periodically deletes the resulting 
orphaned anonymous accounts.

An example of how to configure this is below:

```python
# Set guestauthenticator as the authentication mechanism for the hub
c.JupyterHub.authenticator_class = 'guestauthenticator.GuestAuthenticator'
```
