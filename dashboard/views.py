from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404, redirect
from . forms import *
from django.contrib import messages
from django.views import generic
from .forms import DashboardForm
from django.forms.widgets import FileInput
from youtubesearchpython import VideosSearch
from youtubesearchpython import VideosSearch
from .forms import TodoForm
from .models import Todo
import requests
# Create your views here.

def home(request):
    return render(request,'dashboard/home.html')

def notes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
            notes.save()
        messages.success(request,f"Notes Added from {request.user.username} Successfully!")
    else:
          form = NotesForm()
    notes = Notes.objects.filter(user=request.user)       # request.user means login user
    context = {'notes':notes,'form':form}
    return render(request,'dashboard/notes.html',context)

def delete_note(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")

class NotesDetailView(generic.DetailView):
    model = Notes


#============================================ COMPLETE FOR NOTES =====================================================================================  


def homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
               finished = request.POST['is_finished']
               if finished == 'on':
                    finished = True
               else:
                    finished = False
            except:
                    finished = False
            homeworks = Homework(
            user=request.user,
            subject=request.POST['subject'],
            title=request.POST['title'],
            description=request.POST['description'],
            due=request.POST['due'],
            is_finished=finished
        )
        homeworks.save()
        messages.success(request, f"Homework Added from {request.user.username} Successfully!")
    else:    

        form = HomeworkForm()
    homework = Homework.objects.filter(user = request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False    

    context = {
               "homeworks":homework,
               "homework_done":homework_done,
               "form":form,                   
}
    return render(request,"dashboard/homework.html",context)


def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')


def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")


#============================================ COMPLETE FOR HOMEWORK =====================================================================================  

def youtube(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST.get('text', '').strip()
        if text:  # Check if the text is not empty
            video = VideosSearch(text, limit=10)
            result_list = []
            for i in video.result().get('result', []):  # Use .get() to handle potential None
                result_dict = {
                    'input': text,
                    'title': i.get('title', ''),
                    'duration': i.get('duration', ''),
                    'thumbnail': i['thumbnails'][0]['url'] if i['thumbnails'] else '',
                    'channel': i['channel']['name'],
                    'link': i['link'],
                    'views': i['viewCount'].get('short', ''),
                    'published': i['publishedTime']
                }
                
                desc = ''
                if i.get('descriptionSnippet'):
                    for j in i['descriptionSnippet']:
                        desc += j['text']
                result_dict['description'] = desc
                result_list.append(result_dict)

            context = {
                'form': form,
                'results': result_list  # Use 'results' to match the template
            }
            return render(request, 'dashboard/youtube.html', context)
    else:
        form = DashboardForm()
    
    context = {'form': form}
    return render(request, "dashboard/youtube.html", context)


#============================================ COMPLETE FOR YOUTUBE =====================================================================================  


def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST["is_finished"]
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
        todos = Todo(
            user = request.user,
            title = request.POST['title'],
            is_finished = finished
        )
        todos.save()
        messages.success(request,f"Todo Added from {request.user.username} !! ")
    else:    

        form = TodoForm()
    todo = Todo.objects.filter(user=request.user)
    
    if len(todo)==0:
        todos_done = True
    else:
        todos_done = False

    context = {
        'form':form,
        'todos':todo,
        'todos_done':todos_done
    }
    return render(request,"dashboard/todo.html",context)


def update_todo(request, pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('todo')


def delete_todo(request, pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect("todo")



#============================================ COMPLETE FOR TODO =====================================================================================  

# def books(request):
#     form = DashboardForm()
#     context = {"form": form}
#     return render(request,"dashboard/books.html",context)
def books(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST.get('text', '').strip()
        url = "https://www.googleapis.com/books/v1/volumes?q=" + text
        r = requests.get(url)
        answer = r.json()
        if text:  # Check if the text is not empty
            result_list = []
            for i in range(10):  # Use .get() to handle potential None
                result_dict = {
                    'title': answer['items'][i]['volumeInfo']['title'],
                    'subtitle': answer['items'][i]['volumeInfo'].get('subtitle'),
                    'description': answer['items'][i]['volumeInfo'].get('description'),
                    'count': answer['items'][i]['volumeInfo'].get('pageCount'),
                    'categories': answer['items'][i]['volumeInfo'].get('categories'),
                    'rating': answer['items'][i]['volumeInfo'].get('averageRating'),
                    'thumbnail': answer['items'][i]['volumeInfo'].get('imageLinks', {}).get('thumbnail'),
                    'preview': answer['items'][i]['volumeInfo'].get('previewLink')
                }
                result_list.append(result_dict)

            context = {
                'form': form,
                'results': result_list
            }
            return render(request, 'dashboard/books.html', context)
    else:
        form = DashboardForm()

    context = {'form': form}
    return render(request, "dashboard/books.html", context)


#============================================ COMPLETE FOR BOOKS =====================================================================================  


from django.shortcuts import render
from googletrans import Translator

def dictionary(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST.get('text', '').strip()
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en_US/{text}"
        r = requests.get(url)
        answer = r.json()
        
        # Initialize Google Translator
        translator = Translator()

        try:
            # Safely get values with .get() to prevent errors if data is missing
            phonetics = answer[0].get('phonetics', [{}])[0].get('text', 'N/A')
            audio = answer[0].get('phonetics', [{}])[0].get('audio', '')
            definition = answer[0].get('meanings', [{}])[0].get('definitions', [{}])[0].get('definition', 'No definition available')
            example = answer[0].get('meanings', [{}])[0].get('definitions', [{}])[0].get('example', 'No example available')
            synonyms = answer[0].get('meanings', [{}])[0].get('definitions', [{}])[0].get('synonyms', [])

            # Translate the main word to Hindi and Marathi
            meaning_hindi = translator.translate(text, dest='hi').text
            meaning_marathi = translator.translate(text, dest='mr').text

            context = {
                'form': form,
                'input': text,
                'phonetics': phonetics,
                'audio': audio,
                'definition': definition,
                'meaning_hindi': meaning_hindi,
                'meaning_marathi': meaning_marathi,
                'example': example,
                'synonyms': synonyms
            }
        except (IndexError, KeyError):
            context = {
                'form': form,
                'input': '',
                'error': "Word not found or API limit exceeded"
            }

        return render(request, "dashboard/dictionary.html", context)

    else:
        form = DashboardForm()
        context = {'form': form}
    return render(request, "dashboard/dictionary.html", context)

#============================================ COMPLETE FOR DICTIONARY =====================================================================================  
import wikipedia
from wikipedia.exceptions import PageError, DisambiguationError
from django.shortcuts import render

def wiki(request):
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()  # Get and trim the text input
        form = DashboardForm(request.POST)
        
        try:
            # Attempt to retrieve the Wikipedia page
            search = wikipedia.page(text)
            context = {
                'form': form,
                'title': search.title,
                'link': search.url,
                'details': search.summary,
            }

        except PageError:
            # If no page is found, show an error message
            context = {
                'form': form,
                'error': f"No page found for '{text}'. Please try another search term."
            }
        
        except DisambiguationError as e:
            # If multiple pages are found, list possible options
            context = {
                'form': form,
                'error': f"The term '{text}' is ambiguous. Possible options: {', '.join(e.options)}"
            }
        
        return render(request, "dashboard/wiki.html", context)

    else:
        form = DashboardForm()
        context = {
            'form': form
        }
    return render(request, "dashboard/wiki.html", context)


#============================================ COMPLETE FOR WIKIPEDIA =====================================================================================  
def conversion(request):
    if request.method == "POST":
        form = ConversionForm(request.POST)
        answer = ''
        
        if request.POST.get('measurement') == 'length':
            measurement_form = ConversionLengthForm()  # Make sure this form has options for yard, foot, etc.
            
            # Prepare context and handle input if it's there
            if 'input' in request.POST:
                first = request.POST.get('measure1')
                second = request.POST.get('measure2')
                input_value = request.POST.get('input')
                
                if input_value and input_value.isdigit() and int(input_value) >= 0:
                    input_value = int(input_value)
                    
                    if first == 'yard' and second == 'foot':
                        answer = f'{input_value} yard = {input_value * 3} foot'
                    elif first == 'foot' and second == 'yard':
                        answer = f'{input_value} foot = {input_value / 3} yard'
            
            context = {
                'form': form,
                'm_form': measurement_form,
                'input': True,
                'answer': answer
            }

        elif request.POST.get('measurement') == 'mass':
            measurement_form = ConversionMassForm()
            
            if 'input' in request.POST:
                first = request.POST.get('measure1')
                second = request.POST.get('measure2')
                input_value = request.POST.get('input')
                
                if input_value and input_value.isdigit() and int(input_value) >= 0:
                    input_value = int(input_value)
                    
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input_value} pound = {input_value * 0.453592} kilogram'
                    elif first == 'kilogram' and second == 'pound':
                        answer = f'{input_value} kilogram = {input_value * 2.20462} pound'
            
            context = {
                'form': form,
                'm_form': measurement_form,
                'input': True,
                'answer': answer
            }

    else:
        form = ConversionForm()
        context = {
            'form': form,
            'input': False
        }

    return render(request, "dashboard/conversion.html", context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"Account Created for {username} !! ")
            return redirect("login")
    else:        
        form = UserRegistrationForm()
    context = {
       'form':form
    }
    return render(request,"dashboard/register.html",context)




# def profile(request):
#     homeworks = Homework.objects.filter(is_finished=False, user=request.user)
#     todos = Todo.objects.filter(is_finished=False, user=request.user)

#     if len(homeworks) == 0:
#         homework_done = True
#     else:
#         homework_done = False

#     if len(todos) == 0:
#         todos_done = True
#     else:
#         todos_done = False

#     context = {
#         'homeworks': homeworks,
#         'todos': todos,
#         'homework_done': homework_done,
#         'todos_done': todos_done
#     }

#     return render(request,"dashboard/profile.html")





from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Todo, Homework

@login_required
def profile(request):
    # Fetch incomplete todos and homeworks for the logged-in user
    homeworks = Homework.objects.filter(is_finished=False, user=request.user)
    todos = Todo.objects.filter(is_finished=False, user=request.user)

    # Check if all todos and homeworks are completed
    homework_done = not homeworks.exists()
    todos_done = not todos.exists()

    context = {
        'homeworks': homeworks,
        'todos': todos,
        'homework_done': homework_done,
        'todos_done': todos_done,
    }

    return render(request, "dashboard/profile.html", context)

@login_required
def update_todo(request, id):
    # Toggle the completion status of a Todo
    todo = get_object_or_404(Todo, id=id, user=request.user)
    todo.is_finished = not todo.is_finished
    todo.save()
    return redirect('profile')

@login_required
def delete_todo(request, id):
    # Delete a Todo item
    todo = get_object_or_404(Todo, id=id, user=request.user)
    todo.delete()
    return redirect('profile')

@login_required
def update_homework(request, id):
    # Toggle the completion status of a Homework
    homework = get_object_or_404(Homework, id=id, user=request.user)
    homework.is_finished = not homework.is_finished
    homework.save()
    return redirect('profile')

@login_required
def delete_homework(request, id):
    # Delete a Homework item
    homework = get_object_or_404(Homework, id=id, user=request.user)
    homework.delete()
    return redirect('profile')


# views.py
from django.shortcuts import get_object_or_404, redirect
from .models import Todo

def delete_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.delete()
    return redirect('profile')  # or wherever you want to redirect after deletion


# views.py
from django.shortcuts import get_object_or_404, redirect
from .models import Homework

def delete_homework(request, pk):
    homework = get_object_or_404(Homework, pk=pk)
    homework.delete()
    return redirect('profile')  # Redirect to profile page after deletion

