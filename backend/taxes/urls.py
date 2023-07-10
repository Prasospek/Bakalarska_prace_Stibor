from django.urls import path
from . import views


urlpatterns = [
    path("", views.csv_data_view, name="data_review"),
    path("test/", views.test, name="test"),
]
