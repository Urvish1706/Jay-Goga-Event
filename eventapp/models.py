from time import timezone

from django.db import models
from django.contrib.auth.models import User



class EventCategory(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/')
    description = models.TextField()

    def __str__(self):
        return self.name


class Package(models.Model):
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    package_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.package_name


class Staff(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.name

EVENT_CHOICES = [
    ('Wedding Event', 'Wedding Event'),
    ('Birthday Party', 'Birthday Party'),
    ('Engagement Event', 'Engagement Event'),
    ('Corporate Event', 'Corporate Event'),
    ('Anniversary Event', 'Anniversary Event'),
    ('Festival Event', 'Festival Event'),
    ('Concert Event', 'Concert Event'),
    ('Baby Shower', 'Baby Shower'),
    ('Farewell Party', 'Farewell Party'),
    ('SchoolCollege Event', 'SchoolCollege Event'),
    ('House Warming', 'House Warming'),
    ('Cultural Program', 'Cultural Program'),
]

PACKAGE_CHOICES = [
    ('Silver Package', 'Silver Package'),
    ('Gold Package', 'Gold Package'),
    ('Platinum Package', 'Platinum Package'),
    ('Diamond Package', 'Diamond Package'),
    ('Royal Package', 'Royal Package'),
    ('Wedding Premium', 'Wedding Premium'),
]

class EventBooking(models.Model):

    STATUS = (
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled'),
)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)

    category = models.CharField(
    max_length=100,
    choices=EVENT_CHOICES
)
    package = models.CharField(
    max_length=100,
    choices=PACKAGE_CHOICES
)

    event_date = models.DateField()
    venue = models.CharField(max_length=200)
    guests = models.IntegerField()

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Payment(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Verified', 'Verified'),
        ('Rejected', 'Rejected'),
    ]

    PAYMENT_CHOICES = [
        ('COD', 'Cash On Delivery'),
        ('ONLINE', 'Online Payment'),
    ]

    booking = models.ForeignKey(
        EventBooking,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_CHOICES,
        default='COD'
    )

    screenshot = models.ImageField(
        upload_to='payment_screenshots/',
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.booking.name} - {self.payment_method}"

class Gallery(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='gallery/')

    def __str__(self):
        return self.title


# class Review(models.Model):
#     name = models.CharField(max_length=100)
#     photo = models.ImageField(upload_to='reviews/')
#     rating = models.IntegerField()
#     comment = models.TextField()

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()

    def __str__(self):
        return self.name
    
from django.db import models

class Review(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='reviews/')
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return self.name
    

# class Payment(models.Model):
#     screenshot = models.ImageField(
#         upload_to='payment_screenshots/',
#         blank=True,
#         null=True
#     )

from django.contrib.auth.models import User
from django.db import models

class EmailOTP(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.otp}"