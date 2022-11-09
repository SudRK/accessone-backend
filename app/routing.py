from django.urls import path
from app.consumer import *


websocket_url_pattern = [
    path('ws/api/accessone/', AccessOne.as_asgi())
]