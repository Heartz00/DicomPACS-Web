from django.shortcuts import redirect, render
from userauths.forms import UserRegisterForm, ProfileForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from userauths.models import Profile, User


# User = settings.AUTH_USER_MODEL


def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        #profile_form = ProfileForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.is_active = False  # Deactivate account until admin approves
            username = form.cleaned_data.get("username")
            new_user.save()
            messages.success(request, f"Hey {username}, your account was created successfully and is pending approval.")
            new_user = authenticate(username=form.cleaned_data['email'], 
                                    password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect('userauths:sign-up-success')
    else:
        form = UserRegisterForm()
        #profile_form = ProfileForm()

    context = {
        'form': form,
        #'profile_form': profile_form,
    }
    return render(request, "userauths/sign-up.html", context)



def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Hey you are already Logged In.")
        return redirect("core:index")
    
    if request.method == "POST":
        email = request.POST.get("email") # peanuts@gmail.com
        password = request.POST.get("password") # getmepeanuts

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You are logged in.")
                return redirect("core:index")
            else:
                messages.warning(request, "User Does Not Exist, create an account.")
    
        except:
            messages.warning(request, f"User with {email} does not exist")
        

    
    return render(request, "userauths/sign-in.html")


                                                       

def logout_view(request):

    logout(request)
    messages.success(request, "You logged out.")
    return redirect("userauths:sign-in")




def sign_up_success_view(request):
    return render(request, 'userauths/sign-up-success.html')


def profile_update(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            messages.success(request, "Profile Updated Successfully.")
            return redirect("core:dashboard")
    else:
        form = ProfileForm(instance=profile)

    context = {
        "form": form,
        "profile": profile,
    }

    return render(request, "userauths/profile-edit.html", context)
