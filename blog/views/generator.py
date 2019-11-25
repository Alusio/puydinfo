import datetime
import json
import tempfile
from datetime import timedelta
from operator import itemgetter

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites import requests
from django.db import transaction
from django.shortcuts import render, redirect

from blog.models import Programme, Sejour, Spectacle, Animation

tmp = tempfile.NamedTemporaryFile()
import requests


def frequentation(id):
    number = 0
    if "1" in id:
        number = 1
    if "1N" in id:
        number = 2
    if "2" in id:
        number = 3
    if "2N" in id:
        number = 4
    if "3" in id:
        number = 5
    if "3M" in id:
        number = 6
    if "4" in id:
        number = 7
    if "4M" in id:
        number = 8
    if "4M+" in id:
        number = 9
    if "5" in id:
        number = 10
    if "6" in id:
        number = 11
    if "7" in id:
        number = 12
    if "none" in id:
        number = 400
    return number


def prog_perso(request):
    """ Si True on passe par l'api local, sinon api www.puydinfo.fr """

    """ Si True, on force les valeurs k et j dans l'algo"""
    debug_prog = False

    if debug_prog:
        lists = 'http://127.0.0.1:8000/api/prog'
    else:
        lists = 'https://www.puydinfo.fr/api/prog'

    response_list = requests.get(lists)
    liste = response_list.json()
    data_prog = []
    for list in liste:
        data_hor = []
        for hor in list['prog']:
            data_hor.append(hor['hor'])
        data_prog.append([list['id'], list['name'], list['duree'], data_hor])

    programme_custom = []
    if request.method == 'POST':
        programme, created = Programme.objects.get_or_create(user=request.user)
        req = request.POST
        temps = req.getlist('temps')
        for i, data in enumerate(data_prog):
            total = datetime.datetime.strptime(temps[i], '%H:%M') + timedelta(minutes=int(data[2]))
            total_str = total.strftime('%H:%M')
            programme_custom.append([data[0], data[1], temps[i], data[2], total_str, 0])

        programme_custom = json.dumps(programme_custom, indent=4, sort_keys=True, default=str)
        programme.resultat = programme_custom
        programme.temps = 400
        programme.size = len(programme_custom)

    return render(request, 'prog_perso.html', {'data_prog': data_prog})


def parametres(request):
    programme, created = Programme.objects.get_or_create(user=request.user)
    big_test = False
    """ Si True on passe par l'api local, sinon api www.puydinfo.fr """
    debug_mode = False

    """ Si True, on force les valeurs k et j dans l'algo"""
    debug_prog = False

    if debug_mode:
        list_freq = 'http://127.0.0.1:8000/api/info'
        list_resto = 'http://127.0.0.1:8000/api/resto'
        lists = 'http://127.0.0.1:8000/api/prog'
    else:
        list_freq = 'https://www.puydinfo.fr/api/info'
        list_resto = 'https://www.puydinfo.fr/api/resto'
        lists = 'https://www.puydinfo.fr/api/prog'

    if big_test:
        response_list_freq = requests.get(list_freq)
        response_list_resto = requests.get(list_resto)
        freq_time = response_list_freq.json()[0]["time"][0][:-9]
        prev_time = datetime.datetime.strptime(freq_time, '%d/%m/%Y')

        liste_resto = response_list_resto.json()
        sejour_ok = False
        spectacle = Spectacle.objects.filter(type__name="Programme").union(Animation.objects.filter(type__name="Programme"))

    if request.user.is_authenticated and big_test:
        try:
            sejour = Sejour.objects.order_by('-date').filter(user=request.user).first()
        except Sejour.DoesNotExist:
            sejour = "not"

        if sejour:
            intervalle = sejour.date + datetime.timedelta(days=sejour.duration)
            dt = datetime.datetime.combine(sejour.date, datetime.datetime.min.time())
            dt2 = datetime.datetime.combine(intervalle, datetime.datetime.min.time())
            if prev_time >= dt and prev_time <= dt2:
                sejour_ok = True

    if request.method == 'POST' and big_test:
        req = request.POST
        choix = req.getlist('show')
        temps = req.getlist('temps')
        temps_midi = req.getlist('temps_midi')
        temps_debut = req.getlist('temps_debut')
        visited = req.getlist('visited')
        calculator = req.getlist('calculator')
        resto_type = req.getlist('choix2')
        resto = req.getlist('restaurant')
        price = req.getlist('price')
        resto_type_soir = req.getlist('choix2_soir')
        resto_soir = req.getlist('restaurant_soir')
        price_soir = req.getlist('price_soir')
        prix_min = 0
        prix_max = 50
        prix_min_soir = 0
        prix_max_soir = 50

        """ On set la fourchette d eprix pour le resto du midi"""
        if price:
            if price[0] == '1':
                prix_min = 0
                prix_max = 10
            if price[0] == '2':
                prix_min = 10
                prix_max = 20
            if price[0] == '3':
                prix_min = 20
                prix_max = 50
            if price[0] == '4':
                prix_min = 0
                prix_max = 50

        select_resto_anime = "none"
        if resto:
            select_resto_anime = req.getlist('select_resto_anime_' + resto[0])

        """ On set la fourchette d eprix pour le resto du soir"""
        if price_soir:
            if price_soir[0] == '1':
                prix_min_soir = 0
                prix_max_soir = 10
            if price_soir[0] == '2':
                prix_min_soir = 10
                prix_max_soir = 20
            if price_soir[0] == '3':
                prix_min_soir = 20
                prix_max_soir = 50
            if price_soir[0] == '4':
                prix_min_soir = 0
                prix_max_soir = 50

        select_resto_anime_soir = "none"
        if resto_soir:
            select_resto_anime_soir = req.getlist('select_resto_anime_soir_' + resto_soir[0])

        freq_temps = frequentation(response_list_freq.json()[0]["freq"][0])
        response_list = requests.get(lists)
        json_list = response_list.json()

        if len(choix) == 0:
            messages.error(request, 'Veuillez choisir au moins UN spectacle !')
            return render(request, 'outil_parametre.html')
        tab = []
        resultat_final = []
        state = 0

        if calculator[0] == "1":
            state = 1
        else:
            state = 0
        exclus = '[]'
        if not debug_prog:
            for i in range(1, 10):
                for j in range(1, 3):
                    for k in range(1, 3):
                        tab.append(i)
                        resultat_tmp = programmation(temps, choix, temps_midi, temps_debut, prix_min, prix_max,
                                                     resto_type,
                                                     k, j, freq_temps, freq_time, json_list, resto, liste_resto,
                                                     select_resto_anime, prix_min_soir, prix_max_soir,
                                                     select_resto_anime_soir, resto_soir, resto_type_soir, exclus)
                        if resultat_tmp != []:
                            resultat_final.append(
                                [len(resultat_tmp[0]), resultat_tmp[6], resultat_tmp, resultat_tmp[7]])
        else:
            resultat_tmp = programmation(temps, choix, temps_midi, temps_debut, prix_min, prix_max,
                                         resto_type,
                                         1, 0, freq_temps, freq_time, json_list, resto, liste_resto,
                                         select_resto_anime, prix_min_soir, prix_max_soir,
                                         select_resto_anime_soir, resto_soir, resto_type_soir, exclus)
            if resultat_tmp != []:
                resultat_final.append([len(resultat_tmp[0]), resultat_tmp[6], resultat_tmp, resultat_tmp[7]])

        if resultat_tmp == []:
            return redirect('/planner')
        if state == 1:
            index_max = resultat_final.index(max(resultat_final, key=lambda x: x[1]))
            max_value = resultat_final[index_max][1]
            enum = []
            for p in range(len(resultat_final)):
                if resultat_final[p][1] == max_value:
                    enum.append(p)
            tmp = []

            for p in range(len(enum)):
                tmp.append(resultat_final[enum[p]])

            resultat_index = tmp.index(max(tmp, key=lambda x: x[3]))

            resultat = tmp[resultat_index][2]

        else:
            resultat_index = resultat_final.index(max(resultat_final, key=lambda x: x[0]))
            resultat = resultat_final[resultat_index][2]

        """ On enregistre en bdd le resultat de programmation """
        programme.resultat = json.dumps(resultat[0], indent=4, sort_keys=True, default=str)
        programme.resultat_im = json.dumps(resultat[1], indent=4, sort_keys=True, default=str)
        programme.hor_finder = json.dumps(resultat[2], indent=4, sort_keys=True, default=str)
        programme.freq_temps = json.dumps(resultat[3], indent=4, sort_keys=True, default=str)
        programme.temps = json.dumps(resultat[4], indent=4, sort_keys=True, default=str)
        programme.size = json.dumps(len(resultat[0]), indent=4, sort_keys=True, default=str)
        programme.restaurant_rapide = json.dumps(resultat[5], indent=4, sort_keys=True, default=str)
        programme.coef_unmissable = json.dumps(resultat[7], indent=4, sort_keys=True, default=str)
        programme.coef_grand_show = json.dumps(resultat[6], indent=4, sort_keys=True, default=str)
        programme.number_resto_midi = json.dumps(resultat[8], indent=4, sort_keys=True, default=str)
        programme.name_resto_midi = json.dumps(resultat[9], indent=4, sort_keys=True, default=str)
        programme.k = json.dumps(resultat[10], indent=4, sort_keys=True, default=str)
        programme.j = json.dumps(resultat[11], indent=4, sort_keys=True, default=str)
        programme.suggest = json.dumps(resultat[12], indent=4, sort_keys=True, default=str)
        programme.name_show_midi = json.dumps(resultat[13], indent=4, sort_keys=True, default=str)
        programme.price_show_midi = json.dumps(resultat[14], indent=4, sort_keys=True, default=str)

        programme.suggest_soir = json.dumps(resultat[15], indent=4, sort_keys=True, default=str)
        programme.number_resto_soir = json.dumps(resultat[16], indent=4, sort_keys=True, default=str)
        programme.name_resto_soir = json.dumps(resultat[17], indent=4, sort_keys=True, default=str)
        programme.name_show_soir = json.dumps(resultat[18], indent=4, sort_keys=True, default=str)
        programme.price_show_soir = json.dumps(resultat[19], indent=4, sort_keys=True, default=str)
        programme.temps_form = temps
        programme.choix = choix
        programme.temps_midi = temps_midi
        programme.temps_debut = temps_debut
        programme.prix_min = prix_min
        programme.prix_max = prix_max
        programme.resto_type = resto_type
        programme.resto = resto
        programme.select_resto_anime = select_resto_anime
        programme.prix_min_soir = prix_min_soir
        programme.prix_max_soir = prix_max_soir
        programme.select_resto_anime_soir = select_resto_anime_soir
        programme.resto_soir = resto_soir
        programme.resto_type_soir = resto_type_soir
        programme.calculator = calculator
        programme.exclus = []

        programme.save()
        return redirect('/programme')

    return render(request, 'outil_parametre.html')
    """return render(request, 'outil_parametre.html',
                  {'temps': prev_time, 'liste_resto': liste_resto, 'sejour': sejour, 'sejour_ok': sejour_ok,
                   'spectacle': spectacle})"""


@login_required
@transaction.atomic
def resultat(request):
    programme, created = Programme.objects.get_or_create(user=request.user)
    resultat = json.loads(programme.resultat)
    resultat_im = json.loads(programme.resultat_im)
    hor_finder = json.loads(programme.hor_finder)
    freq_temps = json.loads(programme.freq_temps)
    temps = json.loads(programme.temps)
    size = json.loads(programme.size)
    restaurant_rapide = json.loads(programme.restaurant_rapide)
    coef_unmissable = json.loads(programme.coef_unmissable)
    return render(request, 'result.html',
                  {'resultat': resultat, 'resultat_im': resultat_im, 'hor_finder': hor_finder,
                   'freq_temps': freq_temps, 'temps': temps, "size": size,
                   'restaurant_rapide': restaurant_rapide, 'coef_unmissable': coef_unmissable, 'programme': programme})


def programmation(temps, choix, temps_midi, temps_debut, prix_min, prix_max, resto_type, nb_tab, nb_start,
                  freq_temps, freq_time, json_list, restaurant, liste_resto, select_resto_anime, prix_min_soir,
                  prix_max_soir, select_resto_anime_soir, resto_soir, resto_type_soir, exclus_):
    """Version 10"""
    abort = False
    ret = []
    programme = []
    """Liste des show à ne surtout aps manquer"""
    unmissable = ["1", "2", "5", "6"]

    """Liste des grands spectacles"""
    grand_show = ["1", "2", "3", "4", "5", "6"]

    """Liste des shows immersifs"""
    special_show = ["10", "18", "19", "8"]

    """Liste des show exclus - On enlève par défaut le 7 (Orgues de Feu)"""
    exclus = ['7']
    tab = json.loads(exclus_)
    for ex in tab:
        exclus.append(str(ex))

    programme_immersif = []
    hor_finder = []


    """On cherche le nombre de séance pour chaque show"""
    nb_horaires = []
    for json_ in json_list:
        nb_horaires.append([json_['id'], len(json_['prog']), json_['name'], json_['prog'], json_['duree']])

    if temps_debut[0] == "23:23":
        """temps_debut[0] = datetime.datetime.now().time().strftime('%H:%M')"""
        temps_debut[0] = "12:35"

    """Définition des matrices pour les distances et l'importance des shows"""
    distance = []
    importance = []
    distance_rapide = []
    restaurants = []

    """ Matrice des distances pour les shows"""
    distance.append(['1', '2', '3', '4', '5', '6', '8', '9', '10', '11', '12', '13', '14', '18', '19'])
    distance.append([0, 1, 4, 10, 12, 9, 12, 2, 5, 11, 6, 7, 11, 3, 8])
    distance.append([2, 0, 4, 10, 12, 9, 12, 1, 5, 11, 6, 7, 11, 3, 8])
    distance.append([3, 2, 0, 9, 11, 8, 11, 1, 5, 10, 7, 2, 10, 4, 6])
    distance.append([11, 10, 9, 0, 4, 3, 2, 10, 6, 1, 7, 5, 1, 8, 4])
    distance.append([11, 10, 9, 3, 0, 3, 2, 10, 6, 1, 7, 5, 1, 8, 4])
    distance.append([8, 7, 9, 2, 6, 0, 5, 7, 3, 3, 2, 2, 3, 4, 1])
    distance.append([11, 10, 9, 3, 2, 4, 0, 10, 6, 1, 7, 5, 1, 8, 4])
    distance.append([2, 1, 4, 10, 12, 9, 12, 0, 5, 11, 6, 7, 11, 8, 3])
    distance.append([8, 4, 8, 6, 9, 4, 10, 5, 0, 7, 1, 5, 7, 2, 3])
    distance.append([12, 11, 10, 2, 4, 5, 3, 11, 7, 0, 8, 6, 1, 9, 5])
    distance.append([11, 7, 12, 6, 11, 3, 10, 7, 1, 9, 0, 5, 9, 2, 4])
    distance.append([9, 8, 3, 2, 10, 2, 7, 8, 4, 5, 6, 0, 5, 4, 1])
    distance.append([12, 11, 10, 2, 4, 5, 3, 11, 7, 1, 8, 6, 0, 9, 5])
    distance.append([4, 2, 5, 9, 12, 8, 11, 3, 1, 10, 3, 6, 10, 0, 7])
    distance.append([9, 8, 10, 4, 7, 1, 6, 8, 2, 5, 2, 3, 5, 4, 0])

    """ Matrice d'importance pour les shows"""
    importance.append(['1', '2', '3', '4', '5', '6', '8', '9', '10', '11', '12', '13', '14', '18', '19'])
    importance.append([1, 1, 1, 1, 1, 1, 13, 10, 11, 16, 14, 15, 16, 12, 12])

    """ Matrice de distance pour les restaurants (TOUS les restaurants)"""
    distance_rapide.append(['1', '2', '3', '4', '5', '6', '8', '9', '10', '11', '12', '13', '14', '18', '19'])
    distance_rapide.append([5, 2, 6, 10, 13, 9, 12, 3, 2, 11, 4, 7, 11, 1, 8])
    distance_rapide.append([12, 11, 10, 4, 1, 4, 3, 11, 7, 2, 8, 6, 2, 9, 5])
    distance_rapide.append([12, 8, 13, 7, 12, 4, 11, 8, 2, 10, 1, 6, 10, 3, 5])
    distance_rapide.append([12, 8, 13, 7, 12, 4, 11, 8, 1, 10, 1, 6, 10, 3, 5])
    distance_rapide.append([3, 2, 5, 11, 13, 10, 13, 1, 6, 12, 7, 8, 12, 9, 4])
    distance_rapide.append([12, 8, 13, 7, 12, 4, 11, 8, 1, 10, 1, 6, 10, 3, 5])
    distance_rapide.append([4, 3, 1, 10, 12, 9, 12, 2, 6, 11, 8, 3, 11, 5, 7])
    distance_rapide.append([13, 12, 4, 3, 5, 6, 4, 12, 8, 1, 9, 7, 2, 10, 6])
    distance_rapide.append([10, 9, 4, 3, 11, 3, 8, 9, 5, 6, 7, 1, 6, 5, 2])
    distance_rapide.append([4, 3, 1, 10, 12, 9, 12, 2, 6, 11, 8, 3, 11, 5, 7])
    distance_rapide.append([9, 5, 9, 7, 10, 5, 11, 6, 1, 8, 2, 6, 8, 3, 4])
    distance_rapide.append([12, 11, 10, 4, 1, 4, 3, 11, 7, 2, 8, 6, 2, 9, 5])
    distance_rapide.append([9, 5, 9, 7, 10, 5, 11, 6, 1, 8, 2, 6, 8, 3, 4])
    distance_rapide.append([12, 11, 10, 4, 1, 4, 3, 11, 7, 2, 8, 6, 2, 9, 5])
    distance_rapide.append([10, 9, 11, 5, 8, 2, 7, 9, 3, 6, 3, 4, 6, 5, 1])
    distance_rapide.append([10, 9, 11, 5, 8, 2, 7, 9, 3, 6, 3, 4, 6, 5, 1])
    distance_rapide.append([12, 11, 10, 1, 5, 4, 3, 11, 7, 2, 8, 6, 2, 9, 5])
    distance_rapide.append([4, 3, 1, 10, 12, 9, 12, 2, 6, 11, 8, 3, 11, 5, 7])

    """ Matrice de correspondance de la lettre, noms et prix des restaurants (TOUS les restaurants)"""
    restaurants.append(["I", "A", "B", "J", "K", "C", "L", "D", "M", "E", "N", "F", "O", "G", "P", "H", "R", "S"], )
    restaurants.append(
        ["Le Rendez-vous des ventres Faims", "Le Cafe de la Madelon", "Le Relais de poste", "La Rotissoire",
         "La Popina", "L Auberge", "Le Fort de l An Mil", "Le Bistrot", "La Queue de l Etang", "La Taverne", "L Etape",
         "L Orangerie", "La Maison du Prefou", "L Echansonnerie", "Le Garde-Manger", "La Mijoterie du Roy Henri",
         "La Gargoulette", "L Estaminet"])
    restaurants.append(
        [12.40, 26.90, 23.80, 13.50, 9.90, 41, 9.90, 21, 9.90, 7, 10.50, 16.90, 10.90, 20.50, 9.90, 15.50, 9.90, 9.90])

    """ Définition de la liste des restaurants par catégorie"""
    restaurants_rapide = ['I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'R', 'S']
    restaurants_classique = ['C', 'D', 'E', 'F', 'G', 'H']
    restaurants_anime = ['A', 'B']

    """ Détermine la liste des restaurants pour la suggestion midi"""
    if resto_type[0] == '3' and restaurant[0] == "none_anime":
        choix_resto = restaurants_anime
    if resto_type[0] == '3' and restaurant[0] == "none_classique":
        choix_resto = restaurants_classique
    if resto_type[0] == '2' and restaurant[0] == "none_rapide":
        choix_resto = restaurants_rapide
    if resto_type[0] == '4':
        choix_resto = restaurants[0]

    """ Détermine la liste des restaurants pour la suggestion soir"""
    if resto_type_soir[0] == '3' and resto_soir[0] == "none_anime":
        choix_resto_soir = restaurants_anime
    if resto_type_soir[0] == '3' and resto_soir[0] == "none_classique":
        choix_resto_soir = restaurants_classique
    if resto_type_soir[0] == '2' and resto_soir[0] == "none_rapide":
        choix_resto_soir = restaurants_rapide
    if resto_type_soir[0] == '4':
        choix_resto_soir = restaurants[0]

    """programme[id show, name show, date deb, duree, date fin]"""
    """On ajoute en priorité les shows avec une seule séance"""
    for i in range(len(nb_horaires)):
        if nb_horaires[i][1] == 1 and nb_horaires[i][0] in choix and nb_horaires[i][3][0]['hor'] >= temps_debut[0] and \
                nb_horaires[i][0] not in exclus:
            total = datetime.datetime.strptime(nb_horaires[i][3][0]['hor'], '%H:%M') + timedelta(
                minutes=int(nb_horaires[i][4]))
            open_time = datetime.datetime.strptime(nb_horaires[i][3][0]['hor'], '%H:%M') + timedelta(
                minutes=-30)
            programme.append(
                [nb_horaires[i][0], nb_horaires[i][2], nb_horaires[i][3][0]['hor'], nb_horaires[i][4],
                 total.time(), 0, open_time.time()])
            exclus.append(nb_horaires[i][0])

    exclus_copy = exclus.copy()
    mini = "20:00"
    index_hor = 0
    index_k = 0
    find_first = False

    """On cherche la première séance"""
    for _ in range(nb_start):

        mini = "20:00"
        index_hor = 0
        index_k = 0
        for i in range(len(nb_horaires)):
            if nb_horaires[i][1] != 1 and nb_horaires[i][0] not in exclus_copy \
                    and nb_horaires[i][0] in choix and nb_horaires[i][0] in grand_show:
                for k in range(len(nb_horaires[i][3])):

                    if mini >= nb_horaires[i][3][k]['hor'] >= temps_debut[0]:
                        mini = nb_horaires[i][3][k]['hor']
                        index_hor = i
                        index_k = k
                        find_first = True
        exclus_copy.append(nb_horaires[index_hor][0])

    if find_first:
        """Ajout de la première séance au programme"""
        total = datetime.datetime.strptime(nb_horaires[index_hor][3][index_k]['hor'], '%H:%M') + timedelta(
            minutes=int(nb_horaires[index_hor][4]))
        open_time = datetime.datetime.strptime(nb_horaires[index_hor][3][index_k]['hor'], '%H:%M') + timedelta(
            minutes=-30)

        programme.append(
            [nb_horaires[index_hor][0], nb_horaires[index_hor][2], nb_horaires[index_hor][3][index_k]['hor'],
             nb_horaires[index_hor][4], total.time(), 0, open_time.time()])
        exclus.append(nb_horaires[index_hor][0])
    else:
        abort = True

    if not abort:
        number_resto_midi = "none"
        name_resto_midi = "none"
        number_of_resto = 0

        number_resto_soir = "none"
        name_resto_soir = "none"

        """Ajout d'un restaurant à table pour le midi"""
        if select_resto_anime != "none" and resto_type[0] != "4":
            for json_ in liste_resto:
                if json_['id'] == restaurant[0] and json_['category'] == 0:
                    total_ = datetime.datetime.strptime(select_resto_anime[0], '%H:%M') + timedelta(
                        minutes=60)
                    programme.append(
                        [json_['id'], json_['name'], select_resto_anime[0], '60', total_.time(), 2])
                    number_resto_midi = json_['id']
                    name_resto_midi = json_['name']
                    number_of_resto += 1

        """Ajout d'un restaurant à table pour le soir"""
        if select_resto_anime_soir != "none" and resto_type_soir[0] != "4":
            for json_ in liste_resto:
                if json_['id'] == resto_soir[0] and json_['category'] == 0:
                    total_ = datetime.datetime.strptime(select_resto_anime_soir[0], '%H:%M') + timedelta(
                        minutes=60)
                    programme.append(
                        [json_['id'], json_['name'], select_resto_anime_soir[0], '60', total_.time(), 2])
                    number_resto_soir = json_['id']
                    name_resto_soir = json_['name']
                    number_of_resto += 1

        """Triage du programme par l'horaire"""
        programme = sorted(programme, key=itemgetter(2))
        show_restaurant = []
        show_restaurant_soir = []
        show_restaurant = programme[0]

        """On parcours la boucle 10 fois pour être certain de couvrir tous les shows"""
        retour = parcours(temps_midi, temps, nb_horaires, programme, special_show, exclus, distance, choix,
                          importance,
                          total, 10, nb_tab, restaurants, show_restaurant, distance_rapide, show_restaurant_soir,
                          number_of_resto)
        show_restaurant = retour[0]
        programme = retour[1]
        show_restaurant_soir = retour[2]

        """Triage du programme par l'horaire"""
        programme = sorted(programme, key=itemgetter(2))

        """Récupère les données des specatcles immersifs"""
        for i in range(len(nb_horaires)):
            immersif_debut2 = 0
            immersif_fin2 = 0
            if nb_horaires[i][0] in special_show:

                if len(nb_horaires[i][3]) > 2:
                    immersif_debut = nb_horaires[i][3][0]['hor']
                    immersif_fin = nb_horaires[i][3][1]['hor']

                    immersif_debut2 = nb_horaires[i][3][2]['hor']
                    immersif_fin2 = nb_horaires[i][3][3]['hor']

                else:
                    immersif_debut = nb_horaires[i][3][0]['hor']
                    immersif_fin = nb_horaires[i][3][1]['hor']

                if len(nb_horaires[i][3]) > 2:
                    programme_immersif.append(
                        [nb_horaires[i][0], nb_horaires[i][2], nb_horaires[i][4], immersif_debut, immersif_fin,
                         immersif_debut2,
                         immersif_fin2])
                else:
                    programme_immersif.append(
                        [nb_horaires[i][0], nb_horaires[i][2], nb_horaires[i][4], immersif_debut, immersif_fin])

        """Détection des trous de 50 min dans la journée"""
        find_space(nb_horaires, programme, hor_finder)

        decalage = 0
        hor_finder_copy = hor_finder.copy()
        continu = []
        programme_copy = programme.copy()

        """Pour chaque temps libres trouvés dans hor_finder, on va calculer le score des shows continus 
        et on ajoute le best score"""
        find_immersif(hor_finder, distance, programme_copy, special_show, importance, programme_immersif, exclus,
                      programme, decalage, continu, choix, restaurants, distance_rapide)

        """Ajout des orgues de feu s'il est présent"""
        for j in range(len(nb_horaires)):
            if nb_horaires[j][0] == "7" and nb_horaires[j][0] in choix:
                total = datetime.datetime.strptime(nb_horaires[j][3][0]['hor'], '%H:%M') + timedelta(
                    minutes=int(nb_horaires[j][4]))

                programme.append(
                    [nb_horaires[j][0], nb_horaires[j][2],
                     nb_horaires[j][3][0]['hor'],
                     nb_horaires[j][4], total.time(), 0])

        """On enlève de programme_immersif les shows qui ne sont pas programmés"""
        continu_index = []
        for i in reversed(range(len(programme_immersif))):
            if programme_immersif[i][0] not in continu:
                continu_index.append(i)
        for i in range(len(continu_index)):
            del programme_immersif[continu_index[i]]

        """On va faire une suggestion de restaurant pour le midi"""
        somme_rest_rapide = []
        restaurant_rapide = [999]
        suggest = 0
        exclus_rapide = []
        if len(resto_type) != 0:
            if resto_type[0] == "4" or (resto_type[0] == '2' and restaurant[0] == "none_rapide") or (
                    resto_type[0] == '3' and restaurant[0] == "none_classique") or (
                    resto_type[0] == '3' and restaurant[0] == "none_anime"):
                for json_ in liste_resto:
                    suggest = 1
                    for i in range(len(distance_rapide[0])):
                        if show_restaurant[0] == distance_rapide[0][i]:
                            index_rapide = i

                    for j in range(len(restaurants[2])):
                        if restaurants[0][j] in choix_resto:
                            if prix_min <= restaurants[2][j] <= prix_max and restaurants[0][j] not in exclus_rapide:
                                somme_rest_rapide.append([distance_rapide[j + 1][index_rapide], j])

                    index_rest_rapide_j = somme_rest_rapide.index(min(somme_rest_rapide))
                    index_rest_rapide_name = somme_rest_rapide[index_rest_rapide_j][1]
                    if json_['id'] == restaurants[0][index_rest_rapide_name]:
                        if '08:00' <= json_['prog'][0]['hor'] <= '15:00':
                            restaurant_rapide = [restaurants[0][index_rest_rapide_name],
                                                 restaurants[1][index_rest_rapide_name],
                                                 restaurants[2][index_rest_rapide_name], show_restaurant[1]]
                            number_resto_midi = restaurants[0][index_rest_rapide_name]
                            name_resto_midi = restaurants[1][index_rest_rapide_name]
                        else:
                            exclus_rapide.append(restaurants[0][index_rest_rapide_name])

        show_name_resto = "none"
        price_resto_midi = "none"
        if restaurant_rapide != [999]:
            show_name_resto = restaurant_rapide[3]
            price_resto_midi = restaurant_rapide[2]

        """On va faire une suggestion de restaurant pour le soir"""
        somme_rest_rapide_soir = []
        restaurant_rapide_soir = [999]
        suggest_soir = 0
        exclus_rapide_soir = []
        if len(resto_type_soir) != 0:
            if resto_type_soir[0] == "4" or (resto_type_soir[0] == '2' and resto_soir[0] == "none_rapide") or (
                    resto_type_soir[0] == '3' and resto_soir[0] == "none_classique") or (
                    resto_type_soir[0] == '3' and resto_soir[0] == "none_anime"):
                for json_ in liste_resto:
                    suggest_soir = 1
                    for i in range(len(distance_rapide[0])):
                        if show_restaurant_soir[0] == distance_rapide[0][i]:
                            index_rapide_soir = i

                    for j in range(len(restaurants[2])):
                        if restaurants[0][j] in choix_resto_soir:
                            if prix_min_soir <= restaurants[2][j] <= prix_max_soir and restaurants[0][j] \
                                    not in exclus_rapide_soir:
                                somme_rest_rapide_soir.append([distance_rapide[j + 1][index_rapide_soir], j])

                    index_rest_rapide_j = somme_rest_rapide_soir.index(min(somme_rest_rapide_soir))
                    index_rest_rapide_name = somme_rest_rapide_soir[index_rest_rapide_j][1]
                    if json_['id'] == restaurants[0][index_rest_rapide_name]:
                        if '08:00' <= json_['prog'][0]['hor'] <= '15:00':
                            restaurant_rapide_soir = [restaurants[0][index_rest_rapide_name],
                                                      restaurants[1][index_rest_rapide_name],
                                                      restaurants[2][index_rest_rapide_name], show_restaurant_soir[1]]
                            number_resto_soir = restaurants[0][index_rest_rapide_name]
                            name_resto_soir = restaurants[1][index_rest_rapide_name]
                        else:
                            exclus_rapide_soir.append(restaurants[0][index_rest_rapide_name])

        show_name_resto_soir = "none"
        price_resto_soir = "none"
        if restaurant_rapide_soir != [999]:
            show_name_resto_soir = restaurant_rapide_soir[3]
            price_resto_soir = restaurant_rapide_soir[2]

        """On fait le calcul des coefs"""
        info = []
        incontournable = grand_show + special_show
        for w in range(len(programme)):
            info.append(programme[w][0])
        info_data = [value for value in info if value in incontournable]
        info_unmissable = [value for value in info if value in unmissable]
        coef_grand_show = len(info_data) * 100 / len(info)
        coef_unmissable = len(info_unmissable) * 100 / len(info)

        """ Retour de la fonction"""
        ret = [programme, programme_immersif, hor_finder_copy, freq_temps, freq_time, restaurant_rapide,
               coef_grand_show, coef_unmissable, number_resto_midi, name_resto_midi, nb_tab, nb_start, suggest,
               show_name_resto, price_resto_midi, suggest_soir, number_resto_soir, name_resto_soir,
               show_name_resto_soir,
               price_resto_soir]
    return ret


def find_immersif(hor_finder, distance, programme_copy, special_show, importance, programme_immersif, exclus, programme,
                  decalage, continu, choix, restaurants, distance_rapide):
    for i in range(len(hor_finder)):
        passer_duree = True
        for _ in range(hor_finder[i][4]):
            passer = True
            resto_prog = False
            tab_somme = []
            tab_index_show = 0
            for j in range(len(distance[0])):
                if programme_copy[hor_finder[i][3] - 1][0] == distance[0][j]:
                    tab_index_show = j + 1
                    resto_prog = False
                else:
                    for k in range(len(restaurants[0])):
                        if programme_copy[hor_finder[i][3] - 1][0] == restaurants[0][k]:
                            tab_index_show = k
                            resto_prog = True

            for l in range(len(special_show)):
                if not resto_prog:
                    for k in range(len(distance[tab_index_show])):
                        if special_show[l] == distance[0][k]:
                            tab_somme.append([special_show[l], distance[tab_index_show][k] + importance[1][k]])
                else:
                    for k in range(len(distance_rapide[tab_index_show])):
                        if special_show[l] == distance_rapide[0][k]:
                            tab_somme.append([special_show[l], distance_rapide[tab_index_show][k] + importance[1][k]])

            tab_somme = sorted(tab_somme, key=itemgetter(1))

            for a in range(len(tab_somme)):
                if passer and passer_duree:
                    for b in range(len(programme_immersif)):

                        if tab_somme[a][0] == programme_immersif[b][0] and tab_somme[a][0] not in exclus and \
                                tab_somme[a][0] in choix:

                            if len(programme_immersif[b]) > 5:
                                duree = timedelta(minutes=int(programme_immersif[b][2]))
                                if duree >= timedelta(minutes=30):
                                    passer_duree = False

                                hor_deb = datetime.datetime.strptime(programme_immersif[b][3], '%H:%M')
                                hor_fin = datetime.datetime.strptime(programme_immersif[b][4], '%H:%M')
                                hor_deb2 = datetime.datetime.strptime(programme_immersif[b][5], '%H:%M')
                                hor_fin2 = datetime.datetime.strptime(programme_immersif[b][6], '%H:%M')
                                if hor_finder[i][3] >= len(programme_copy):
                                    fin = datetime.datetime.strptime("22:00", '%H:%M')
                                else:
                                    fin = datetime.datetime.strptime(programme_copy[hor_finder[i][3]][2], '%H:%M')
                                deb_tmp = programme_copy[hor_finder[i][3] - 1][4]
                                deb = datetime.datetime.combine(datetime.date(1, 1, 1), deb_tmp)
                                plus = timedelta(minutes=10)

                                if (hor_deb <= fin - duree - plus) and (
                                        hor_fin >= deb + duree + plus) \
                                        or (hor_deb2 <= fin - duree - plus) and (
                                        hor_fin2 >= deb + duree + plus):
                                    exclus.append(tab_somme[a][0])
                                    programme.insert(
                                        hor_finder[i][3] + decalage,
                                        [tab_somme[a][0],
                                         programme_immersif[b][1], 0,
                                         programme_immersif[b][2], 0, 1])
                                    continu.append(tab_somme[a][0])
                                    decalage += 1
                                    passer = False
                            else:

                                hor_deb = datetime.datetime.strptime(programme_immersif[b][3], '%H:%M')
                                hor_fin = datetime.datetime.strptime(programme_immersif[b][4], '%H:%M')
                                deb_tmp = programme_copy[hor_finder[i][3] - 1][4]
                                deb = datetime.datetime.combine(datetime.date(1, 1, 1), deb_tmp)
                                duree = timedelta(minutes=int(programme_immersif[b][2]))
                                plus = timedelta(minutes=10)
                                if duree >= timedelta(minutes=30):
                                    passer_duree = False

                                if hor_finder[i][3] >= len(programme_copy):
                                    fin = datetime.datetime.strptime("22:00", '%H:%M')
                                else:
                                    fin = datetime.datetime.strptime(programme_copy[hor_finder[i][3]][2], '%H:%M')

                                if (hor_deb <= fin - duree - plus) and (
                                        hor_fin >= deb + duree + plus):
                                    exclus.append(tab_somme[a][0])
                                    programme.insert(
                                        hor_finder[i][3] + decalage,
                                        [tab_somme[a][0],
                                         programme_immersif[b][1], 0,
                                         programme_immersif[b][2], 0, 1])
                                    continu.append(tab_somme[a][0])
                                    decalage += 1
                                    passer = False


def find_space(nb_horaires, programme, hor_finder):
    max_test = nb_horaires[nb_horaires.index(max(nb_horaires))][3]
    max_val = max_test[-1]['hor']
    value = 1
    for i in range(len(programme)):
        if 0 < i < len(programme) - 1:
            hor_finder1 = datetime.datetime.strptime(programme[i][2], '%H:%M')
            hor_finder2_time = programme[i - 1][4].strftime('%H:%M')
            hor_finder2 = datetime.datetime.strptime(hor_finder2_time, '%H:%M')
            elapsed = hor_finder1 - hor_finder2
            if elapsed >= timedelta(minutes=50):
                if str(elapsed)[:-3] >= "1:00":
                    temps_affichage = str(elapsed)[:-6] + " h " + str(elapsed)[2:-3] + " min"
                else:
                    temps_affichage = str(elapsed)[2:-3] + " min"
                if str(elapsed)[:-3] >= "1:15":
                    value = 2
                else:
                    value = 1

                hor_finder.append([programme[i - 1][1], programme[i][1], temps_affichage, i, value])
        elif i != 0:
            hor_finder2_time = programme[i][4].strftime('%H:%M')
            hor_finder2 = datetime.datetime.strptime(hor_finder2_time, '%H:%M')
            if hor_finder2.time() <= datetime.time(21, 30):
                hor_finder1 = datetime.datetime.strptime("21:30", '%H:%M')
                elapsed = hor_finder1 - hor_finder2
                if str(elapsed)[:-3] >= "1:00":
                    temps_affichage = str(elapsed)[:-6] + " h " + str(elapsed)[2:-3] + " min"
                else:
                    temps_affichage = str(elapsed)[2:-3] + " min"

                hor_finder.append([programme[i][1], "Fin de journée", temps_affichage, i + 1, value])


def parcours(temps_midi, temps, nb_horaires, programme, special_show, exclus, distance, choix, importance, total1,
             nb_boucle, nb_tab, restaurants, show_restaurant, distance_rapide, show_restaurant_soir, number_of_resto):
    nb_pop = 1
    index_prog = 0
    failed = False
    number_done = False
    for _ in range(nb_boucle):
        if failed:
            index_prog = -1
        programme = sorted(programme, key=itemgetter(2))
        total = datetime.datetime.strptime(programme[index_prog][2], '%H:%M') + timedelta(
            minutes=int(programme[index_prog][3]))
        total_deb_str = '23:00'
        if not failed:
            if (index_prog + 1) < len(programme):
                total_deb = datetime.datetime.strptime(programme[index_prog + 1][2], '%H:%M') - timedelta(minutes=30)
                total_deb_str = total_deb.strftime('%H:%M')

        """Si l'heure du dernier show est entre 12h et 13h, on set la variable temps_midi"""
        if datetime.time(13) >= total.time() >= datetime.time(12):
            heure_midi = int(temps_midi[0])
        else:
            heure_midi = 0

        """Set des temps delta"""
        time_90 = total + timedelta(minutes=160) + timedelta(minutes=heure_midi) + timedelta(
            minutes=int(temps[0]))
        time_90_str = time_90.strftime('%H:%M')
        total_str = (total + timedelta(minutes=int(temps[0])) + timedelta(minutes=heure_midi)).strftime(
            '%H:%M')

        hor_find = []

        """On cherche les spectacles avec les prochaines séances dans les 90 prochaines minutes"""
        for i in range(len(nb_horaires)):

            passer = True
            if nb_horaires[i][1] != 1 and nb_horaires[i][0] not in exclus \
                    and nb_horaires[i][0] in choix and nb_horaires[i][0] not in special_show:

                for k in range(len(nb_horaires[i][3])):
                    duree_show = datetime.datetime.strptime(nb_horaires[i][3][k]['hor'], '%H:%M') + timedelta(
                        minutes=int(nb_horaires[i][4]))
                    duree_show_str = duree_show.strftime('%H:%M')

                    if time_90_str >= nb_horaires[i][3][k][
                        'hor'] >= total_str and passer and duree_show_str <= total_deb_str:
                        hor_find.append(nb_horaires[i][0])
                        passer = False
                        failed = False

        """Si on ne trouve plus d'horaires on break"""
        if len(hor_find) == 0 and failed == True:
            break

        if len(hor_find) == 0:
            failed = True

        if not failed:
            """On cherche dans distance la bonne ligne"""
            index_show = 0
            resto_prog = False
            for i in range(len(distance[0])):
                if distance[0][i] == programme[-1][0]:
                    index_show = i + 1
                    resto_prog = False
                else:
                    for j in range(len(restaurants)):
                        if restaurants[0][j] == programme[-1][0]:
                            index_show = j
                            resto_prog = True

            """On cherche pour chaque show sa distance"""
            index_show_cal = 0
            score = []

            """On va calculer pour chaque show un score"""
            for k in range(len(hor_find)):
                if not resto_prog:
                    for j in range(len(distance[0])):
                        if distance[0][j] == hor_find[k]:
                            index_show_cal = j
                else:
                    for j in range(len(restaurants[0])):
                        if restaurants[0][j] == hor_find[k]:
                            index_show_cal = j
                somme_show = 0
                score_time = 0
                valider = True
                time_next_str = ""
                for i in range(len(nb_horaires)):
                    if nb_horaires[i][0] == hor_find[k]:
                        for l in range(len(nb_horaires[i][3])):
                            if nb_horaires[i][3][l]['hor'] >= total_str:
                                somme_show += 1
                                if valider:
                                    time_next_str = nb_horaires[i][3][l]['hor']
                                    valider = False

                """Définition d'un score en fonction du temps du next show"""
                time_next = datetime.datetime.strptime(time_next_str, '%H:%M')
                time_diff = time_next - total
                if time_diff >= timedelta(hours=2):
                    score_time = 11
                if timedelta(hours=1, minutes=20) <= time_diff <= timedelta(hours=2):
                    score_time = 8
                if timedelta(hours=1) <= time_diff <= timedelta(hours=1, minutes=30):
                    score_time = 5
                if timedelta(minutes=20) <= time_diff <= timedelta(minutes=40):
                    score_time = 3
                if timedelta(minutes=40) <= time_diff <= timedelta(hours=1):
                    score_time = 1

                """Score = score distance + score importance + somme des show restants + score temps"""
                if not resto_prog:
                    score_temp = distance[index_show][index_show_cal] + importance[1][
                        index_show_cal] + somme_show + score_time
                else:
                    score_temp = distance_rapide[index_show + 1][index_show_cal] + importance[1][
                        index_show_cal] + somme_show + score_time

                score.append(score_temp)

            """On regarde le score le plus faible et on l'ajoute au programme"""
            nb_pop = nb_tab

            for _ in range(nb_pop):
                if len(score) >= 2:
                    best_score_index = score.index(min(score))
                    best_score_id = hor_find[best_score_index]
                    score.pop(best_score_index)
                    hor_find.pop(best_score_index)

                elif (len(score) == 1):
                    best_score_index = score.index(min(score))
                    best_score_id = hor_find[best_score_index]
                    score.pop(best_score_index)
                    hor_find.pop(best_score_index)

            valider_show = True
            index_k = 0
            index_show = 0

            for i in range(len(nb_horaires)):

                if nb_horaires[i][0] == best_score_id:
                    index_show = i
                    for l in range(len(nb_horaires[i][3])):
                        if nb_horaires[i][3][l]['hor'] >= total_str:
                            if valider_show:
                                index_k = l
                                valider_show = False
                        total = datetime.datetime.strptime(nb_horaires[i][3][index_k]['hor'], '%H:%M') + timedelta(
                            minutes=int(nb_horaires[i][4]))
            open_time = datetime.datetime.strptime(nb_horaires[index_show][3][index_k]['hor'], '%H:%M') + timedelta(
                minutes=-30)
            programme.append(
                [nb_horaires[index_show][0], nb_horaires[index_show][2], nb_horaires[index_show][3][index_k]['hor'],
                 nb_horaires[index_show][4], total.time(), 0, open_time.time()])
            exclus.append(nb_horaires[index_show][0])

            """ Si on a trouver un shows on augmenter l'index prog"""
            if not failed:
                index_prog += 1

            """ Si on a deux resto à table dans le programme, un fait un increment supp"""
            if number_of_resto == 2 and not number_done:
                index_prog += 1
                number_done = True

        """ Si le show est entre 12h et 13h, c'est le show du midi"""
        if datetime.time(13) >= total.time() >= datetime.time(12):
            show_restaurant = programme[-1]

        """ Si le show est entre 19h et 21h, ou 18h et 21h, c'est le show du midi"""
        if datetime.time(21) >= total.time() >= datetime.time(19):
            show_restaurant_soir = programme[-1]
        if show_restaurant_soir == []:
            if datetime.time(21) >= total.time() >= datetime.time(18):
                show_restaurant_soir = programme[-1]

    """ Si on a pas de show pour le restaurant du soir, on prend le dernier show"""
    if show_restaurant_soir == []:
        show_restaurant_soir = programme[-1]

    ret = [show_restaurant, programme, show_restaurant_soir]
    return ret
