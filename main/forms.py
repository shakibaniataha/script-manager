from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Request
from django.forms import ValidationError


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class AddRequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ('api_id', 'input_params')
        labels = {
            "api_id": "API",
            "input_params": "Input Parameters"
        }

    def clean(self):
        super(AddRequestForm, self).clean()
        input_params = self.cleaned_data.get('input_params')
        params_list = input_params.replace(' ', '').split(',')
        num_valid_params = 0
        for param in params_list:
            if param != '':
                num_valid_params += 1

        num_required_input_params = self.cleaned_data.get('api_id').num_input_params
        if num_valid_params != num_required_input_params:
            raise ValidationError('The number of input params must match the number of required params'
                                  ' specified by the API')