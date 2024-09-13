from django.shortcuts import render,redirect

# Create your views here.
from . import forms

def add_category(request):
    if request.method == 'POST': # if user click submit button
        category_form = forms.CategoryForm(request.POST) 
        if category_form.is_valid():
            category_form.save()
            return redirect('add_category') 
    
    else: # user normally website e gele blank form pabe
        category_form = forms.CategoryForm()
    return render(request, 'add_category.html', {'form' : category_form})