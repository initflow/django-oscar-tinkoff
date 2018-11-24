from django.conf.urls import url
from .views import  NotificationView


urlpatterns = [
    url(r'^authorize/', NotificationView.as_view(), name='creditcards-authorize'),
]
