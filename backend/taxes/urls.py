from django.urls import path
from . import views


urlpatterns = [
    # path("upload/", views.get_action_column, name="data_review"),
    path("submit-email/", views.email_submit, name="submit-email"),
    path('process-csv/', views.processCSV, name='processCSV'),
    path('merge-csv/', views.merge_csv_files, name='merge_csv_files'),
]