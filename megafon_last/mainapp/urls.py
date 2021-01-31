from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
    path('', views.post_number, name='post_number')
]
# urlpatterns = [
#     path('', mainapp.main, name='main'),
#     path('admin/', admin.site.urls),
# ]
