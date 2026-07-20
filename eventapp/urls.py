from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [

    # Home
    path('', views.home, name='home'),

    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),

    # OTP Verification
    path(
        'verify-otp/<int:user_id>/',
        views.verify_otp,
        name='verify_otp'
    ),

    path(
        'resend-otp/<int:user_id>/',
        views.resend_otp,
        name='resend_otp'
    ),

    # Forgot Password OTP
    path(
        'forgot-password/',
        views.forgot_password,
        name='forgot_password'
    ),

    path(
        'verify-reset-otp/<int:user_id>/',
        views.verify_reset_otp,
        name='verify_reset_otp'
    ),

    path(
        'reset-password/<int:user_id>/',
        views.reset_password,
        name='reset_password'
    ),

    # Events
    path(
        'events/',
        views.event_list,
        name='events'
    ),

    path(
        'event-details/<str:event_name>/',
        views.event_details,
        name='event_details'
    ),

    # Booking
    path(
        'book-event/',
        views.book_event,
        name='book_event'
    ),

    path(
        'payment/<int:booking_id>/',
        views.payment_view,
        name='payment'
    ),

    path(
        'my-bookings/',
        views.my_bookings,
        name='my_bookings'
    ),

    path(
        'cancel-booking/<int:booking_id>/',
        views.cancel_booking,
        name='cancel_booking'
    ),

    # Packages
    path(
        'packages/',
        views.packages,
        name='packages'
    ),

    path(
        'package-details/<str:package_name>/',
        views.package_details,
        name='package_details'
    ),

    # Gallery
    path(
        'gallery/',
        views.gallery,
        name='gallery'
    ),

    # Reviews
    path(
        'reviews/',
        views.review_view,
        name='reviews'
    ),

    # Contact
    path(
        'contact/',
        views.contact_view,
        name='contact'
    ),

    # Dashboard
    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    # Invoice
    path(
        'invoice/<int:booking_id>/',
        views.generate_invoice,
        name='invoice'
    ),

    # Change Password
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='change_password.html'
        ),
        name='change_password'
    ),

    path(
        'change-password-done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='change_password_done.html'
        ),
        name='password_change_done'
    ),

    path(
    "resend-reset-otp/<int:user_id>/",
    views.resend_reset_otp,
    name="resend_reset_otp"
),

    path(
    "verify-reset-otp/<int:user_id>/",
    views.verify_reset_otp,
    name="verify_reset_otp"
),

path(
    "resend-reset-otp/<int:user_id>/",
    views.resend_reset_otp,
    name="resend_reset_otp"
),

path("resend-otp/", views.resend_otp, name="resend_otp"),

path(
    "resend-reset-otp/<int:user_id>/",
    views.resend_reset_otp,
    name="resend_reset_otp"
),

path("resend-reset-otp/<int:id>/", views.resend_reset_otp, name="resend_reset_otp")
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )