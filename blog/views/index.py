import tempfile

from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render

from blog.forms import ContactForm
from blog.models import Spectacle, New, Restaurant, Hotel, \
    Programme, Ville, Animation, Feed, Sejour

tmp = tempfile.NamedTemporaryFile()


def index(request):
    show = Spectacle.objects.filter(type__name__in=['Grand Spectacle', 'Spectacle Immersif']).order_by('?').first()
    category = show.category.all()
    type = show.type.all()
    theme_show = show.theme.all()

    resto = Restaurant.objects.filter(
        type__name__in=['Restaurant animé', 'Restaurant hôtel', 'Restaurant', 'Restauration rapide']).order_by(
        '?').first()
    category2 = resto.category.all()
    type2 = resto.type.all()
    theme_resto = resto.theme.all()
    hotel = Hotel.objects.filter(type__name='Hotel').order_by('?').first()
    category3 = hotel.category.all()
    type3 = hotel.type.all()
    theme_hotel = hotel.theme.all()
    news = New.objects.order_by('-date').all()[:3]

    animation = Animation.objects.order_by('?').all()[:2]
    ville = Ville.objects.order_by('?').all()[:2]
    date = "not"
    feeds = Feed.objects.order_by('?').all()[:3]
    feed = Feed.objects.order_by('-date').first()
    show_id = "not"
    sejour = "not"
    if request.user.is_authenticated:
        try:
            sejour = Sejour.objects.order_by('-date').filter(user=request.user).first()
        except Sejour.DoesNotExist:
            sejour = "not"

    if feed and not feed.photo_home:
        if feed.show_id:
            show_id = feed.show_id
        if feed.animation_id:
            show_id = feed.animation_id
        if feed.ville_id:
            show_id = feed.ville_id
        if feed.resto_id:
            show_id = feed.resto_id
        if feed.hotel_id:
            show_id = feed.hotel_id
    if request.user.is_authenticated:
        programme, created = Programme.objects.get_or_create(user=request.user)
        if programme.resultat == "":
            date = "none"
        else:
            date = programme.date

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            sender_name = form.cleaned_data['nom']
            sender_email = form.cleaned_data['email']

            message = "{0} has sent you a new message:\n\n{1}".format(sender_name, form.cleaned_data['message'])
            send_mail('Contact Form - Index', message, sender_email, ['contact@puydinfo.fr'])
            return HttpResponse('Merci pour votre message!')
    else:
        form = ContactForm()

    return render(request, 'index.html',
                  {'form': form, 'show': show, 'category': category, 'type': type, 'resto': resto,
                   'category2': category2, 'type2': type2, 'hotel': hotel, 'category3': category3, 'type3': type3,
                   'news': news, 'animation': animation, 'ville': ville, 'date': date, 'theme_show': theme_show[0],
                   'theme_resto': theme_resto[0], 'theme_hotel': theme_hotel[0], 'feeds': feeds, 'feed': feed,
                   'show_id': show_id, 'sejour': sejour})
