from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from registration.forms import RegistrationFormUniqueEmail
from .models import CustomUser


class CustomUserRegisterForm(RegistrationFormUniqueEmail):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class CustomUserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """
    class Meta:
        model = CustomUser
        fields = '__all__'

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

class TransferPointsForm(forms.Form):
    username = forms.CharField(required=True)
    amount = forms.IntegerField(required=True)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            receiving_user = get_user_model().objects.get(username=username)
        except ObjectDoesNotExist:
            raise forms.ValidationError(_("Receiving username Does Not Exist"))
        return username

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount < 0 or amount > 10000:
            raise forms.ValidationError(_("Amount can't be less than 0 or more than 10000"))

        return amount
