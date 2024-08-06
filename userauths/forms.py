from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User, Profile


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Full name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Confirm Password"}))
    institution = forms.ChoiceField(choices=[
        ('Crest View', 'Crest View'),
        ('All Saint Clinic', 'All Saint Clinic'),
        ('NOHL', 'NOHL'),
    ], widget=forms.Select(attrs={"class": "form-control"}), required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'institution']



class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Full Name"}))
    bio = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Bio"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Phone"}))
    institution = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Institution"}))
    
    class Meta:
        model = Profile
        fields = ['full_name', 'image', 'bio', 'phone', 'institution']
