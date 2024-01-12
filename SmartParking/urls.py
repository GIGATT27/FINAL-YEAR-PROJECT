from django.urls import path
from . import views

app_name = 'SmartParking'

urlpatterns = [
    path('',views.home, name='home'),
    # path('signout',views.signout,name='signout'),
    # path('signup/',views.signup,name='signup'),
    path('signin/',views.signin,name='signin'),
    path('detail/', views.detail,name='detail'),
    # path('parking_lot_state/', views.parking_lot_state, name='parking_lot_state'),
    # path('free_spaces/', views.free_spaces, name='free_spaces'),
]