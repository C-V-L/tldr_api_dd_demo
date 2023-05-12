"""
URL configuration for TLDR_Directory project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

from django.urls import include, path
from rest_framework import routers
from TLDR_Backend_API_App.views import MyModelViewSet  # replace with your app's ViewSet

router = routers.DefaultRouter()
router.register(r'root_page', MyModelViewSet)  # replace 'my-model' with your preferred endpoint

urlpatterns = [
    path('', include(router.urls)),
]