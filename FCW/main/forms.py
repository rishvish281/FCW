from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import ProductReview,UserAddressBook

class SignupForm(UserCreationForm):
	class Meta:
		model=User
		fields=('first_name','last_name','email','username','password1','password2')

# Review Add Form
class ReviewAdd(forms.ModelForm):
	class Meta:
		model=ProductReview
		fields=('review_text','review_rating')

# AddressBook Add Form
class AddressBookForm(forms.ModelForm):
	class Meta:
		model=UserAddressBook
		fields=('address','mobile','status')

# ProfileEdit
class ProfileForm(UserChangeForm):
	class Meta:
		model=User
		fields=('first_name','last_name','email','username')

from django import forms
from main.models import Product, ProductAttribute

class GymCateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'title','specs', 'detail', 'slug', 'category', 'brand', 'status', 'is_featured'
        ]
        labels = {
            'title': 'Gym Name',
            'specs': 'Specialization',
            'slug': 'Address',
            'detail': 'Details',
            'category': 'Place',
            'brand': 'Gender',
            'status': 'Mornings',
            'is_featured': 'Evenings',
        }

    def __init__(self, *args, **kwargs):
        super(GymCateForm, self).__init__(*args, **kwargs)





class GymPriceForm(forms.ModelForm):
    class Meta:
        model = ProductAttribute
        fields = [
            'product', 'color', 'size', 'price', 'image'
        ]
        labels = {
            'product': 'Select your entered Gym Name again',
            'color': 'Timing',
            'size': 'Gym Capacity',
            'price': 'Hourly rate',
            'image': 'Image'
        }
    def _init_(self, *args, **kwargs):
        super(GymPriceForm, self)._init_(*args, **kwargs)
        # Add any customization for form fields here if needed