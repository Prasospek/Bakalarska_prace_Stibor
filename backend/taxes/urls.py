from django.urls import path
from . import views


urlpatterns = [
    path("", views.csv_data_view, name="data_review"),
    path("submit-email/", views.email_submit, name="submit-email"),
]
