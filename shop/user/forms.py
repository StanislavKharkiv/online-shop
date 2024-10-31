from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from django import forms
from django.forms.widgets import PasswordInput, TextInput


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    groups = forms.ModelChoiceField(
        queryset=Group.objects.all(),  # Single selection of one group
        widget=forms.Select(
            attrs={"class": "input"}
        ),  # Simple select widget for one group
        required=True,  # Ensure that selection of one group is required
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "groups")
        widgets = {
            "username": forms.TextInput(attrs={"class": "input"}),
            "email": forms.EmailInput(attrs={"class": "input"}),
            "password1": forms.PasswordInput(attrs={"class": "input"}),
            "password2": forms.PasswordInput(attrs={"class": "input"}),
        }

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields["password1"].widget = forms.PasswordInput(attrs={"class": "input"})
        self.fields["password2"].widget = forms.PasswordInput(attrs={"class": "input"})

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def save(self, commit=True):
        # Save the user instance first
        user = super(CreateUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()

        # After saving the user, assign the group (must be a list or iterable)
        selected_group = self.cleaned_data.get("groups")
        if selected_group:
            user.groups.set([selected_group])

        return user


class ProfileForm(forms.ModelForm):

    # groups = forms.ModelChoiceField(
    #     queryset=Group.objects.all(),
    #     required=False,
    #     widget=forms.Select(attrs={"class": "input"}),
    # )

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "groups")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.email = self.cleaned_data["email"]
    #     if commit:
    #         user.save()
    #     return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())
