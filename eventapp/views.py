from urllib import request, response

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import EventBooking
from .models import EventBooking, Payment
from .models import *
from .forms import *
from django.contrib import messages

from datetime import timedelta
from django.utils import timezone


def home(request):
    categories = EventCategory.objects.all()
    gallery = Gallery.objects.all()[:8]
    reviews = Review.objects.all()[:6]

    return render(request, 'home.html', {
        'categories': categories,
        'gallery': gallery,
        'reviews': reviews,
    })


#register
from django.contrib.auth.models import User
from django.contrib import messages
import random
from django.core.mail import send_mail
from .models import EmailOTP

from django.core.mail import send_mail
from django.conf import settings

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]

            if User.objects.filter(username=email).exists():
                messages.error(request, "This email is already registered. Please login.")
                return render(request, "register.html", {"form": form})

            otp = str(random.randint(100000, 999999))

            user = form.save(commit=False)
            user.is_active = False
            user.save()

            EmailOTP.objects.create(
                user=user,
                otp=otp
            )

            try:
                send_mail(
                    "Email Verification - Jay Goga Event",
                    f"""
Hello {user.first_name},

Thank you for registering.

Your OTP is: {otp}

Please do not share this OTP with anyone.

Jay Goga Event Management
""",
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )

                messages.success(request, "OTP has been sent to your email.")

            except Exception as e:
                print(e)
                messages.error(request, f"Email could not be sent: {e}")

            return redirect("verify_otp", user.id)

    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})

# EVENT LIST
def event_list(request):
    events = EventCategory.objects.all()

    return render(request, 'event_list.html', {
        'events': events
    })

# from django.shortcuts import render, get_object_or_404
# from .models import EventBooking

# def invoice(request, booking_id):
#     booking = get_object_or_404(EventBooking, id=booking_id, user=request.user)

#     return render(request, "invoice.html", {
#         "booking": booking
#     })

# BOOK EVENT
@login_required
def book_event(request):

    form = BookingForm()

    if request.method == 'POST':
        form = BookingForm(request.POST)

        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()

            return redirect('payment', booking.id)

    return render(request, 'booking.html', {
        'form': form
    })

import qrcode
import base64
from io import BytesIO

@login_required
def payment_view(request, booking_id):

    booking = get_object_or_404(
        EventBooking,
        id=booking_id
    )

    PACKAGE_PRICES = {
        "Silver Package": 25000,
        "Gold Package": 50000,
        "Platinum Package": 100000,
        "Diamond Package": 150000,
        "Royal Package": 250000,
        "Wedding Premium": 500000,
    }

    amount = PACKAGE_PRICES.get(
        booking.package,
        0
    )

    upi_link = (
        f"upi://pay?"
        f"pa=urvishpatel008@oksbi"
        f"&pn=Jay Goga Event"
        f"&am={amount}"
        f"&cu=INR"
    )

    qr = qrcode.make(upi_link)

    buffer = BytesIO()
    qr.save(buffer, format="PNG")

    qr_code = base64.b64encode(
        buffer.getvalue()
    ).decode()

    form = PaymentForm()

    if request.method == 'POST':

        form = PaymentForm(
            request.POST,
            request.FILES
        )

    if form.is_valid():

        payment = form.save(commit=False)

        payment.booking = booking

        payment.amount = amount

        payment.save()

        messages.success(
            request,
            f"Payment Submitted Successfully.<br><br>Booking ID : EV-{booking.id:04d}"
        )

        return redirect('my_bookings')

    return render(request, "payment.html", {
    "form": form,
    "booking": booking,
    "amount": amount,
    "qr_code": qr_code,
})


    
# MY BOOKINGS
@login_required(login_url='login')
def my_bookings(request):
    bookings = EventBooking.objects.filter(user=request.user)
    return render(request, 'my_bookings.html', {
        'bookings': bookings
    })


# GALLERY
def gallery(request):

    images = Gallery.objects.all()

    return render(request, 'gallery.html', {
        'images': images
    })


# REVIEW
@login_required
def review_view(request):

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('reviews')

    else:
        form = ReviewForm()

    reviews = Review.objects.all().order_by('-id')

    return render(request, 'reviews.html', {
        'form': form,
        'reviews': reviews
    })

# CONTACT
def contact_view(request):

    form = ContactForm()

    if request.method == 'POST':

        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'contact.html', {
        'form': form
    })


# DASHBOARD
@login_required
def dashboard(request):

    total_bookings = EventBooking.objects.count()
    total_users = User.objects.count()
    total_packages = Package.objects.count()

    context = {
        'total_bookings': total_bookings,
        'total_users': total_users,
        'total_packages': total_packages,
    }

    return render(request, 'dashboard.html', context)

from django.db.models import Sum

@login_required
def dashboard(request):

    total_bookings = EventBooking.objects.count()

    approved_bookings = EventBooking.objects.filter(
        status='Approved'
    ).count()

    pending_bookings = EventBooking.objects.filter(
        status='Pending'
    ).count()

    total_users = User.objects.count()

    total_revenue = Payment.objects.filter(
        payment_status='Paid'
    ).aggregate(
        Sum('amount')
    )['amount__sum']

    context = {

        'total_bookings': total_bookings,

        'approved_bookings': approved_bookings,

        'pending_bookings': pending_bookings,

        'total_users': total_users,

        'total_revenue': total_revenue or 0
    }

    return render(
        request,
        'dashboard.html',
        context
    )

def wedding_details(request):
    return render(request, 'wedding_details.html')

from django.shortcuts import render

def event_details(request, event_name):
    return render(request, 'event_details.html', {
        'event_name': event_name
    })

def event_details(request, event_name):

    details = {

        "Wedding Event": {
            "price": "₹25,000",
            "image": "Wedding Event.jpg",
            "services": [
                "Decoration",
                "Photography & Videography",
                "DJ & Music",
                "Catering"
            ]
        },

        "Birthday Party": {
            "price": "₹15,000",
            "image": "Birthday Party.jpg",
            "services": [
                "Theme Decoration",
                "Cake Arrangement",
                "Games & Activities"
            ]
        },

        "Engagement Event": {
            "price": "₹20,000",
            "image": "Engagement Event.jpg",
            "services": [
                "Ring Ceremony Setup",
                "Floral Decoration"
            ]
        },

        "Corporate Event": {
            "price": "₹35,000",
            "image": "Corporate Event.jpg",
            "services": [
                "Conference Setup",
                "Projector",
                "Audio System"
            ]
        },

        "Anniversary Event": {
            "price": "₹18,000",
            "image": "Anniversary Event.jpg",
            "services": [
                "Decoration",
                "Photography"
            ]
        },

        "Festival Event": {
            "price": "₹30,000",
            "image": "Festival Event.jpg",
            "services": [
                "Stage Setup",
                "Lighting"
            ]
        },

        "Concert Event": {
            "price": "₹40,000",
            "image": "Concert Event.jpg",
            "services": [
                "Sound System",
                "Artist Management"
            ]
        },

        "Baby Shower": {
            "price": "₹12,000",
            "image": "Baby Shower.jpg",
            "services": [
                "Theme Decoration",
                "Photography"
            ]
        },

        "Farewell Party": {
            "price": "₹15,000",
            "image": "Farewell Party.jpg",
            "services": [
                "DJ Music",
                "Entertainment"
            ]
        },

        "SchoolCollege Event": {
            "price": "₹20,000",
            "image": "SchoolCollege Event.jpg",
            "services": [
                "Stage Setup",
                "Prize Distribution"
            ]
        },

        "House Warming": {
            "price": "₹18,000",
            "image": "House Warming.jpg",
            "services": [
                "Puja Arrangement",
                "Guest Management"
            ]
        },

        "Cultural Program": {
            "price": "₹22,000",
            "image": "Cultural Program.jpg",
            "services": [
                "Stage Decoration",
                "Artist Coordination"
            ]
        },
    }

    event = details.get(event_name)

    return render(
        request,
        'event_details.html',
        {
            'event_name': event_name,
            'event': event
        }
    )

def packages(request):
    return render(request, 'packages.html')

def packages(request):
    return render(request, 'packages.html')

def package_details(request, package_name):
    

    packages = {

        "Silver Package": {
            "price": "₹25,000",
            "services": [
                "Basic Decoration",
                "Sound System",
                "Seating Arrangement",
                "Stage Setup",
                "Event Coordinator",
                "Welcome Entry"
            ]
        },

        "Gold Package": {
            "price": "₹50,000",
            "services": [
                "Premium Decoration",
                "Photography",
                "DJ Setup",
                "Sound System",
                "Stage Decoration",
                "Event Coordinator",
                "Welcome Drinks",
                "Guest Assistance"
            ]
        },

        "Platinum Package": {
            "price": "₹1,00,000",
            "services": [
                "Luxury Decoration",
                "Premium Catering",
                "Photography",
                "Videography",
                "DJ & Music",
                "Stage Setup",
                "Guest Management",
                "Lighting Arrangement"
            ]
        },

        "Diamond Package": {
            "price": "₹1,50,000",
            "services": [
                "Luxury Decoration",
                "Premium Catering",
                "Photography & Videography",
                "DJ & Lighting",
                "Fireworks Show",
                "Guest Management",
                "Luxury Entry Gate",
                "Stage Design"
            ]
        },

        "Royal Package": {
            "price": "₹2,50,000",
            "services": [
                "Royal Theme Decoration",
                "Premium Catering",
                "Photography & Videography",
                "Live Music Performance",
                "Luxury Stage Setup",
                "VIP Guest Management",
                "Security Service",
                "Valet Parking"
            ]
        },

        "Wedding Premium": {
            "price": "₹5,00,000",
            "services": [
                "Complete Wedding Planning",
                "Luxury Decoration",
                "Premium Catering",
                "Photography",
                "Cinematic Videography",
                "DJ & Live Music",
                "Guest Management",
                "Bridal Entry Setup",
                "Luxury Stage Design",
                "Security & Parking Management"
            ]
        }

    }

    package = packages.get(package_name)

    return render(
        request,
        'package_details.html',
        {
            'package_name': package_name,
            'package': package
        }
    )

def review_view(request):

    if request.method == 'POST':

        form = ReviewForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            review = form.save(commit=False)
            review.user = request.user
            review.save()

            return redirect('reviews')

    else:
        form = ReviewForm()

    reviews = Review.objects.all().order_by('-id')

    return render(
        request,
        'reviews.html',
        {
            'form': form,
            'reviews': reviews
        }
    )

def review_view(request):

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('reviews')

    else:
        form = ReviewForm()

    reviews = Review.objects.all().order_by('-id')

    return render(request, 'reviews.html', {
        'form': form,
        'reviews': reviews
    })


@login_required
def my_bookings(request):

    bookings = EventBooking.objects.filter(
        user=request.user
    ).order_by('-id')

    return render(
        request,
        'my_bookings.html',
        {
            'bookings': bookings
        }
    )


from .models import EventBooking
from django.shortcuts import get_object_or_404, redirect

def cancel_booking(request, booking_id):

    booking = get_object_or_404(
        EventBooking,
        id=booking_id,
        user=request.user
    )

    booking.status = "Cancelled"
    booking.save()

    return redirect('my_bookings')

from django.contrib.auth.decorators import login_required
from .models import EventBooking

@login_required
def dashboard(request):

    total_bookings = EventBooking.objects.count()

    pending = EventBooking.objects.filter(
        status='Pending'
    ).count()

    approved = EventBooking.objects.filter(
        status='Approved'
    ).count()

    cancelled = EventBooking.objects.filter(
        status='Cancelled'
    ).count()

    context = {
        'total_bookings': total_bookings,
        'pending': pending,
        'approved': approved,
        'cancelled': cancelled,
    }

    return render(request, 'dashboard.html', context)

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('home')

from django.contrib.auth import authenticate, login, logout

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            if not user.is_active:
                return render(request, 'login.html', {
                    'error': 'Please verify your email first.'
                })

            login(request, user)
            return redirect('home')

        return render(request, 'login.html', {
            'error': 'Invalid Username or Password'
        })

    return render(request, 'login.html')

from django.utils.html import format_html

@login_required
def profile_view(request):
    return render(request, 'profile.html')

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import EventBooking


def generate_invoice(request, booking_id):

    booking = get_object_or_404(
    EventBooking,
    id=booking_id,
    user=request.user
)

    payment = Payment.objects.filter(booking=booking).first()

    if payment:
        amount = payment.amount
    else:
        amount = 0

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="Invoice_EV_{booking.id}.pdf"'
    )

    p = canvas.Canvas(response)

    # ==================================
    # HEADER
    # ==================================

    p.setTitle("Jay Goga Event Invoice")

    p.setFont("Helvetica-Bold", 24)
    p.drawString(95, 800, "JAY GOGA EVENT MANAGEMENT")

    p.setFont("Helvetica", 11)
    p.drawString(190, 780, "Making Your Events Memorable")

    p.line(40, 770, 550, 770)

    # ==================================
    # INVOICE DETAILS
    # ==================================

    p.setFont("Helvetica-Bold", 14)
    p.drawString(40, 740, "INVOICE")

    # Invoice No
    p.setFont("Helvetica-Bold", 11)
    p.drawString(40, 715, "Invoice No :")

    p.setFont("Helvetica", 11)
    p.drawString(115, 715, f"EV-{booking.id:04d}")

    # Booking Date
    p.setFont("Helvetica-Bold", 11)
    p.drawString(330, 715, "Booking Date :")

    p.setFont("Helvetica", 11)
    p.drawString(
        425,
        715,
        booking.created_at.strftime('%d-%m-%Y')
    )

    # ==================================
    # CUSTOMER DETAILS
    # ==================================

    p.rect(40, 610, 510, 80)

    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, 670, "Customer Details")

    p.line(40, 660, 550, 660)

    # Name
    p.setFont("Helvetica-Bold", 11)
    p.drawString(50, 635, "Name :")

    p.setFont("Helvetica", 11)
    p.drawString(95, 635, booking.name)

    # Contact
    p.setFont("Helvetica-Bold", 11)
    p.drawString(300, 635, "Contact :")

    p.setFont("Helvetica", 11)
    p.drawString(360, 635, booking.contact_number)

    # ==================================
    # EVENT DETAILS
    # ==================================

    p.rect(40, 350, 510, 230)

    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, 555, "Event Details")

    p.line(40, 535, 550, 535)

    y = 505

    details = [
        ("Event Category :", booking.category),
        ("Package :", booking.package),
        ("Venue :", booking.venue),
        ("Guests :", str(booking.guests)),
        ("Event Date :", str(booking.event_date)),
    ]

    for label, value in details:

        p.setFont("Helvetica-Bold", 11)
        p.drawString(60, y, label)

        p.setFont("Helvetica", 11)
        p.drawString(250, y, value)

        y -= 35

    # ==================================
    # BOOKING SUMMARY
    # ==================================

    # ==================================
# BOOKING SUMMARY
# ==================================


# ==================================
# BOOKING SUMMARY
# ==================================

# Box
    p.rect(40, 210, 510, 110)

# Heading
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, 300, "Booking Summary")

# Header Line
    p.line(40, 290, 550, 290)

# Booking Status
    p.setFont("Helvetica-Bold", 11)
    p.drawString(60, 260, "Booking Status :")

    p.setFont("Helvetica", 11)
    p.drawString(250, 260, booking.status)

# Payable Amount
    p.setFont("Helvetica-Bold", 11)
    p.drawString(60, 235, "Payable Amount :")

    p.setFont("Helvetica-Bold", 11)
    p.drawString(250, 235, f"INR. {amount}")
    # ==================================
    # SIGNATURE
    # ==================================

    p.line(380, 150, 520, 150)

    p.drawString(395, 130, "Authorized Signature")

    # ==================================
    # FOOTER
    # ==================================

    p.line(40, 120, 550, 120)

    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(
        300,
        90,
        "Thank You For Choosing Us!"
    )

    p.setFont("Helvetica", 13)
    p.drawCentredString(
        300,
        65,
        "Jay Goga Event Management"
    )

    p.setFont("Helvetica-Oblique", 11)
    p.drawCentredString(
        300,
        40,
        "Creating Memories, One Event At A Time"
    )

    p.save()

    return response


import random

otp = str(random.randint(100000, 999999))

from django.shortcuts import get_object_or_404

def verify_otp(request, user_id):

    user = get_object_or_404(User, id=user_id)
    otp_obj = get_object_or_404(EmailOTP, user=user)

    if request.method == "POST":

        form = OTPForm(request.POST)

        if form.is_valid():

            # OTP Expire Check
            if timezone.now() > otp_obj.created_at + timedelta(minutes=5):

                otp_obj.delete()

                messages.error(
                    request,
                    "OTP has expired. Please request a new OTP."
                )

                return redirect("resend_otp", user.id)

            entered_otp = form.cleaned_data["otp"]

            if entered_otp == otp_obj.otp:

                user.is_active = True
                user.save()

                otp_obj.delete()

                messages.success(
                    request,
                    "Email Verified Successfully."
                )

                return redirect("login")

            else:

                messages.error(
                    request,
                    "Invalid OTP"
                )

    else:
        form = OTPForm()

    return render(request, "verify_otp.html", {
        "form": form,
        "user": user
    })

import random

def resend_otp(request, user_id):

    user = get_object_or_404(User, id=user_id)

    otp = str(random.randint(100000,999999))

    EmailOTP.objects.update_or_create(
        user=user,
        defaults={
            "otp": otp
        }
    )

    send_mail(
        "New OTP",
        f"Your new OTP is {otp}",
        "urvishpatel008@gmail.com",
        [user.email],
        fail_silently=False,
    )

    messages.success(request,"New OTP Sent.")

    return redirect("verify_otp",user.id)

from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib import messages

def forgot_password(request):

    if request.method == "POST":

        email = request.POST.get("email")

        if not User.objects.filter(email=email).exists():

            messages.error(request, "Email is not registered.")

            return render(request, "forgot_password.html")

        user = User.objects.get(email=email)

        otp = str(random.randint(100000, 999999))

        EmailOTP.objects.update_or_create(
            user=user,
            defaults={
                "otp": otp
            }
        )

        send_mail(
            "Password Reset OTP",
            f"Your OTP is {otp}",
            "urvishpatel008@gmail.com",
            [email],
            fail_silently=False,
        )

        messages.success(request, "OTP has been sent to your email.")

        return redirect("verify_reset_otp", user.id)

    return render(request, "forgot_password.html")

from django.shortcuts import get_object_or_404

def verify_reset_otp(request, user_id):

    user = get_object_or_404(User, id=user_id)
    otp_obj = get_object_or_404(EmailOTP, user=user)

    if request.method == "POST":

        otp = request.POST.get("otp")

        if otp == otp_obj.otp:

            return redirect("reset_password", user.id)

        else:

            messages.error(request, "Invalid OTP")

    return render(request, "verify_reset_otp.html", {
        "user": user
    })

from django.contrib.auth.hashers import make_password

def reset_password(request, user_id):

    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":

        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:

            messages.error(
                request,
                "Passwords do not match."
            )

            return render(
                request,
                "reset_password.html",
                {
                    "user": user
                }
            )

        if len(password1) < 8:

            messages.error(
                request,
                "Password must be at least 8 characters."
            )

            return render(
                request,
                "reset_password.html",
                {
                    "user": user
                }
            )

        user.password = make_password(password1)
        user.save()

        # OTP Delete
        EmailOTP.objects.filter(user=user).delete()

        messages.success(
            request,
            "Password has been reset successfully. Please login."
        )

        return redirect("login")

    return render(
        request,
        "reset_password.html",
        {
            "user": user
        }
    )

def resend_reset_otp(request, user_id):

    user = get_object_or_404(User, id=user_id)

    otp = str(random.randint(100000, 999999))

    # જૂનો OTP હોય તો delete કરો
    EmailOTP.objects.filter(user=user).delete()

    # નવો OTP save કરો
    EmailOTP.objects.create(
        user=user,
        otp=otp
    )

    # Email મોકલો
    send_mail(
        "Password Reset OTP",
        f"Your new OTP is: {otp}",
        "urvishpatel008@gmail.com",
        [user.email],
        fail_silently=False,
    )

    messages.success(
        request,
        "New OTP has been sent to your email."
    )

    return redirect("verify_reset_otp", user.id)

def resend_otp(request):

    if request.method == "POST":

        otp = random.randint(100000,999999)

        request.session["otp"] = str(otp)

        send_mail(
            "Your OTP",
            f"OTP is {otp}",
            settings.EMAIL_HOST_USER,
            [request.session["email"]],
            fail_silently=False,
        )

        messages.success(request,"OTP Sent Again")

    return redirect("verify_otp")