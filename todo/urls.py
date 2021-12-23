from django.urls import path
from . import views

urlpatterns = [
    # path('list/', views.list_todo, name='list'),
    # path('add_todo/', views.add_todo, name='add_todo'),
    # path('delete_todo/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    # path('update_todo/<str:todo_id>/', views.update_todo, name='update_todo'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout', views.logoutPage, name= 'logout'),
    path('', views.home, name='home'),
    path('products/', views.product, name='products'),
    path('customers/<str:pk>/', views.customer, name='customers'),
    path('create_order/<str:pk>/', views.createOrder, name='create_order'),
    path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>/', views.deleteOrder, name='delete_order'),
]