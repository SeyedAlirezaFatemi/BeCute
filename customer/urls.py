from django.urls import path

from . import views

urlpatterns = [
    path('', views.main),
    path('reserve/<int:shop_uid>/', views.reserve),
    path('reserve/<int:shop_uid>/<str:start>/<str:end>/', views.reserve),
    # path('reserve/<str:barber>/', views.reserve),
    path('search/', views.search),
    path('profile/', views.profile),

]
