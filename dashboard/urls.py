from django.urls import path
from . import views    # . (dot) means current application
import httpx

urlpatterns = [
      path('', views.home, name='home'),
    path('notes',views.notes,name='notes'),
    path('delete_note/<int:pk>',views.delete_note,name="delete-note"),
    path('notes_detail/<int:pk>',views.NotesDetailView.as_view(),name="notes-detail"),

#============================================ COMPLETE FOR NOTES =====================================================================================  

    path('homework',views.homework,name='homework'),
    path('update_homework/<int:pk>',views.update_homework,name='update-homework'),
    path('delete_homework/<int:pk>',views.delete_homework,name='delete-homework'),

#============================================ COMPLETE FOR HOMEWORK =====================================================================================  

    path('youtube',views.youtube,name='youtube'),

#============================================ COMPLETE FOR YOUTUBE =====================================================================================  

    path('todo',views.todo,name='todo'),
    path('update_todo/<int:id>',views.update_todo,name='update-todo'),
    path('delete_todo/<int:pk>',views.delete_todo,name='delete-todo'),

#============================================ COMPLETE FOR TODO =====================================================================================  

    path('books',views.books,name='books'),

#============================================ COMPLETE FOR BOOKS =====================================================================================  

    path('dictionary',views.dictionary,name='dictionary'),

#============================================ COMPLETE FOR DICTIONARY =====================================================================================  

    path('wiki',views.wiki,name='wiki'),

#============================================ COMPLETE FOR WIKIPEDIA =====================================================================================  

   path('conversion',views.conversion,name='conversion'),

]
