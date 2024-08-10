from django.urls import path
from . import views

urlpatterns = [
    path('items/', views.ItemsView.as_view(), name='items_view'),
    path('items/<int:id>/', views.ItemsView.as_view()),
    path('items/like/<int:id>/', views.likeItem),
]