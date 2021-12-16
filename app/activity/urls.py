from django.urls import path

from activity import views

app_name = 'activity'

urlpatterns = [
    path('create_activity/', views.BaseActivityViewSet),
    path('manage_activity/', views.ActivityViewSet)
]
