from django.urls import path
from welcome.views import welcome_page, BMI, retirement
from . import views

app_name = 'welcome'

urlpatterns = [
    path("", views.welcome_page, name="home"),
    path("bmi_calculator/", views.BMI, name="bmi_cal"),
    path("retirement_calculator/", views.retirement, name="retire"),
]

