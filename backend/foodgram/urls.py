from django.contrib import admin
from django.urls import include, path

api_paths = [
    path('', include('users.urls', namespace='api_users')),
    path('', include('recipes.urls', namespace='api'))
]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_paths)),
]
