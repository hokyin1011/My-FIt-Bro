import base64
from decimal import Decimal
from io import BytesIO
from django import forms
from django.shortcuts import render
from matplotlib import pyplot as plt
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


person = []
food=[]
class NewPersonForm(forms.Form):
    name = forms.CharField(label="Name")
    age = forms.IntegerField(label="Age")
    weight = forms.DecimalField(label="Weight (kg)", max_digits=5, decimal_places=2)
    height = forms.DecimalField(label="Height (cm)", max_digits=5, decimal_places=2)
    GENDER_CHOICES = [('female', 'Female'), ('male', 'Male')]
    gender = forms.ChoiceField(label="Gender", choices=GENDER_CHOICES)
    ACTIVITY_CHOICES = [
            ('sedentary', 'Sedentary'),
            ('lightly', 'Light Activity'),
            ('moderate', 'Moderate Activity'),
            ('active', 'Active'),
            ('extra active', 'Extra Active')
    ]
    activity = forms.ChoiceField(label="Activity Level", choices=ACTIVITY_CHOICES)

class NewFoodForm(forms.Form):
    food = forms.CharField(label="food")
    weight = forms.CharField(label="weight")
    

def add(request):
    if request.method == 'POST':
        form = NewPersonForm(request.POST)
        if form.is_valid():
            # Extracting data from the form and adding it to the person list

            person_data = {
                'name': form.cleaned_data['name'],
                "age": form.cleaned_data['age'],
                "weight": form.cleaned_data['weight'],
                "height": form.cleaned_data['height'],
                "gender": form.cleaned_data['gender'],
                "activity": form.cleaned_data['activity'],
            }
            person.append(person_data)
            activity_multipliers = {
            'sedentary': Decimal('1.2'),
            'lightly': Decimal('1.375'),
            'moderate': Decimal('1.55'),
            'active': Decimal('1.725'),
            'extra active': Decimal('1.9')
    }

        for p in person:
            # Convert all inputs to Decimal for consistent calculations
            weight = Decimal(p['weight'])
            height_cm = Decimal(p['height'])
            age = Decimal(p['age'])
            if p['gender'].lower() == 'male':
                bmr = Decimal('66') + (Decimal('13.7') * weight) + (Decimal('5') * height_cm) - (Decimal('6.8') * age)
            else:
                bmr = Decimal('655') + (Decimal('9.6') * weight) + (Decimal('1.8') * height_cm) - (Decimal('4.7') * age)

            # Get activity multiplier and calculate TDEE
            activity_level = p['activity'].lower()
            activity_multiplier = activity_multipliers.get(activity_level, Decimal('1'))
            tdee = bmr * activity_multiplier

            p['tdee'] = tdee
            p['lose_tdee']= tdee -500
            p['gain_tdee']= tdee +500
            # Redirect to a new URL or show a success message
            # return redirect('some-view-name')  # If you want to redirect
            return render(request, "calculator/name.html", {'person': person})
    else:
        form = NewPersonForm()

    return render(request, "calculator/index.html", {"form": form})


def checkpeople(request):
  
    return render(request, 'calculator/name.html', {'person': person})

def checkfood(request):
  
    return render(request, 'calculator/nutrition.html')


def lookup(request):
    if request.method == "POST":
        form = NewFoodForm(request.POST)
        if form.is_valid():
            food_name = form.cleaned_data['food']
            weight = form.cleaned_data['weight']  # Get the weight data from the form
            query = f'{weight} {food_name}'  # Format the query correctly
            api_url = f'https://api.api-ninjas.com/v1/nutrition?query={query}'
            response = requests.get(api_url, headers={'X-Api-Key': 'rg52hIGOW18/AGwFgi+C6A==ZNa9picvgQj06W4O'})

            if response.status_code == requests.codes.ok:
                data = response.json() 
                food.append(data)
                
                return render(request, "calculator/nutrition.html", {'food_data': data})
            else:
                error_message = f"Error: {response.status_code} - {response.text}"
                return render(request, "calculator/food.html", {'error': error_message})
    

    else:
        form = NewFoodForm()

    return render(request, "calculator/food.html", {'form': form, 'food': food})



def signup(request):
    if request.method == "POST":
        username = request.POST.get

        return render(request, 'user/login.html')
def signin(request):
    return render(request, 'user/login.html')

def signout(request):
    return render(request, 'user/login.html')


