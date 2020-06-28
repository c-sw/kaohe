from django.db import models
import datetime
from django.core.validators import *
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.safestring import mark_safe

class Publisher(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField()
    city = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=20, blank=False, default='USA')

    def __str__(self):
        return self.name


class Book(models.Model):
    CATEGORY_CHOICES = [
        ('S', 'Scinece&Tech'),
        ('F', 'Fiction'),
        ('B', 'Biography'),
        ('T', 'Travel'),
        ('O', 'Other')
    ]
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, default='S')
    num_pages = models.PositiveIntegerField(default=100)
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                validators=[MaxValueValidator(1000), MinValueValidator(0)])
    publisher = models.ForeignKey(Publisher, related_name='books', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    num_reviews = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.title


class Member(User):
    STATUS_CHOICES = [
        (1, 'Regular member'),
        (2, 'Premium Member'),
        (3, 'Guest Member'),
    ]

    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=20, default='Windsor')
    province = models.CharField(max_length=2, default='ON')
    last_renewal = models.DateField(default=timezone.now)
    auto_renew = models.BooleanField(default=True)
    borrowed_books = models.ManyToManyField(Book, blank=True, related_name='bb')
    image = models.ImageField(upload_to='profile_imamge', blank=True)


    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" style="width: 200px; height:200px;" />' % self.image.url)
        else:
            return 'No Image Found'
    image_tag.short_description = 'Image'

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Order(models.Model):
    CHOICE = [
        (0, 'Purchase'),
        (1, 'Borrow')
    ]
    member = models.ForeignKey(Member, related_name='MemberOrder', on_delete=models.CASCADE)
    books = models.ManyToManyField(Book, related_name='orderbooks')
    order_type = models.IntegerField(choices=CHOICE, default=1)
    order_date = models.DateField(default=timezone.now)

    def total_items(self):
        return self.books.count()

    def __str__(self):
        return '{} {} {} {} {}'.format(self.member.first_name, self.member.last_name, self.order_date,
                                       self.total_items(), self.pk)


class Review(models.Model):
    reviewer = models.EmailField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    comments = models.TextField(blank=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return '{} {} {}'.format(self.book, self.reviewer, self.rating)



# class MemberF(models.Model):
#     user = models.ForeignKey('loadin.User',on_delete=m)
