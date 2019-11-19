from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from snowpenguin.django.recaptcha3.fields import ReCaptchaField

from .models import Profile, Sejour, Spectacle, Member, Group, Hotel, Uploaded_picture


class ContactForm(forms.Form):
    nom = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(widget=forms.PasswordInput, label='Mot de passe',
                                help_text='Le mot de passe doit contenir au moins 8 caractères.<br> Il ne peut pas '
                                          'être une de vos données personnelles, <br>ni un mot de passe commun et '
                                          'encore moins une suite de chiffres.')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirmer le mot de passe')
    terms = forms.BooleanField(help_text="J'accepte les conditions d'uilisation"

                               ,
                               error_messages={'required': 'You must accept the terms and conditions'},
                               label="Conditions"
                               )
    captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'terms')
        labels = {
            'username': _('Pseudo'),
        }
        help_texts = {
            'username': _('Seulement des lettres.'),
        }


class UserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False,
                                 help_text='',
                                 label='Prénom')

    class Meta:
        model = User
        fields = ('first_name', 'email')

class ProfileForm(forms.ModelForm):
    show = forms.ModelChoiceField(queryset=Spectacle.objects.all(), label='Spectacle favori',
                                  widget=forms.Select(attrs={'class': "form-control"}))

    class Meta:
        model = Profile
        fields = ('show',)


class GroupForm(forms.ModelForm):
    name = forms.CharField(max_length=30, required=True, label="Nom du groupe")

    class Meta:
        model = Group
        fields = ('name',)


class MemberForm(forms.ModelForm):
    name = forms.CharField(max_length=30, required=True, label="Nom")
    age = forms.IntegerField(required=True, label="Âge")

    class Meta:
        model = Member
        fields = ('name', 'age')


class SejourForm(forms.ModelForm):
    name = forms.CharField(max_length=30, required=True, label="Nom")
    date = forms.DateField(
        widget=DatePickerInput(options={
            "format": 'DD/MM/YY',
            "locale": "fr"
        }), label="Date du séjour"
    )
    duration = forms.IntegerField(required=True, label="Durée (en jours)")
    class Meta:
        model = Sejour
        fields = ('name', 'date', 'duration')


class SejourEditForm(forms.ModelForm):
    name = forms.CharField(max_length=30, required=True, label="Nom")
    hotel = forms.ModelChoiceField(queryset=Hotel.objects.all(), label='Hotel',
                                   widget=forms.Select(attrs={'class': "form-control"}), required=False)

    class Meta:
        model = Sejour
        fields = ('name', 'hotel')


class UploadPictureForm(forms.Form):
    title = forms.CharField(max_length=50)
    photo = forms.FileField()

    class Meta:
        model = Uploaded_picture
        fields = ('title', 'photo')
