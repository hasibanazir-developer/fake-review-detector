from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegistrationForm
from django.http import HttpResponse
from django.contrib import messages
from .models import Product  # Import the Product model
from .models import Product, Review
from .forms import ReviewForm

# Registration view
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = RegistrationForm()
    
    return render(request, 'register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {user.username}!")
                return redirect('dashboard')  # Redirect to the dashboard after login
            else:
                messages.error(request, "Invalid username or password. Please try again.")
                return redirect('login')  # Redirect back to login if credentials are invalid
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


# Logout view
def logout_view(request):
    logout(request)  # Clears the session
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')  # Redirect to login page after logout

def admin_login(request):
    return render(request, '~/admin/login/?next=/admin/')

def user_login(request):
    return render(request, 'login.html')
def home(request):
    return render(request, 'home.html')  # Assuming your home page template is home.html


from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Review
from django.contrib.auth.decorators import login_required







# View for the dashboard page (protected, requires login)
@login_required
def dashboard_view(request):
    # Fetch all products
    products = Product.objects.annotate(avg_sentiment=Avg('reviews__sentiment_score')).order_by('-avg_sentiment')

#    products = Product.objects.all()  # You can modify this to filter or limit results if necessary

    # Passing the username and products to the template
    return render(request, 'dashboard.html', {'username': request.user.username, 'products': products})

# Annotate each product with average sentiment score from its reviews
    


from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()
from django.db.models import Avg

def get_client_ip(request):
    """Helper to get client's real IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)


    if request.method == 'POST':
        review_text = request.POST.get('review_text')
        ip_address = get_client_ip(request)

        # Check if it's a duplicate
        existing_review = Review.objects.filter(product=product, user=request.user, review_text=review_text).first()
        is_duplicate = existing_review is not None

        # Sentiment score
       
        sentiment_score = analyzer.polarity_scores(review_text)['compound']

            # Label the sentiment
        if sentiment_score > 0:
            sentiment_label = "positive"
        elif sentiment_score <0:
            sentiment_label = "negative"
        else:
            sentiment_label = "neutral"

        # Check IP usage for this product
        ip_review_count = Review.objects.filter(product=product, ip_address=ip_address,user=request.user).count()
        is_fake = ip_review_count >= 3  # Mark fake if 3 or more from the same IP/same user/ same product

        # Save the review
        Review.objects.create(
            
            product=product,
            user=request.user,
            review_text=review_text,
            sentiment_score=sentiment_score,
            sentiment_label=sentiment_label,
            is_duplicate=is_duplicate,
            is_fake=is_fake,
            ip_address=ip_address

            
        )

        messages.success(request, 'Your review has been added successfully!')
        return redirect('dashboard')

    return render(request, 'add_review.html', {'product': product})


# ---------------------------------------------------------------------------
# Temporary deployment diagnostics. Remove once the 500 is resolved.
#
# DEBUG is off in production, so Django replies with a blank "Server Error
# (500)" page and the real exception is only visible in Vercel's function log.
# This endpoint reports just enough to identify the cause. It never exposes the
# password: only the host, port and database name, which are already in
# DEPLOY.md.
# ---------------------------------------------------------------------------
import os

from django.conf import settings as _settings
from django.contrib.auth.models import User
from django.db import connection as _connection
from django.http import JsonResponse


def _url_shape(url):
    """Describe a connection URL's structure without revealing the password.

    Enough to spot the usual paste mistakes - a leftover ``[YOUR-PASSWORD]``
    placeholder, a stray newline, an unencoded ``#`` truncating the string -
    while never echoing the credential itself.
    """
    if not url:
        return None
    tail = url.split('@', 1)[1] if '@' in url else '(no @ - password or host missing)'
    return {
        'length': len(url),
        'starts_with': url.split('://', 1)[0] if '://' in url else '(no scheme)',
        'after_the_at_sign': tail,
        'has_placeholder_brackets': ('[' in url or ']' in url),
        'has_whitespace_or_newline': (url.strip() != url or any(c in url for c in ' \t\r\n')),
        'has_raw_hash': '#' in url,
    }


def healthz(request):
    db = _settings.DATABASES['default']
    info = {
        'engine': db['ENGINE'].rsplit('.', 1)[-1],
        'database_url_set': bool(os.environ.get('DATABASE_URL')),
        'missing_database_url': getattr(_settings, 'MISSING_DATABASE_URL', False),
        'host': db.get('HOST') or '(none)',
        'port': str(db.get('PORT') or '(none)'),
        'name': str(db.get('NAME')),
        'on_vercel': bool(os.environ.get('VERCEL')),
        'region': os.environ.get('VERCEL_REGION', '(unset)'),
        'vercel_env': os.environ.get('VERCEL_ENV', '(unset)'),
        # Why a DATABASE_URL that is present still did not parse. Redacted.
        'database_url_error': getattr(_settings, 'DATABASE_URL_ERROR', None),
        'database_url_shape': _url_shape(os.environ.get('DATABASE_URL')),
        # Which project-level variables reach the function at all. Names and a
        # yes/no only - never the values. If every one of these is false, the
        # variables were saved on a different project or environment rather
        # than being merely mistyped.
        'env_vars_seen': {
            k: bool(os.environ.get(k))
            for k in ('DATABASE_URL', 'SECRET_KEY', 'ALLOWED_HOSTS',
                      'CSRF_TRUSTED_ORIGINS', 'DEBUG')
        },
    }

    try:
        with _connection.cursor() as cur:
            cur.execute('SELECT 1')
            cur.fetchone()
    except Exception as exc:                      # noqa: BLE001 - reporting it is the point
        info['db_ok'] = False
        info['error_type'] = type(exc).__name__
        info['error'] = str(exc).strip()[:400]
    else:
        info['db_ok'] = True
        # Confirms migrations actually ran against this database.
        try:
            info['user_count'] = User.objects.count()
        except Exception as exc:                  # noqa: BLE001
            info['user_count'] = f'{type(exc).__name__}: {str(exc).strip()[:200]}'

    return JsonResponse(info, json_dumps_params={'indent': 2})
