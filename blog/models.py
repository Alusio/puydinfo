from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse


class Type(models.Model):
    name = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name


class Theme(models.Model):
    name = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name


class Price(models.Model):
    name = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name


class Spectacle(models.Model):
    name = models.CharField(max_length=100, blank=True)
    slug = models.CharField(max_length=30, blank=True)
    content = models.TextField(blank=True)
    duration = models.IntegerField(null=True, blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    type = models.ManyToManyField(Type)
    color_title = models.ForeignKey(Color, on_delete=models.DO_NOTHING, null=True, blank=True)
    photo_banner = models.ImageField(upload_to='banner', null=True, blank=True)
    photo_home = models.ImageField(upload_to='show_hom', null=True, blank=True)
    category = models.ManyToManyField(Category)
    theme = models.ManyToManyField(Theme)
    url = models.CharField(max_length=500, blank=True)
    number = models.CharField(max_length=2, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('show', args=[str(self.slug)])


class Ville(models.Model):
    name = models.CharField(max_length=100, blank=True)
    slug = models.CharField(max_length=30, blank=True)
    content = models.TextField(blank=True)
    duration = models.IntegerField(null=True, blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    type = models.ManyToManyField(Type)
    color_title = models.ForeignKey(Color, on_delete=models.DO_NOTHING, null=True, blank=True)
    photo_banner = models.ImageField(upload_to='banner', null=True, blank=True)
    photo_home = models.ImageField(upload_to='show_hom', null=True, blank=True)
    category = models.ManyToManyField(Category)
    theme = models.ManyToManyField(Theme)
    url = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('ville', args=[str(self.slug)])


class Animation(models.Model):
    name = models.CharField(max_length=100, blank=True)
    slug = models.CharField(max_length=30, blank=True)
    content = models.TextField(blank=True)
    duration = models.IntegerField(null=True, blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    type = models.ManyToManyField(Type)
    color_title = models.ForeignKey(Color, on_delete=models.DO_NOTHING, null=True, blank=True)
    photo_banner = models.ImageField(upload_to='banner', null=True, blank=True)
    photo_home = models.ImageField(upload_to='show_hom', null=True, blank=True)
    category = models.ManyToManyField(Category)
    theme = models.ManyToManyField(Theme)
    url = models.CharField(max_length=500, blank=True)
    number = models.CharField(max_length=2, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('animation', args=[str(self.slug)])


class Restaurant(models.Model):
    name = models.CharField(max_length=100, blank=True)
    slug = models.CharField(max_length=30, blank=True)
    content = models.TextField(blank=True)
    type = models.ManyToManyField(Type)
    color_title = models.ForeignKey(Color, on_delete=models.DO_NOTHING, null=True, blank=True)
    photo_banner = models.ImageField(upload_to='banner', null=True, blank=True)
    photo_home = models.ImageField(upload_to='show_hom', null=True, blank=True)
    category = models.ManyToManyField(Category)
    theme = models.ManyToManyField(Theme)
    price = models.ForeignKey(Price, on_delete=models.DO_NOTHING, null=True, blank=True)
    num_plan = models.CharField(max_length=1, blank=True)
    price_adult = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2)
    price_child = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2)
    price_general = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2)
    exact_price = models.BooleanField(default=False)
    url = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('restaurant', args=[str(self.slug)])


class Hotel(models.Model):
    name = models.CharField(max_length=100, blank=True)
    slug = models.CharField(max_length=30, blank=True)
    content = models.TextField(blank=True)
    type = models.ManyToManyField(Type)
    color_title = models.ForeignKey(Color, on_delete=models.DO_NOTHING, null=True, blank=True)
    photo_banner = models.ImageField(upload_to='banner', null=True, blank=True)
    photo_home = models.ImageField(upload_to='show_hom', null=True, blank=True)
    category = models.ManyToManyField(Category)
    theme = models.ManyToManyField(Theme)
    price = models.ForeignKey(Price, on_delete=models.DO_NOTHING, null=True, blank=True)
    price_general = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2)
    url = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('hotel', args=[str(self.slug)])


class Image_Show(models.Model):
    show_id = models.ForeignKey(Spectacle, on_delete=models.DO_NOTHING, null=True, blank=True)
    photo = models.ImageField(upload_to='show')
    author = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.photo.name


class Image_Restaurant(models.Model):
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.DO_NOTHING, null=True, blank=True)
    photo = models.ImageField(upload_to='show')
    author = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.photo.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    show_id = models.ForeignKey(Spectacle, on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Group(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user.username


class Member(models.Model):
    group_id = models.ForeignKey(Group, on_delete=models.DO_NOTHING, null=True, blank=True)
    name = models.CharField(max_length=30, blank=True)
    age = models.IntegerField(blank=True, null=True)
    child = models.BooleanField(default=False)

    def __str__(self):
        return self.group_id.name


class Fact(models.Model):
    name = models.CharField(max_length=30, blank=True)
    show_id = models.OneToOneField(Spectacle, on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.name


class Quote(models.Model):
    name = models.CharField(max_length=30, blank=True)
    content = models.TextField(blank=True)
    author = models.CharField(max_length=100, blank=True)
    show_id = models.ForeignKey(Spectacle, on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.name


class New(models.Model):
    name = models.CharField(max_length=30, blank=True)
    content = models.TextField(blank=True)
    url = models.CharField(max_length=500, blank=True)
    date = models.DateField(blank=True, auto_now=True)

    def __str__(self):
        return self.name


class Programme(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    resultat = models.TextField(blank=True)
    resultat_im = models.TextField(blank=True)
    hor_finder = models.TextField(blank=True)
    freq_temps = models.TextField(blank=True)
    temps = models.TextField(blank=True)
    size = models.TextField(blank=True)
    restaurant_rapide = models.TextField(blank=True)
    coef_grand_show = models.TextField(blank=True)
    coef_unmissable = models.TextField(blank=True)
    date = models.DateField(blank=True, auto_now=True)
    i = models.CharField(max_length=10, blank=True)
    j = models.CharField(max_length=10, blank=True)
    k = models.CharField(max_length=10, blank=True)
    suggest = models.CharField(max_length=1, blank=True)
    number_resto_midi = models.CharField(max_length=10, blank=True)
    name_resto_midi = models.CharField(max_length=100, blank=True)
    name_show_midi = models.CharField(max_length=100, blank=True)
    price_show_midi = models.CharField(max_length=10, blank=True)
    suggest_soir = models.CharField(max_length=1, blank=True)
    number_resto_soir = models.CharField(max_length=10, blank=True)
    name_resto_soir = models.CharField(max_length=100, blank=True)
    name_show_soir = models.CharField(max_length=100, blank=True)
    price_show_soir = models.CharField(max_length=10, blank=True)
    temps_form = models.CharField(max_length=300, blank=True)
    choix = models.CharField(max_length=300, blank=True)
    temps_midi = models.CharField(max_length=300, blank=True)
    temps_debut = models.CharField(max_length=300, blank=True)
    prix_min = models.CharField(max_length=300, blank=True)
    prix_max = models.CharField(max_length=300, blank=True)
    resto_type = models.CharField(max_length=300, blank=True)
    resto = models.CharField(max_length=300, blank=True)
    select_resto_anime = models.CharField(max_length=300, blank=True)
    prix_min_soir = models.CharField(max_length=300, blank=True)
    prix_max_soir = models.CharField(max_length=300, blank=True)
    select_resto_anime_soir = models.CharField(max_length=300, blank=True)
    resto_soir = models.CharField(max_length=300, blank=True)
    resto_type_soir = models.CharField(max_length=300, blank=True)
    calculator = models.CharField(max_length=300, blank=True)
    exclus = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username


class Feed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    content = models.TextField(max_length=255, blank=True)
    date = models.DateField(blank=True, auto_now=True)
    url = models.CharField(max_length=500, blank=True)
    show_id = models.ForeignKey(Spectacle, on_delete=models.DO_NOTHING, null=True, blank=True)
    animation_id = models.ForeignKey(Animation, on_delete=models.DO_NOTHING, null=True, blank=True)
    ville_id = models.ForeignKey(Ville, on_delete=models.DO_NOTHING, null=True, blank=True)
    resto_id = models.ForeignKey(Restaurant, on_delete=models.DO_NOTHING, null=True, blank=True)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.DO_NOTHING, null=True, blank=True)
    photo_home = models.ImageField(upload_to='show_hom', null=True, blank=True)

    def __str__(self):
        return self.title


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    content = models.TextField(blank=True)
    date = models.DateField(blank=True, auto_now=True)
    slug = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.slug


class Sejour(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True)
    programme = models.ForeignKey(Programme, on_delete=models.DO_NOTHING, null=True, blank=True)
    groupe = models.ForeignKey(Group, on_delete=models.DO_NOTHING, null=True, blank=True)
    date = models.DateField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Calendar(models.Model):
    title = models.CharField(max_length=50, blank=True)
    allDay = models.BooleanField(default=False)
    start = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)
    color = models.ForeignKey(Color, on_delete=models.DO_NOTHING, null=True, blank=True)
    rendering = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.title


class Uploaded_picture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    photo = models.ImageField(upload_to='uploaded')

    def __str__(self):
        return self.title
