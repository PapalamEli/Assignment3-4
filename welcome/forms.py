from django import forms

#class HomeForm(forms.Form):

class BMIForms(forms.Form):
    feet = forms.IntegerField(required=True)
    inches = forms.IntegerField(required=True)
    weight = forms.FloatField(required=True)


class RetirementForms(forms.Form):
    age = forms.IntegerField(required=True)
    salary = forms.IntegerField(required=True)
    savings = forms.FloatField(required=True)
    goal = forms.IntegerField(required=True)