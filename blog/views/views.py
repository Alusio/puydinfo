import tempfile

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from blog.forms import SignUpForm
from blog.models import Spectacle, Quote, Image_Show, Restaurant, Image_Restaurant, Hotel, Ville, Animation, Article, \
    Calendar

tmp = tempfile.NamedTemporaryFile()

def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)

def index_off(request):
    return render(request, 'index_off.html')

def calendar(request):
    calendar = Calendar.objects.all()
    color = Calendar.objects.values('color__name', 'title').distinct()
    return render(request, 'calendar.html', {'calendar': calendar, 'color': color})

def legales(request):
    return render(request, 'legales.html')


def upload_picture(request):
    return render(request, 'upload_picture.html')

def period(request, slug):
    period = "none"
    shows = "none"

    if slug == "antiquite":
        period = "Antiquité"
        shows = Spectacle.objects.filter(theme__name=period).all()
        return render(request, 'period/antiquite.html', {'slug': period, 'shows': shows})
    if slug == "renaissance":
        period = "Renaissance"
        shows = Spectacle.objects.filter(theme__name=period).all()
        return render(request, 'period/renaissance.html', {'slug': period, 'shows': shows})
    if slug == "xxe-siecle":
        period = "XXème siècle"
        shows = Spectacle.objects.filter(theme__name=period).all()
        return render(request, 'period/xxe-siecle.html', {'slug': period, 'shows': shows})
    if slug == "belle-epoque":
        period = "Belle Epoque"
        shows = Spectacle.objects.filter(theme__name=period).all()
        return render(request, 'period/belle-epoque.html', {'slug': period, 'shows': shows})
    if slug == "grand-siecle":
        period = "Grand Siècle"
        shows = Spectacle.objects.filter(theme__name=period).all()
        return render(request, 'period/grand-siecle.html', {'slug': period, 'shows': shows})
    if slug == "moyen-age":
        period = "Moyen-Âge"
        shows = Spectacle.objects.filter(theme__name=period).all()
        return render(request, 'period/moyen-age.html', {'slug': period, 'shows': shows})

    return render(request, 'period/period.html', {'slug': period, 'shows': shows})

def articles(request, slug):
    article = Article.objects.filter(slug=slug).first()

    return render(request, 'articles.html', {'article': article})

def shows(request, slug):
    show = Spectacle.objects.filter(slug=slug, type__name__in=['Grand Spectacle', 'Spectacle Immersif'])
    quote = Quote.objects.filter(show_id=show[0].id).order_by('?').first()
    category = show[0].category.all()
    type = show[0].type.all()
    theme = show[0].theme.all()
    photos = Image_Show.objects.filter(show_id=show[0].id)
    return render(request, 'spectacles/Show.html',
                  {'show': show[0], 'quote': quote, 'category': category, 'type': type, 'photos': photos,
                   'theme': theme})


def restaurant(request, slug):
    resto = Restaurant.objects.filter(slug=slug,
                                      type__name__in=['Restaurant animé', 'Restaurant hôtel', 'Restaurant',
                                                      'Restauration rapide']).first()
    category = resto.category.all()
    type = resto.type.all()
    price = resto.price
    photos = Image_Restaurant.objects.filter(restaurant_id=resto.id)
    theme = resto.theme.all()
    return render(request, 'spectacles/Restaurant.html',
                  {'show': resto, 'category': category, 'type': type, 'photos': photos, 'price': price, 'theme': theme})


def hotel(request, slug):
    hotel = Hotel.objects.filter(slug=slug, type__name__in=['Hotel']).first()
    category = hotel.category.all()
    type = hotel.theme.all()
    price = hotel.price
    photos = Image_Restaurant.objects.filter(restaurant_id=hotel.id)
    type = hotel.type.all()
    return render(request, 'spectacles/Hotel.html',
                  {'show': hotel, 'category': category, 'type': type, 'photos': photos, 'price': price})


def animation(request, slug):
    show = Animation.objects.filter(slug=slug, type__name='Animation')
    category = show[0].category.all()
    type = show[0].type.all()
    photos = Image_Show.objects.filter(show_id=show[0].id)
    return render(request, 'spectacles/Animation.html',
                  {'show': show[0], 'category': category, 'type': type, 'photos': photos})


def ville(request, slug):
    show = Ville.objects.filter(slug=slug, type__name='Ville d\'Epoque')
    category = show[0].category.all()
    type = show[0].type.all()
    photos = Image_Show.objects.filter(show_id=show[0].id)
    return render(request, 'spectacles/Ville.html',
                  {'show': show[0], 'category': category, 'type': type, 'photos': photos})


def index_temp(request):

    return render(request, 'index_temp.html')

def SignUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            messages.success(request, 'Votre compte est bien créé')
            return redirect('/index')
        else:
            messages.error(request, 'Erreur de validation du formulaire')
    else:

        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
