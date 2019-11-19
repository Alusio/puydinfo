import ast
import json
import requests
import tempfile
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect

from blog.forms import UserForm, ProfileForm, GroupForm, MemberForm, SejourForm, SejourEditForm
from blog.models import Group, Member, Sejour, Profile, Programme
from blog.views import programmation, frequentation

tmp = tempfile.NamedTemporaryFile()


@login_required
@transaction.atomic
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            prof = profile_form.save()
            prof.show_id = profile_form.cleaned_data['show']
            prof.save()

            return redirect('/index')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile, initial={'show': profile.show_id})

    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
@transaction.atomic
def group_edit(request):
    group, created = Group.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        group_form = GroupForm(request.POST, instance=group)
        if group_form.is_valid():
            group_form.save()
            gr = group_form.save()
            gr.user = request.user
            gr.name = group_form.cleaned_data['name']
            gr.save()

            return redirect('/groupe')
    else:
        group_form = GroupForm(instance=group, initial={'name': group.name})

    return render(request, 'groupe_edit.html', {
        'group_form': group_form
    })


@login_required
@transaction.atomic
def member_edit(request, pk):
    member, created = Member.objects.get_or_create(id=pk)
    if request.method == 'POST':
        member_form = MemberForm(request.POST, instance=member)
        if member_form.is_valid():
            member_form.save()
            gr = member_form.save()
            gr.name = member_form.cleaned_data['name']
            gr.age = member_form.cleaned_data['age']
            if gr.age < 13:
                gr.child = True
            gr.save()

            return redirect('/groupe')
    else:
        member_form = MemberForm(instance=member, initial={'name': member.name, 'age': member.age})

    return render(request, 'member_edit.html', {
        'member_form': member_form, 'id': member.id
    })


@login_required
@transaction.atomic
def member_delete(request, pk):
    member, created = Member.objects.get(id=pk).delete()
    return redirect('/groupe')


@login_required
@transaction.atomic
def member_add(request, pk):
    group = Group.objects.get(id=pk)
    if request.method == 'POST':
        member = Member.objects.create(group_id=group)
        member_form = MemberForm(request.POST, instance=member)
        if member_form.is_valid():
            member_form.save()
            gr = member_form.save()
            gr.group_id = group
            gr.name = member_form.cleaned_data['name']
            gr.age = member_form.cleaned_data['age']
            if gr.age < 13:
                gr.child = True
            gr.save()

            return redirect('/groupe')
    else:
        member_form = MemberForm()
    return render(request, 'member_add.html', {
        'member_form': member_form
    })


@login_required
@transaction.atomic
def group(request):
    try:
        group = Group.objects.get(user=request.user)
        member = Member.objects.filter(group_id=group).all()
    except Group.DoesNotExist:
        group = "none"
        member = "none"

    return render(request, 'groupe.html', {'group': group, 'member': member})


@login_required
@transaction.atomic
def sejour(request):
    try:
        sejours = Sejour.objects.filter(user=request.user).all()
    except Sejour.DoesNotExist:
        sejours = "none"

    return render(request, 'sejour.html', {'sejours': sejours})


@login_required
@transaction.atomic
def sejour_add(request):
    if request.method == 'POST':
        sejour = Sejour.objects.create(user=request.user)
        sejour_form = SejourForm(request.POST, instance=sejour)
        if sejour_form.is_valid():
            sejour_form.save()
            gr = sejour_form.save()
            gr.date = sejour_form.cleaned_data['date']
            gr.duration = sejour_form.cleaned_data['duration']
            gr.name = sejour_form.cleaned_data['name']
            gr.save()

            return redirect('/sejour')
    else:
        sejour_form = SejourForm()
    return render(request, 'sejour_add.html', {
        'sejour_form': sejour_form
    })


@login_required
@transaction.atomic
def sejour_edit(request, pk):
    sejour = Sejour.objects.get(id=pk)
    try:
        group = Group.objects.get(user=request.user)
    except Group.DoesNotExist:
        group = "none"

    if request.method == 'POST':
        sejour_form = SejourEditForm(request.POST, instance=sejour)
        if sejour_form.is_valid():
            sejour_form.save()
            gr = sejour_form.save()
            if group != "none":
                gr.groupe = group
            gr.name = sejour_form.cleaned_data['name']
            gr.hotel = sejour_form.cleaned_data['hotel']
            gr.save()

            return redirect('/sejour')
    else:
        sejour_form = SejourEditForm(instance=sejour,
                                     initial={'name': sejour.name, 'date': sejour.date, 'duration': sejour.duration})
    return render(request, 'sejour_edit.html', {
        'sejour_form': sejour_form, "group": group, 'id': sejour.id
    })


@login_required
@transaction.atomic
def sejour_delete(request, pk):
    sejour = Sejour.objects.get(id=pk).delete()
    return redirect('/sejour')


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            return redirect('/')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'user_update.html', {
        'user_form': user_form,
        'profile_form': profile_form

    })


@login_required
@transaction.atomic
def resultat_live(request):
    programme, created = Programme.objects.get_or_create(user=request.user)
    resultat = json.loads(programme.resultat)
    calculator = programme.calculator
    resultat_im = json.loads(programme.resultat_im)
    hor_finder = json.loads(programme.hor_finder)
    freq_temps = json.loads(programme.freq_temps)
    temps = json.loads(programme.temps)
    size = json.loads(programme.size)
    restaurant_rapide = json.loads(programme.restaurant_rapide)
    coef_unmissable = json.loads(programme.coef_unmissable)
    temps_form = programme.temps_form
    choix = programme.choix
    temps_midi = programme.temps_midi
    temps_debut = programme.temps_debut
    prix_min = programme.prix_min
    prix_max = programme.prix_max
    resto_type = programme.resto_type
    resto = programme.resto
    select_resto_anime = programme.select_resto_anime
    prix_min_soir = programme.prix_min_soir
    prix_max_soir = programme.prix_max_soir
    select_resto_anime_soir = programme.select_resto_anime_soir
    resto_soir = programme.resto_soir
    resto_type_soir = programme.resto_type_soir
    exclus = programme.exclus

    if request.method == 'GET':
        req = request.GET
        if req:
            excl = json.loads(programme.exclus)
            if int(req['exclus']) not in excl:
                excl.append(int(req['exclus']))
                programme.exclus = excl
                programme.save()

    if request.method == 'POST':
        list_freq = 'https://www.puydinfo.fr/api/info'
        list_resto = 'https://www.puydinfo.fr/api/resto'
        lists = 'https://www.puydinfo.fr/api/prog'
        req = request.POST
        response_list_freq = requests.get(list_freq)
        freq_time = response_list_freq.json()[0]["time"][0][:-9]
        response_list_resto = requests.get(list_resto)
        liste_resto = response_list_resto.json()
        freq_temps = frequentation(response_list_freq.json()[0]["freq"][0])
        response_list = requests.get(lists)
        json_list = response_list.json()

        temps_form_ = req.getlist('temps_form')

        temps_form_ = ast.literal_eval(temps_form_[0])

        choix_ = req.getlist('choix')
        choix_ = ast.literal_eval(choix_[0])

        temps_midi_ = req.getlist('temps_midi')
        temps_midi_ = ast.literal_eval(temps_midi_[0])

        temps_debut_ = ['23:23']

        prix_min_ = req.getlist('prix_min')
        prix_min_ = ast.literal_eval(prix_min_[0])

        prix_max_ = req.getlist('prix_max')
        prix_max_ = ast.literal_eval(prix_max_[0])

        resto_type_ = req.getlist('resto_type')
        resto_type_ = ast.literal_eval(resto_type_[0])

        resto_ = req.getlist('resto')
        resto_ = ast.literal_eval(resto_[0])

        select_resto_anime_ = req.getlist('select_resto_anime')
        if select_resto_anime_[0] != "none":
            select_resto_anime_ = ast.literal_eval(select_resto_anime_[0])

        prix_min_soir_ = req.getlist('prix_min_soir')
        prix_min_soir_ = ast.literal_eval(prix_min_soir_[0])

        prix_max_soir_ = req.getlist('prix_max_soir')
        prix_max_soir_ = ast.literal_eval(prix_max_soir_[0])

        select_resto_anime_soir_ = req.getlist('select_resto_anime_soir')
        if select_resto_anime_soir_[0] != "none":
            select_resto_anime_soir_ = ast.literal_eval(select_resto_anime_soir_[0])

        resto_soir_ = req.getlist('resto_soir')
        resto_soir_ = ast.literal_eval(resto_soir_[0])

        resto_type_soir_ = req.getlist('resto_type_soir')
        resto_type_soir_ = ast.literal_eval(resto_type_soir_[0])
        tab = []
        resultat_final = []
        state = 0
        select_resto_anime_ = "none"
        if resto_:
            select_resto_anime_ = req.getlist('select_resto_anime_' + resto_[0])

        select_resto_anime_soir_ = "none"
        if resto_soir_:
            select_resto_anime_soir_ = req.getlist('select_resto_anime_soir_' + resto_soir_[0])

        if calculator[0] == "1":
            state = 1
        else:
            state = 0

        for i in range(1, 10):
            for j in range(1, 3):
                for k in range(1, 3):
                    tab.append(i)
                    resultat_tmp = programmation(temps_form_, choix_, temps_midi_, temps_debut_, prix_min_, prix_max_,
                                                 resto_type_,
                                                 k, j, freq_temps, freq_time, json_list, resto_, liste_resto,
                                                 select_resto_anime_, prix_min_soir_, prix_max_soir_,
                                                 select_resto_anime_soir_, resto_soir_, resto_type_soir_, exclus)
                    if resultat_tmp != []:
                        resultat_final.append(
                            [len(resultat_tmp[0]), resultat_tmp[6], resultat_tmp, resultat_tmp[7]])
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
        programme.temps_form = temps_form
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

        programme.save()
        return redirect('/result_live')


    return render(request, 'result_live.html',
                  {'resultat': resultat, 'resultat_im': resultat_im, 'hor_finder': hor_finder,
                   'freq_temps': freq_temps, 'temps': temps, "size": size,
                   'restaurant_rapide': restaurant_rapide, 'coef_unmissable': coef_unmissable, 'programme': programme,
                   "temps_form": temps_form, "choix": choix, "temps_midi": temps_midi,
                   "temps_debut": temps_debut, "prix_min": prix_min, "prix_max": prix_max,
                   "resto_type": resto_type, "resto": resto, "select_resto_anime": select_resto_anime,
                   "prix_min_soir": prix_min_soir, "prix_max_soir": prix_max_soir,
                   "select_resto_anime_soir": select_resto_anime_soir,
                   "resto_soir": resto_soir, "resto_type_soir": resto_type_soir})
