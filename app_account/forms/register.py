from django import forms

from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
User = get_user_model()


class RegisterForm(forms.Form):
    firstName = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter your first name'}))
    lastName = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter your last name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter your username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter your email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'}))
    terms = forms.BooleanField(required=True, error_messages={
        'required': 'You must agree to the terms.'})

    @staticmethod
    def validate_name(name):
        if name.startswith(' ') or name.endswith(' '):
            raise ValidationError("Name should not start or end with a space.")
        words = name.split(' ')
        for word in words:
            if not word.isalpha():
                raise ValidationError(
                    "Name can only contain letters and single spaces between words.")
        return name

    def clean_firstName(self):
        first_name = self.cleaned_data.get('firstName')
        return self.validate_name(first_name)

    def clean_lastName(self):
        last_name = self.cleaned_data.get('lastName')
        return self.validate_name(last_name)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def validate_password(password):
        if len(password) < 5:
            raise ValidationError('Password must be at least 5 characters long.')
        
        if not any(c.isupper() for c in password):
            raise ValidationError('Password must include at least one uppercase letter.')
        
        if not any(c.islower() for c in password):
            raise ValidationError('Password must include at least one lowercase letter.')
        
        if not any(c.isdigit() for c in password):
            raise ValidationError('Password must include at least one number.')
        
        return password


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')

        if password and confirm and password != confirm:
            self.add_error('confirm_password', 'Passwords do not match.')
