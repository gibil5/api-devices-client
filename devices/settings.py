import os
from distutils.util import strtobool

AUTH0_URL = "https://electric-staging.auth0.com/oauth/token"
AUTH0_AUDIENCE = "https://electric-staging.auth0.com/api/v2/"
AUTH0_CLIENT_ID = "JdUofZPSNp418Dq8MeHIke5kZpPaZY60"
AUTH0_CLIENT_SECRET = "Fc6jioQzvJNfeO_d6zfhsCBoicS5cUzUZpK3gOum2HNMYpm7kzdOsaSylN0ipgvs"

# AUTH0
#AUTH0_URL = os.getenv("AUTH0_URL")
#AUTH0_GRANT_TYPE = 'client_credentials'
#AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE")
#AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
#AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_URL = AUTH0_URL
AUTH0_GRANT_TYPE = 'client_credentials'
AUTH0_AUDIENCE = AUTH0_AUDIENCE
AUTH0_CLIENT_ID = AUTH0_CLIENT_ID
AUTH0_CLIENT_SECRET = AUTH0_CLIENT_SECRET
