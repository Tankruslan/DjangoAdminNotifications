from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser, Profile


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.is_active = False
        if commit:
            user.save()
            custom_user = CustomUser.objects.create(user=user)
            Profile.objects.create(user=custom_user)
        return user
