from django.urls import path
from . import views

# defined the urls for my app here
urlpatterns = [
    # url for homepage
    path('',views.index,name = 'index'),
    # url for create page
    path('create/' ,views.create, name = 'create'),
    # url for update page which takes as an argument the id of the model you want to edit
    path(r'^update/(?P<model_id>\d+)/$',views.update, name = 'update'),
]