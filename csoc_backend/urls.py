from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django.views.generic import TemplateView
from .views import IndexTemplateView as ITV

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ITV.as_view(), name='index'),
    path('user/', include('user.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
