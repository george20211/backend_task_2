from django.urls import path
from .views import (OrgListViewSet,
                    DownloadViewSet,
                    ClientListViewSet)


urlpatterns = [
    path('org', OrgListViewSet.as_view({'get': 'list'})),
    path('load', DownloadViewSet.as_view({'post': 'get_filename'})),
    path('client', ClientListViewSet.as_view({'get': 'list'})),
]