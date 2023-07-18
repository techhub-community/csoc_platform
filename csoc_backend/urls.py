from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from user import views
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='landing/index.html'), name='index'),
    path('submit-contact/', views.submit_contact, name='submit_contact'),
    path('user/', include('user.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += [
    # API base url
    path('api/v1/', include([
        # users API
        path('dsa/', include('dsa.urls')),
        path('user/', include('user.apis.urls')),
        ]),
    ),
]
