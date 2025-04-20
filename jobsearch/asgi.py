
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from .routing import application as websocket_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobsearch.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": websocket_application
})
