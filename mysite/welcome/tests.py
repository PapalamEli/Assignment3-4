from django.test import TestCase, Client
from django.urls import reverse, resolve, path
from welcome.forms import BMIForms, RetirementForms
from welcome.views import welcome_page, BMI, retirement
from django.http import JsonResponse, HttpResponseBadRequest

# Create your tests here.

class TestForms(TestCase):

    def test_BMI_data(self):
        form = BMIForms(data={
            'feet': '4',
            'inches': '4',
            'weight': '120.1'
        })
        self.assertTrue(form.is_valid())

    def test_BMI_calc(self):
        response = self.client.get(reverse('welcome:bmi_cal'), {
            'first': 1,
            'second': 1,
        })
        self.assertEqual(response.status_code, 200)
        self.assertEquals(200, {
            'results': '200',
        })

    def test_BMI_no_data(self):
        form = BMIForms(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),3)

    def test_retire_data(self):
        form = RetirementForms(data={
            'age': '20',
            'salary': '50000',
            'savings': '0.22',
            'goal': '1000000'
        })
        self.assertTrue(form.is_valid())
        

    def test_retire_no_data(self):
        form = RetirementForms(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),4)


class TestViews(TestCase):

    def test_view_home(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_view_home_by_name(self):
        response = self.client.get(reverse('welcome:home'))
        self.assertEquals(response.status_code, 200)
    
    def test_view_home_correct_template(self):
        response = self.client.get(reverse('welcome:home'))
        self.assertTemplateUsed(response, 'welcome/home.html')
    
    def test_view_bmi(self):
        response = self.client.get('/bmi_calculator/')
        self.assertEquals(response.status_code, 200)

    def test_view_bmi_by_name(self):
        response = self.client.get(reverse('welcome:bmi_cal'))
        self.assertEquals(response.status_code, 200)
        
    
    def test_view_bmi_correct_template(self):
        response = self.client.get(reverse('welcome:bmi_cal'))
        self.assertTemplateUsed(response, 'welcome/bmi_calculator.html')

    def test_view_retire(self):
        response = self.client.get('/retirement_calculator/')
        self.assertEquals(response.status_code, 200)

    def test_view_retire_by_name(self):
        response = self.client.get(reverse('welcome:retire'))
        self.assertEquals(response.status_code, 200)
    
    def test_view_retire_correct_template(self):
        response = self.client.get(reverse('welcome:retire'))
        self.assertTemplateUsed(response, 'welcome/retirement_calculator.html')



class TestUrls(TestCase):

    def test_home_url(self):
        url = reverse('welcome:home')
        self.assertEquals(resolve(url).func, welcome_page)

    def test_bmi_url(self):
        url = reverse('welcome:bmi_cal')
        self.assertEquals(resolve(url).func, BMI)
    
    def test_retire_url(self):
        url = reverse('welcome:retire')
        self.assertEquals(resolve(url).func, retirement)
