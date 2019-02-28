from django.db import models

class User(models.Model):
    name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"id={self.id}, name={self.name}, email={self.email}"

class Book(models.Model):
    title = models.CharField(max_length = 255)
    author = models.CharField(max_length = 255)
    creator = models.ForeignKey(User, related_name='books_created')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"id={self.id}, title={self.title}, author={self.author}"

class Review(models.Model):
    rating = models.IntegerField()
    reviews = models.CharField(max_length = 255)
    reviewer = models.ForeignKey(User, related_name='reviews')
    books = models.ForeignKey(Book, related_name='reviews')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"id={self.id}, reviews={self.reviews}, books={self.books}"


# REVIEW A BOOK

# Review.objects.create(rating=request.POST['rating'],
# reviews=request.POST['review'],
# reviewer=User.objects.get(id=request.session['u_id']),
# books=book_id)

# TOTAL REVIEWS
# {{ reviews | length }}

# ADDING A BOOK AND REVIEW SAME TIME

# book_id=Book.objects.create(title=request.POST['title'],
# author=request.POST['author'], 
# creator=User.objects.get(id=request.session['u_id']))

# review_id=Review.objects.create(rating=request.POST['rating'],
# reviews=request.POST['review'],
# reviewer=User.objects.get(id=request.session['u_id']),
# books=book_id)
