from django.contrib import admin
from django.urls import path, include
from MyAppIADS import views
from MyAppIADS.views import IndexView, DetailView

app_name = 'MyAppIADS'

urlpatterns = [
    path(r'', IndexView.as_view(), name='index'),
    path(r'about/', views.about, name='about_page'),
    path(r'<int:book_id>/', DetailView.as_view(), name='detail'),
    path(r'findbooks/', views.findbooks, name='findbooks'),
    path(r'placeorder/', views.place_order, name='placeorder'),
    path(r'review/', views.review, name='review'),
    path(r'login/' ,views.user_login, name='login'),
    path(r'logout/',views.user_logout, name='logout'),
    path(r'register/', views.register_member, name='register_member'),
    path(r'checkreview/<int:book_id>', views.chk_reviews,name='checkreview'),
    path(r'myorder/', views.myorders, name='my_order'),
    path(r'userratings/', views.UserRatings, name='User_Ratings'),
    path(r'chk_reviews/<int:book_id>', views.chk_reviews, name='chk_reviews'),
    path(r'checkreviews', views.checkreviews, name='checkreviews'),
    path(r'loginpage/', views.loginpage, name='loginpage'),
    ]


