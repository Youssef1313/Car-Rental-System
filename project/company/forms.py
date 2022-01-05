from django.contrib.auth.forms import UserCreationForm
from .models import Customer


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Customer
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', )
