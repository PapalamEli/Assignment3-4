from django.test import TestCase, Client, LiveServerTestCase
from django.urls import reverse, resolve, path
from welcome.forms import BMIForms, RetirementForms
from welcome.views import welcome_page, BMI, retirement
from django.http import JsonResponse, HttpResponseBadRequest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create your tests here.

class TestForms(TestCase):

    def test_BMI_data(self):
        form = BMIForms(data={
            'feet': '4',
            'inches': '4',
            'weight': '120.1'
        })
        self.assertTrue(form.is_valid())

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

class TestFrontEnd(LiveServerTestCase):

    def testBMI(self):
        selenium = webdriver.Firefox()
        selenium.get('http://127.0.0.1:8000/bmi_calculator')

        feet = selenium.find_element_by_id('id_feet')
        inches = selenium.find_element_by_id('id_inches')
        weight = selenium.find_element_by_id('id_weight')

        submit = selenium.find_element_by_name('submit')

        feet.send_keys('5')
        inches.send_keys('4')
        weight.send_keys('120')

        #submit.send_keys(Keys.RETURN)
        submit.click()
        selenium.implicitly_wait(10)
        assert 'BMI is 21.1 - Normal Weight' in selenium.page_source
        


    def testRetire(self):
        selenium = webdriver.Firefox()
        selenium.get('http://127.0.0.1:8000/retirement_calculator')

        age = selenium.find_element_by_id('id_age')
        salary = selenium.find_element_by_id('id_salary')
        savings = selenium.find_element_by_id('id_savings')
        goal = selenium.find_element_by_id('id_goal')

        submit = selenium.find_element_by_name('submit')

        age.send_keys('20')
        salary.send_keys('50000')
        savings.send_keys('0.25')
        goal.send_keys('120000')

        #submit.send_keys(Keys.RETURN)
        submit.click()

        assert 'Goal will be met at age: 27' in selenium.page_source
        