from django.urls import path

from . import views


urlpatterns = [
    path('nodes/<slug:uuid>', views.get_content),
    path('imports', views.import_content),
    path('delete/<slug:uuid>', views.delete_content),
]