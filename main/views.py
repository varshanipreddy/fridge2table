from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Ingredient, Recipe
from .core.recommender import non_personalized_rec, personalized_rec

@login_required(login_url="/login")
def home(request):
    ingredients = []
    recipes = []
    inghidden = ""
    rechidden = ""
    if request.method == 'POST':
        iq = "%" + request.POST.get("ingquery", "") + "%"
        rq = "%" + request.POST.get("recquery", "") + "%"
        inghidden = request.POST.get("inghidden", "")
        rechidden = request.POST.get("rechidden", "")
        if iq != "%%":
            for i in Ingredient.objects.raw("SELECT id,name FROM main_ingredient WHERE name LIKE %s limit 5", [iq]):
                ingredients.append(i)
        if rq != "%%":
            for r in Recipe.objects.raw("SELECT id,recipeid,recipename FROM main_recipe WHERE recipename LIKE %s limit 5", [rq]):
                recipes.append(r)

    return render(request, 'main/home.html', {"ingredients": ingredients, "recipes": recipes, "inghidden": inghidden, "rechidden": rechidden})

@login_required(login_url="/login")
def results(request):
    results = {'res': []}
    if request.method == 'POST':
        ingredients = [] if len(request.POST.get("ingchosen", "")) == 0 else request.POST.get("ingchosen", "").split(",")
        recipe_ids = [] if len(request.POST.get("recidchosen", "")) == 0 else [int(i) for i in request.POST.get("recidchosen", "").split(",")]
        tags = dict(request.POST).get("tagchosen", [""])
        if tags[0] == "":
            tags = []
        if len(ingredients) and len(recipe_ids):
            results = personalized_rec(ingredients, recipe_ids)
        if len(ingredients) and len(recipe_ids) == 0:
            results = non_personalized_rec(ingredients, recipe_ids, tags, option=4)
        else:
            return render(request, 'main/results.html', results)
        print(results)

    return render(request, 'main/results.html', results)

def about(request):
    return render(request, 'main/about.html', {})

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})