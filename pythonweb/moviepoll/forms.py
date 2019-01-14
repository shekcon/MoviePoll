from django import forms

class PollMovie(forms.Form):
   option = forms.ChoiceField(required = True, choices = CHOICES,
                                widget=forms.RadioSelect(attrs={
                                    'class' : 'Radio'
                                }), initial=1)