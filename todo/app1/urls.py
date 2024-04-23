from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name='home'),
    path('login',views.loginn,name='login'),
    path('todo/<int:project_id>/',views.todo,name='todo'),
    path('add/<int:project_id>/',views.add_todo,name='add'),
    path('edit/<int:id>/', views.edit_todo, name='edit'),
    path('update/<int:id>/',views.update_todo,name="update"),
    path('delete/<int:id>/',views.delete_todo,name="delete"),
    path('updatestatus',views.update_todo_status,name='updatestatus'),
    path('signup',views.signup,name='signup'),
    path('logout',views.logoutt,name='logout'),
    path('edit_project/<int:project_id>/', views.edit_project, name='edit_project'),
]