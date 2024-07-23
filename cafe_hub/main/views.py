# views.py
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm

from .decorators import unauthenticated_user
from main.models import Branch
from .forms import SignUpForm
from .forms import BranchForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Q 

@unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'search')
            return redirect(next_url)
        else:
            print(login_form.errors)
    else:
        login_form = AuthenticationForm()
    return render(request, 'main/login.html', {'login_form': login_form})
    
@unauthenticated_user
def signup_view(request):
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save(commit=False)
            user.set_password(signup_form.cleaned_data['password'])
            user.save()

            role = signup_form.cleaned_data['role']
            if role == 'Customer':
                group = Group.objects.get(name='Customer')
            elif role == 'Uber-User':
                group = Group.objects.get(name='Uber-user')
            elif role == 'Admin':
                group = Group.objects.get(name='Admin')
            else:
                group = None

            if group:
                user.groups.add(group)

            login(request, user)
            return redirect('search')
    else:
        signup_form = SignUpForm()

    return render(request, 'main/signup.html', {'signup_form': signup_form})

def get_user_role(user):
    if user.is_superuser:
        return 'uber-user'
    elif user.role:
        return user.role
    else:
        return 'unknown'
    
def search(request):
    search_by = request.GET.get('search_by')
    query = request.GET.get(search_by, '')  
    
    if search_by == 'name':
        results = Branch.objects.filter(name__icontains=query)
    elif search_by == 'address':
        results = Branch.objects.filter(address__icontains=query)
    elif search_by == 'city':
        results = Branch.objects.filter(city__icontains=query)
    elif search_by == 'zip_code':
        results = Branch.objects.filter(zip_code__icontains=query)
    else:
        results = []
    
    if request.user.is_authenticated:
        user_role = get_user_role(request.user)
        print(f"Authenticated user: {request.user.username}, Role: {user_role}")
    else:
        user_role = 'unknown'
        print("User is not authenticated")
    
    context = {
        'results': results,
        'name_query': request.GET.get('name', ''),
        'address_query': request.GET.get('address', ''),
        'city_query': request.GET.get('city', ''),
        'zip_code_query': request.GET.get('zip_code', ''),
        'user_role': user_role
    }
    
    return render(request, 'main/search.html', context)


@login_required
def index(request):
    user_branch = request.user.branch
    context = {
        'user_role': request.user.role,
        'user_branch': user_branch
    }
    
    return render(request, 'main/index.html', context)

def is_admin(user):
    return user.is_superuser or user.role == 'admin'

@user_passes_test(is_admin)
def create_branch(request):
    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            branch = form.save()
            request.user.branch = branch
            request.user.save()
            return redirect('index') 
    else:
        form = BranchForm()
    return render(request, 'main/create_branch.html', {'form': form})

def branch_detail(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id)
    
    if request.user.is_authenticated:
        user_role = get_user_role(request.user)
    else:
        user_role = 'unknown'
    
    return render(request, 'main/index.html', {'branch': branch, 'user_role': user_role})