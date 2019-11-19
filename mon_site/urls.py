from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

import blog
from . import settings
from .sitemaps import SpectacleSitemap, RestaurantSitemap, StaticViewSitemap, HotelSitemap, AnimationSitemap, \
    VilleSitemap

sitemaps = {
    'spectacles': SpectacleSitemap,
    'restaurants': RestaurantSitemap,
    'hotels': HotelSitemap,
    'animations': AnimationSitemap,
    'villes': VilleSitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
                  path('admin/', admin.site.urls, name='admin'),
                  path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
                       name='django.contrib.sitemaps.views.sitemap'),
                  path('accounts/', include('blog.urls')),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('', include('blog.urls')),
                  path('', include('pwa.urls')),
                  path(r'auth/', include('social_django.urls', namespace='social')),
                  path('webpush/', include('webpush.urls'))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = blog.views.handler404
handler500 = blog.views.handler500
urlpatterns += staticfiles_urlpatterns()
