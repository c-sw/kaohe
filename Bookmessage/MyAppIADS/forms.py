from django import forms
from MyAppIADS.models import Order, Review, Member
from django.contrib.auth.forms import UserCreationForm


class SearchForm(forms.Form):
    CATEGORY_CHOICES = [
        ('S', 'Scinece&Tech'),
        ('F', 'Fiction'),
        ('B', 'Biography'),
        ('T', 'Travel'),
        ('O', 'Other')
    ]
    name = forms.CharField(label='Your Name', max_length=100, required=False)
    category = forms.ChoiceField(label='Select a Category:', widget=forms.RadioSelect, choices=CATEGORY_CHOICES,
                                 required=False)
    max_price = forms.IntegerField(label='Maximum Price', min_value=0, required=True)


class OrderForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #    self.request = kwargs.pop('request')
    #    super(OrderForm, self).__init__(*args, **kwargs)
    #    self.fields['member'].label = "Member name:"
    #    self.fields['member'].initial = self.request.user.username

    class Meta:
        model = Order
        fields = ['books', 'member', 'order_type']
        widgets = {'books': forms.CheckboxSelectMultiple(), 'order_type': forms.RadioSelect}
        # labels = {'member': u'Member name', }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewer', 'book', 'rating', 'comments', 'date']
        widgets = {'book': forms.RadioSelect()}
        labels = {'reviewer': u'Please enter a valid email', 'rating': u'Rating: An integer between 1 and 5 '}


class MemberForm(UserCreationForm):
    class Meta:
        model = Member
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    first_name = forms.CharField(label='First Name', max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(label='Last Name', max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(label='Email', max_length=254, help_text='Required. Inform a valid email address.')


