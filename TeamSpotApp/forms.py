from django import forms

USER_CHOICES = (

)

class UserForm(forms.Form):
    user_field = forms.ChoiceField(choices = USER_CHOICES)