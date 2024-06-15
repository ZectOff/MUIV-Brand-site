from django.urls import path

from main import views


app_name = "main"

urlpatterns = [
    path("", views.index, name="home"),
    path("about", views.about, name="about"),
    path("news", views.news, name="news"),
    path("support", views.support, name="support"),
    path("testing", views.testing, name="testing"),  # page for debugging and testing code
]


# ngrok http http://localhost:8000