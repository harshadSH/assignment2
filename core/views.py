from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .models import Patient, Doctor
from django.db.utils import IntegrityError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from datetime import datetime

def patient_signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        profile_picture = request.FILES.get('profile_picture')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        address = request.POST.get('address')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('patient_signup')

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            Patient.objects.create(
                user=user,
                profile_picture=profile_picture,
                address=address,
            )
            messages.success(request, "Patient signup successful! Please log in.")
            return redirect('home')
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect('patient_signup')

    return render(request, 'patient_signup.html')


def doctor_signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        profile_picture = request.FILES.get('profile_picture')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        address = request.POST.get('address')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('doctor_signup')

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            Doctor.objects.create(
                user=user,
                profile_picture=profile_picture,
                address=address,
            )
            messages.success(request, "Doctor signup successful! Please log in.")
            return redirect('home')
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect('doctor_signup')

    return render(request, 'doctor_signup.html')

def doctor_home(request):
    doctor = request.user.doctor  # Assuming the logged-in user is a doctor
    context = {
        "doctor": doctor,
        "year": datetime.now().year,
    }
    return render(request, "doctor_home.html", context)

def patient_home(request):
    patient = request.user.patient  # Assuming the logged-in user is a doctor
    context = {
        "patient": patient,
        "year": datetime.now().year,
    }
    return render(request, "patient_home.html", context)


def home_page(request):
    if request.method == 'POST':
        # Handling login for patient
        if 'patient_login' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user and hasattr(user, 'patient'):
                auth_login(request, user)
                return redirect('patient_home')

        # Handling login for doctor
        elif 'doctor_login' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user and hasattr(user, 'doctor'):
                auth_login(request, user)
                return redirect('doctor_home')

    # Handle signup


    return render(request, 'home.html', )

def patient_dashboard(request):
    return render(request, 'patient_dashboard.html')

def doctor_dashboard(request):
    return render(request, 'doctor_dashboard.html')


#----------------BLOG------------------

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BlogForm
from .models import Blog

@login_required
def create_blog(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user

            # Check if the action is 'draft' or 'publish'
            if request.POST.get('action') == 'draft':
                blog.is_draft = True  # Set the status to 'draft'
            else:
                blog.is_draft = False  # Set the status to 'published'

            blog.save()
            return redirect('blog_list')  # Redirect to the blog listing page
    else:
        form = BlogForm()

    return render(request, 'create_blog.html', {'form': form})


@login_required
def my_blog(request):
    blogs = Blog.objects.filter(author=request.user).order_by('-created_at')  # Fetch blogs by user, order by date
    return render(request, 'my_blog.html', {'blogs': blogs})

# views.py

@login_required

def blog_list(request):
    search_query = request.GET.get('search', '')  # Get the search query from the GET request
    category_filter = request.GET.get('category', None)  # Get the category from the GET request
    blogs = Blog.objects.all()

    if search_query:
        blogs = blogs.filter(title__icontains=search_query)  # Filter by search query in the title

    if category_filter:
        blogs = blogs.filter(category=category_filter)  # Filter by category if provided

    # Add ordering functionality
    order_by = request.GET.get('order_by', None)
    if order_by:
        blogs = blogs.order_by(order_by)

    for blog in blogs:
        words = blog.summary.split()  # Split the summary into words
        if len(words) > 15:
            blog.short_summary = ' '.join(words[:15]) + "..."  # Limit to 15 words and add ellipsis
        else:
            blog.short_summary = blog.summary

    categories = Blog.objects.values_list('category', flat=True).distinct()  # Get distinct categories

    return render(request, 'blog_list.html', {'blogs': blogs, 'categories': categories, 'search_query': search_query})


@login_required
def blog_detail(request, blog_id):
    # Get the blog by its ID
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'blog_detail.html', {'blog': blog})

