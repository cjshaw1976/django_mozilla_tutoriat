import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.views import generic

from .models import Book, Author, BookInstance, Genre

def index(request):
    """
    View function for home page of site.
    """
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()
    num_genre=Genre.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    visit={'num':num_visits,
           'last':request.session.get('last_visit', '')}
    request.session['num_visits'] = num_visits+1
    request.session['last_visit'] = datetime.datetime.now().strftime("%d %b %Y %H:%M")

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'num_books':num_books,
                 'num_instances':num_instances,
                 'num_instances_available':num_instances_available,
                 'num_authors':num_authors,
                 'num_genre':num_genre,
                 'visit':visit},
    )


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book


class AuthorsListView(generic.ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class AllLoanedBooksListView(PermissionRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
