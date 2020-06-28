from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import SearchForm, OrderForm, ReviewForm, MemberForm
from loadin.models import User
from MyAppIADS.models import Book, Member, Review, Order
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
import random, datetime
from django.views.generic.base import View

def index(request):
    if 'username' in request.session:
        if 'last_login' in request.session:
            last_log = request.session.get('last_login')
        else:
            last_log = "more than one hour ago"
        booklist = Book.objects.all().order_by('pk')[:10]
        member = Member.objects.filter(username=request.session.get('username'))
        image = member.image.url
        return render(request, 'MyApp/index0.html', {'booklist': booklist, 'last_login': last_log})
    else:
        return render(request, 'MyApp/index0.html', {})


def about(request):
    if 'lucky_num' in request.session:
        mynum = request.session.get('lucky_num')
        return render(request, 'MyApp/about.html', {'mynum': mynum})
    else:
        request.session['lucky_num'] = random.randint(1, 101)
        request.session.set_expiry(5 * 60)
        return render(request, 'MyApp/about.html')


class IndexView(View):

    def get(self, request):
                if 'last_login' in request.session:
                    last_log = request.session.get('last_login')
                else:
                    last_log = "more than one hour ago"
                booklist = Book.objects.all().order_by('pk')[:10]
                return render(request, 'MyApp/index0.html', {'booklist': booklist, 'last_login': last_log})


class AboutView(View):

    def get(self, request):
        if request.session.has_key('username'):
            if 'lucky_num' in request.session:
                mynum = request.session.get('lucky_num')
                return render(request, 'MyApp/about.html', {'mynum': mynum})
            else:
                request.session['lucky_num'] = random.randint(1, 101)
                request.session.set_expiry(5 * 60)
                return render(request, 'MyApp/about.html')
        else:
            return render(request, 'loadin/login.html')


def detail(request, book_id):
    book_Detail = get_object_or_404(Book, id=book_id)
    return render(request, 'MyApp/detail.html',
                  {'book_title': book_Detail.title.upper(), 'book_price': book_Detail.price,
                   'book_publisher': book_Detail.publisher})


class DetailView(View):

    def get(self, request, book_id):
        book_Detail = get_object_or_404(Book, id=book_id)
        id = str(book_id)+'.jpg'
        return render(request, 'MyApp/detail.html',
                      {'book_title': book_Detail.title.upper(), 'book_price': book_Detail.price,
                       'book_publisher': book_Detail.publisher, 'id': id})


def UserRatings(request):
    dictn = {}
    li = []
    for i in range(1, 9):
        B = Book.objects.get(pk=i)
        if B:
            R = Review.objects.filter(book__id=B.id)
            if R:
                total = 0
                i = 0
                for r in R:
                    total += r.rating
                    i += 1
                ave = total / i
                dictn[ave] = B.title
    li = list(dictn.items())
    li.sort(reverse=True)
    return render(request, 'MyApp/UserRatings.html', {'Rating': li})


def findbooks(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            max_price = form.cleaned_data['max_price']
            if category:
                booklist = Book.objects.filter(category=category).filter(price__lte=max_price)
                return render(request, 'MyApp/results.html',
                              {'booklist': booklist, 'name': name, 'category': category, 'max_price': max_price})
            else:
                booklist = Book.objects.filter(price__lte=max_price)
                return render(request, 'MyApp/results.html',
                              {'booklist': booklist, 'name': name, 'max_price': max_price})
        else:
            return HttpResponse('Invalid data')
    else:
        form = SearchForm()
        return render(request, 'MyApp/findbooks.html', {'form': form})


def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            books = form.cleaned_data['books']
            #m = request.session.get('username')
            #member = Member.objects.get(username=m)
            order = form.save()
            member = order.member
            type = order.order_type
            order.save()
            if type == 1:
                for b in order.books.all():
                    member.borrowed_books.add(b)
            return render(request, 'MyApp/order_response.html', {'books': books, 'order': order, })
        else:
            return render(request, 'MyApp/placeorder.html', {'form': form})

    else:
        form = OrderForm()
        return render(request, 'MyApp/placeorder.html', {'form': form})



def review(request):
    status = request.session.get('status')
    if status == 1 or status == 2:
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                reviewer = form.cleaned_data['reviewer']
                comments = form.cleaned_data['comments']
                date = form.cleaned_data['date']
                rating = form.cleaned_data['rating']
                review1 = form.save()
                book = review1.book
                book.num_reviews += 1
                book.save()
                booklist = Book.objects.all()
                return render(request, 'MyApp/index0.html', {'booklist': booklist})
            else:
                return render(request, 'MyApp/review.html', {'form': form})
        else:
            form = ReviewForm()
            return render(request, 'MyApp/review.html', {'form': form})
    else:
        return HttpResponse('You must be either a Premium or a Regular Member to submit reviews')


def user_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                current_login_time = str(datetime.datetime.now())
                request.session['last_login'] = current_login_time
                request.session.set_expiry(60 * 60)
                request.session['username'] = username
                request.session['status'] = Member.objects.get(username=username).status
                if 'bookid' not in request.session:  #
                    return HttpResponseRedirect(reverse('MyAppIADS:index'))
                else:
                    return chk_reviews(request, request.session.get('bookid'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')

    return render(request, 'MyApp/login.html')


def register_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            msg = 'Successfully registered! Kindly log in'
            return render(request, 'loadin/registration.html', {'msg': msg})
        else:
            return render(request, 'loadin/registration.html', {'form': User()})
    else:
        form = MemberForm()
        return render(request, 'loadin/registration.html', {'form': form})


def chk_reviews(request, book_id):
    request.session['bookid'] = book_id
    if request.session.has_key('username'):
        B = get_object_or_404(Book, id=book_id)
        R = Review.objects.filter(book__id=B.id)
        if Member.username:
            # user = authenticate()
            if R:
                total = 0
                i = 0
                for r in R:
                    total += r.rating
                    i += 1
                ave = total / i
                return render(request, 'MyApp/checkreviews.html',
                              {'review': R, 'Book': B, 'average': ave, 'total': total, 'count': i})
            else:
                return HttpResponse('There are no reviews')
        else:
            return HttpResponse('You are not a registered member')
    else:
        bookid = request.session.get('bookid')
        return render(request, 'loadin/login.html', {'book': bookid})


def checkreviews(request):
    booklist = Book.objects.all().order_by('pk')[:10]
    return render(request, 'MyApp/chk_reviews.html', {'booklist': booklist})


def loginpage(request):
    return render(request,'MyApp/index.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('MyAppIADS:index'))


@login_required
def myorders(request):
    if Member.username:
        order = Order.objects.filter(member__username=request.user.username)
        return render(request, 'MyApp/myorder.html', {'order': order})
    else:
        return HttpResponse('You are not a registered member')
