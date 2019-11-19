from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.models import Spectacle, Restaurant, Hotel, Ville, Animation


class SpectacleSitemap(Sitemap):
    protocol = "https"

    def items(self):
        return Spectacle.objects.all()


class RestaurantSitemap(Sitemap):
    protocol = "https"

    def items(self):
        return Restaurant.objects.all()


class HotelSitemap(Sitemap):
    protocol = "https"

    def items(self):
        return Hotel.objects.all()


class AnimationSitemap(Sitemap):
    protocol = "https"

    def items(self):
        return Animation.objects.all()


class VilleSitemap(Sitemap):
    protocol = "https"

    def items(self):
        return Ville.objects.all()


class StaticViewSitemap(Sitemap):

    def items(self):
        return ['index']

    def location(self, item):
        return reverse(item)
