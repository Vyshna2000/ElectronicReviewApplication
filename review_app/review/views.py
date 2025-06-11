from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import Product
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import Product
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Product, Review,Category
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Review, ReviewReaction
import random
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import PasswordResetOTP
from django.utils import timezone
from django.utils import timezone  
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Category



def login_view(request):
    return render(request, 'base.html')  


def admin_login(request):
    return render(request, 'admin_login.html')  

def admin_dashboard(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.is_superuser:
                return redirect('dashboard')
            else:
                return redirect('login') 

        else:
            return render(request, 'base.html', {'error': 'Invalid username or password'})
    else:
        return redirect('login') 

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'base.html', {'error': 'Invalid username or password'})
    else:
        return redirect('login')  


def logout_view(request):
    auth_logout(request)
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    products = Product.objects.all()
    from django.db.models import Q
from django.core.paginator import Paginator
from .models import Product

def dashboard(request):
    products = Product.objects.all()
    pname = request.POST.get('pname') or request.GET.get('pname')
    if pname:
        products = products.filter(name__icontains=pname)

    sort_option = request.GET.get('sort')
    if sort_option == 'name':
        products = products.order_by('name')
    elif sort_option == 'price':
        products = products.order_by('price')
    elif sort_option == 'rating':
        products = products.order_by('reviews')
    elif sort_option == 'category':
        products = products.order_by('category__name') 

    paginator = Paginator(products, 9)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    return render(request, 'dashboard.html', {
        'products': products,
        'pname': pname,
        'sort_option': sort_option
    })

    return render(request, 'dashboard.html', {'products': products})

def product_reviews(request):
    pass

def signup(request):
    if request.method == 'POST':
        uname = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST.get('password2') 

       
        if password != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "signup.html")

       
        if User.objects.filter(username=uname).exists():
            messages.error(request, "Username already taken.")
            return render(request, "signup.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, "signup.html")

    
        myuser = User.objects.create_user(username=uname, password=password, email=email)
        myuser.save()
        messages.success(request, "Account created successfully. Please login.")
        return redirect('login')

    return render(request, "signup.html")

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    reviews = product.reviews.select_related('user').all()
    
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
    
    context = {
        'product': product,
        'reviews': reviews,
        'user_review': user_review,
    }
    
    return render(request, 'product_details.html', context)




@login_required
def add_review(request, id):
    product = get_object_or_404(Product, id=id)
    user = request.user

    if request.method == 'POST':
        comment = request.POST.get('comment')
        rating = request.POST.get('rating')

        
        if Review.objects.filter(product=product, user=user).exists():
            messages.error(request, "You have already reviewed this product.")
            return redirect('product_detail', pk=product.id)

        # Create and save the review
        Review.objects.create(
            product=product,
            user=user,
            comment=comment,
            rating=rating,
        )

        messages.success(request, "Review submitted successfully!")
        return redirect('product_detail', pk=product.id)

    # If GET or other method, redirect to product detail
    return redirect('product_detail', pk=product.id)




@login_required
def review_react(request):
    if request.method == "POST":
        review_id = request.POST.get('review_id')
        action = request.POST.get('action')  
        user = request.user

        if action not in ['like', 'dislike']:
            return JsonResponse({'error': 'Invalid action'}, status=400)

        try:
            review = Review.objects.get(pk=review_id)
        except Review.DoesNotExist:
            return JsonResponse({'error': 'Review not found'}, status=404)

        
        reaction, created = ReviewReaction.objects.get_or_create(review=review, user=user)

        if not created:
            
            if reaction.reaction_type == action:
                reaction.delete()
            else:
                reaction.reaction_type = action
                reaction.save()
        else:
            reaction.reaction_type = action
            reaction.save()

        # Return updated counts
        likes_count = review.reactions.filter(reaction_type='like').count()
        dislikes_count = review.reactions.filter(reaction_type='dislike').count()

        return JsonResponse({'likes': likes_count, 'dislikes': dislikes_count})

    return JsonResponse({'error': 'Invalid request method'}, status=405)



def add_product(request):
    categories = Category.objects.all()  # Fetch all categories
    return render(request, 'add_product.html', {'categories': categories})



def add_category(request):
    return render(request,'add_category.html')

def product_add(request):
    if request.method == 'POST':
        name = request.POST['name']
        brand = request.POST['brand']
        description = request.POST['description']
        price = request.POST['price']
        category_id = request.POST['category']
        image = request.FILES.get('image')

        category = Category.objects.get(id=category_id)

        Product.objects.create(
            name=name,
            brand=brand,
            description=description,
            price=price,
            category=category,
            image=image
        )
        return redirect('dashboard')

    categories = Category.objects.all()
    return render(request, 'add_product.html', {'categories': categories})


def category_add(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            Category.objects.create(name=name)
            messages.success(request, '✅ Category added successfully!')
            return redirect('category_add')  # or 'dashboard' if you'd prefer to go back
        else:
            messages.error(request, '⚠️ Category name is required.')
    
    return render(request, 'add_category.html')  # ensure this matches your actual template name



def index(request):
    return render(request,'index.html')









@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    product = review.product

    if request.method == "POST":
        review.comment = request.POST.get('comment')
        review.rating = request.POST.get('rating')
        review.save()
        return redirect('product_detail', pk=product.id)  

    context = {
        'product': product,
        'review': review,
    }
    return render(request, 'edit_review.html', context)




@login_required
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        product.name = request.POST['name']
        product.brand = request.POST['brand']
        product.description = request.POST['description']
        product.price = request.POST['price']
        product.category_id = request.POST['category']  # assuming FK
        if 'image' in request.FILES:
            product.image = request.FILES['image']
        product.save()
        return redirect('dashboard')

    categories = Category.objects.all()
    return render(request, 'edit_product.html', {'value': product, 'categories': categories})




@login_required
def delete_comment(request,id):
    review = get_object_or_404(Review, id=id, user=request.user)
    review.delete()
    return redirect('dashboard')

def delete_product(request, id):
    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to delete this product.")
        return redirect('dashboard')

    product = get_object_or_404(Product, id=id)
    product.delete()
    messages.success(request, "Product deleted successfully.")
    return redirect('dashboard')




def search(request):
    if request.method == 'POST':
        name = request.POST.get('pname')
        products = Product.objects.filter(name__icontains=name)
        return render(request, 'dashboard.html', {'products': products})


from django.contrib.auth.hashers import make_password

def reset_password_view(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm = request.POST['confirm']
        user_id = request.session.get('reset_user_id')

        if password != confirm:
            return render(request, 'reset_password.html', {'error': 'Passwords do not match'})

        if user_id:
            user = User.objects.get(id=user_id)
            user.password = make_password(password)
            user.save()

            # Clean up
            PasswordResetOTP.objects.filter(user=user).delete()
            del request.session['reset_user_id']

            return redirect('login')
    return render(request, 'reset_password.html')

def verify_otp_view(request):
    if request.method == 'POST':
        otp_entered = request.POST['otp']
        user_id = request.session.get('reset_user_id')
        if user_id:
            try:
                otp_obj = PasswordResetOTP.objects.get(user_id=user_id)

                if timezone.now() - otp_obj.created_at > timedelta(minutes=10):
                    return render(request, 'verify_otp.html', {'error': 'OTP expired'})

                if otp_obj.otp == otp_entered:
                    return redirect('reset_password')
                else:
                    return render(request, 'verify_otp.html', {'error': 'Invalid OTP'})
            except PasswordResetOTP.DoesNotExist:
                return render(request, 'verify_otp.html', {'error': 'OTP not found'})
    return render(request, 'verify_otp.html')



import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.models import User
from .models import PasswordResetOTP  # Make sure this model exists

def forgot_password_view(request):
    if request.method == "POST":
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            otp = str(random.randint(100000, 999999))

            # Save OTP to DB with timestamp
            PasswordResetOTP.objects.update_or_create(
                user=user,
                defaults={
                    'otp': otp,
                    'created_at': timezone.now()
                }
            )

            # Prepare the email content
            app_name = "Electronic Review Application"  # Or your app name
            subject = 'Password Reset OTP - ' + app_name
            message = f'''
Hello {user.username},

Welcome to {app_name}!

We received a request to reset your password. 
Your One-Time Password (OTP) is:

🔐 {otp}

This OTP is valid for the next 10 minutes.
Please do not share it with anyone for your security.

If you did not request this, you can safely ignore this message.

Thanks,  
Team {app_name}
'''

            # Send the email
            send_mail(
                subject=subject,
                message=message,
                from_email='vyshnaknr2000@gmail.com',
                recipient_list=[email],
                fail_silently=False,
            )

            # Store user ID in session
            request.session['reset_user_id'] = user.id
            return redirect('verify_otp')

        except User.DoesNotExist:
            return render(request, 'forgot_password.html', {'error': 'Email not found'})

    return render(request, 'forgot_password.html')
from social_core.exceptions import AuthAlreadyAssociated
from django.shortcuts import redirect


def auth_error_view(request):
    return render(request, 'auth_error.html', {
        'message': "This Google account is already linked to another user."
    })
