from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from .routers import router

# Set the administrative site header
admin.site.site_title = "Ironman Stats Admin"
admin.site.site_header = "Ironman Stats Admin Panel"

# Wire up our API using automatic URL routing.
# Additionally, include login URLs for the browsable API.
urlpatterns = [

    # DRF Routes
    url(r'^', include(router.urls)),

    # Django Admin Routes
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
