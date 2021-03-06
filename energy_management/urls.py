"""energy_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from rest_framework.urlpatterns import format_suffix_patterns

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.urls import path, reverse_lazy

from energy_tracker.views import (
    AllStatusView,
    AllStatusTimeView,
    DeviceStatusView,
    DeviceStatusTimeView,
    TempView,
    TrackerListView,
    export_csv_view,
)
from energy_management.views import (
    AboutView,
    DashboardView,
)


urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('dashboard'))),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('about/', AboutView.as_view(), name="about"),
    path('admin/', admin.site.urls),
    path('entry/', TrackerListView.as_view()),
    path('post/', TempView.as_view()),
    path('status/', AllStatusView.as_view()),
    path('status/<str:device>/', DeviceStatusView.as_view()),
    path('status/<int:hour>/<int:minute>/<str:date>/', AllStatusTimeView.as_view()),
    path('status/<str:device>/<int:hour>/<int:minute>/<str:date>/', DeviceStatusTimeView.as_view()),
    path('csv/', export_csv_view, name="download_csv"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns = format_suffix_patterns(urlpatterns)
