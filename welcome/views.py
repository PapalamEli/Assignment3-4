from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import BMIForms
from .forms import RetirementForms

# Create your views here.
#class HomePage(TemplateView):
template_name = 'welcome/home.html'
def welcome_page(request):

    return render(request=request,
    template_name=template_name)
    


def BMI(request):
    form = BMIForms(request.POST)
    results = ""


    if form.is_valid():
        input_ft = form.cleaned_data['feet']
        input_in = form.cleaned_data['inches']
        input_lbs = form.cleaned_data['weight']

        

        w = input_lbs * 0.45
        i = (input_ft * 12) + input_in
        inch = (i * 0.025) * (i * 0.025)
        bmi = w / inch
        bmi = format(bmi, '.1f')
        bmi = float(bmi)

        if bmi < 18.5:
            results = "BMI is {} - Underweight" .format(bmi)
        elif bmi > 18.5 and bmi < 24.9:
            results = "BMI is {} - Normal Weight" .format(bmi)
        elif bmi > 25.0 and bmi < 29.9:
            results = "BMI is {} - Overweight" .format(bmi)
        else:
            results = "BMI is {} - Obese" .format(bmi)

    
        form = BMIForms()
    args = {"form":form, 'results':results}
    return render(request = request,
                    template_name= "welcome/bmi_calculator.html",
                    context=args )

def retirement(request):
    form = RetirementForms(request.POST)
    year_met = ""

    if form.is_valid():
        input_age = form.cleaned_data['age']
        input_sal = form.cleaned_data['salary']
        input_savings = form.cleaned_data['savings']
        input_goal = form.cleaned_data['goal']


        savings_per_year = (input_sal * input_savings) * 1.35
        years_till = input_goal / savings_per_year
        age_met = input_age + years_till
        age_met = round(age_met)

        
        if age_met < 100:
            year_met = "Goal will be met at age: {}" .format(age_met)
        else:
            year_met = "The goal will not be met: {}" .format(age_met)
    
        form = RetirementForms()
        
    args = {"form":form, "year_met":year_met}
    return render(request = request,
                    template_name= "welcome/retirement_calculator.html",
                    context=args)