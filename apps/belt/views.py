from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import re
import bcrypt
from apps.belt.models import *
EMAIL_REGEX= re.compile (r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


def index(request):
    
        return render(request,'belt/index.html')

def register(request):
    # VALIDATIONS
    error=False

    for key, value in request.POST.items():
        if len(value)==0:
            messages.error(request, key + ' cannot be empty')
            error=True

    if len(request.POST['name'])>2 and not request.POST['name'].isalpha():
        messages.error(request,'First name must be letters')
        print('name must be letters')
        error=True

    if len(request.POST['alias'])>0 and not request.POST['alias'].isalpha():
        messages.error(request,'Alias must be letters')
        print('Alias must be letters')
        error=True

    if not EMAIL_REGEX.match(request.POST['email']):
        messages.error(request,'Bad email')
        error=True
    
    elif len(User.objects.filter(email=request.POST['email']))>0:
        messages.error(request,'Email already exists')
        error=True

    if len(request.POST['password'])<8:
        messages.error(request,'Password must be longer')
        error=True
    
    if request.POST['confirm_password']!=request.POST['password']:
        messages.error(request,'Passwords must match')
        error=True
    
    if error:
        return redirect('/')
        
    new_user=User.objects.create(name=request.POST['name'], 
    alias=request.POST['alias'], 
    email=request.POST['email'], 
    password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))

    request.session['u_id']=new_user.id


    return redirect('/books')

def login(request):

    user = User.objects.filter(email=request.POST['email'])

    if len(user)==0:
        print('Email does not exist')
        messages.error(request,'Try again')
        return redirect('/')
    
    if not bcrypt.checkpw(request.POST['password'].encode(),user[0].password.encode()):
        print('passwords dont match')
        messages.error(request,'Try again')
        return redirect('/')

    request.session['u_id']=user[0].id

    return redirect('/books')

def books(request):

    if 'u_id' not in request.session:
        messages.error(request,'Must log in')
        return redirect('/')

    user=User.objects.get(id=request.session['u_id'])
    books=Book.objects.all()
    reviews=Review.objects.all()
    recent_reviews=Review.objects.order_by('-created_at')[:4]
    context={
        "user" : user,
        "books" : books,
        "reviews" : reviews,
        "recent_reviews" : recent_reviews,
    }

    return render(request,'belt/books.html', context)

def add(request):

    authors=Book.objects.all().values('author').distinct()
    
    context={
        "authors" : authors
    }

    return render(request,'belt/add.html', context)

def process(request):

    if len(request.POST['title'])>1 and len(request.POST['author'])>1:

        book_id=Book.objects.create(title=request.POST['title'],
        author=request.POST['author'], 
        creator=User.objects.get(id=request.session['u_id']))

        review_id=Review.objects.create(rating=request.POST['rating'],
        reviews=request.POST['review'],
        reviewer=User.objects.get(id=request.session['u_id']),
        books=book_id)
    
    if len(request.POST['title'])>1 and len(request.POST['author'])==0:
        book_id=Book.objects.create(title=request.POST['title'],
        author=request.POST['author2'], 
        creator=User.objects.get(id=request.session['u_id']))

        review_id=Review.objects.create(rating=request.POST['rating'],
        reviews=request.POST['review'],
        reviewer=User.objects.get(id=request.session['u_id']),
        books=book_id)


    return redirect('/books')

def info(request, id):

    book=Book.objects.get(id=id)
    reviews=book.reviews.all()
    context={
        "book" : book,
        "reviews": reviews
    }

    return render(request,'belt/info.html', context)

def users(request, id):
    
    users=User.objects.get(id=id)
    reviews=Review.objects.filter(reviewer=users)
    stinks=Review.objects.filter(reviewer=User.objects.last()).values('books').distinct()

    context={
        "users":users,
        "reviews": reviews,
        "stinks": stinks
    }

    return render(request,'belt/users.html',context)

def review(request, id):

    book_id=Book.objects.get(id=id)
    
    if len(request.POST['review'])<1:
        messages.error(request,'Cannot be empty')
        return redirect(f'/books/{id}')
    
    Review.objects.create(rating=request.POST['rating'],
    reviews=request.POST['review'],
    reviewer=User.objects.get(id=request.session['u_id']),
    books=book_id)

    return redirect('/books')


def delete(request, id):
    
    book_id=Review.objects.get(id=id).books.id
    Review.objects.get(id=id).delete()

    return redirect(f'/books/{book_id}')

def logout(request):

    request.session.pop('u_id')
    return redirect('/')
