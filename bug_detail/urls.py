from django.urls import include,path
from . import views


app_name = "detail"
urlpatterns = [
    path('<int:bug_id>', views.index, name= 'index'),

]