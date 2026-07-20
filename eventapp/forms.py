from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import EventBooking, Review, Contact, Payment

class RegisterForm(UserCreationForm):

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].label = "Name"

        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter Your Name'
        })

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter Email Address'
        })

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter Password'
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })

    def save(self, commit=True):

        user = super().save(commit=False)

        user.username = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

class BookingForm(forms.ModelForm):

    class Meta:
        model = EventBooking

        fields = [
            'name',
            'contact_number',
            'category',
            'package',
            'event_date',
            'venue',
            'guests'
        ]

        widgets = {

            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Your Full Name'
            }),

            'contact_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Contact Number'
            }),

            'event_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),

            'venue': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Event Venue'
            }),

            'guests': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Number of Guests'
            }),

            'category': forms.Select(attrs={
                'class': 'form-control'
            }),

            'package': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        label="⭐ Your Rating"
    )

    comment = forms.CharField(
        label="💬 Share Your Experience",
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'Tell us about your experience...'
        })
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'message']


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method', 'screenshot']


# from django import forms
# from .models import Review

# class ReviewForm(forms.ModelForm):
#     class Meta:
#         model = Review
#         fields = ['name', 'photo', 'rating', 'comment']

# class ReviewForm(forms.ModelForm):
#     class Meta:
#         model = Review
#         fields = ['name', 'photo', 'rating', 'comment']

#         widgets = {
#             'name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter Your Name'
#             }),

#             'photo': forms.FileInput(attrs={
#                 'class': 'form-control'
#             }),

#             'rating': forms.Select(attrs={
#                 'class': 'form-control'
#             }),

#             'comment': forms.Textarea(attrs={
#                 'class': 'form-control',
#                 'rows': 4,
#                 'placeholder': 'Share Your Experience'
#             }),
#         }

# from django import forms
# from .models import Review

# RATING_CHOICES = [
#     (1, '⭐'),
#     (2, '⭐⭐'),
#     (3, '⭐⭐⭐'),
#     (4, '⭐⭐⭐⭐'),
#     (5, '⭐⭐⭐⭐⭐'),
# ]

# class ReviewForm(forms.ModelForm):

#     rating = forms.ChoiceField(
#         choices=RATING_CHOICES,
#         widget=forms.RadioSelect
#     )

#     class Meta:
#         model = Review
#         fields = ['name', 'photo', 'rating', 'comment']

#         widgets = {
#             'name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter Your Name'
#             }),

#             'photo': forms.FileInput(attrs={
#                 'class': 'form-control'
#             }),

#             'comment': forms.Textarea(attrs={
#                 'class': 'form-control',
#                 'rows': 4,
#                 'placeholder': 'Share Your Experience'
#             }),
#         }


from django import forms
from .models import Review

RATING_CHOICES = [
    (1, '⭐'),
    (2, '⭐⭐'),
    (3, '⭐⭐⭐'),
    (4, '⭐⭐⭐⭐'),
    (5, '⭐⭐⭐⭐⭐'),
]

class ReviewForm(forms.ModelForm):

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect
    )

    class Meta:
        model = Review
        fields = ['name', 'photo', 'rating', 'comment']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Your Name'
            }),

            'photo': forms.FileInput(attrs={
                'class': 'form-control'
            }),

            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share Your Experience'
            }),
        }

class OTPForm(forms.Form):

    otp = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter 6 Digit OTP"
        })
    )