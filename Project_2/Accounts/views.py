from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from .models import Profile
@require_http_methods(["GET"])
def logout_view(request):
    logout(request)
    return redirect('login')  # or any page you want

# Create your views here.
def signup_view(request):
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('home')
    else:
        form =UserCreationForm()
    return render(request,'signup.html',{'form':form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # or wherever you want to redirect after login
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form':form})


def logout_view(request):
    print(f"Logout view called with method: {request.method}")
    if request.method == 'GET':
        logout(request)
        return redirect('Login')
    else:
        from django.http import HttpResponseNotAllowed
        return HttpResponseNotAllowed(['GET'])

@login_required
def edit_profile(request):
    
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Adjust this redirect as needed
    else:
        form = UserProfileForm(instance=profile, user=request.user)

    return render(request, 'edit_profile.html', {'form': form, 'profile': profile})
