import os
from app.main import app as application
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
app = application
