from django.shortcuts import render
from .models import Results,Students,Downloads,Update
from django.shortcuts import render

# Create your views here.
data = []
def post_list(request):
    update = Update.objects.latest('time')
    posts = Downloads.objects.all()
    return render(request,
                 'result/post/list.xhtml',
                 {'posts': posts,
                  'update': update})

# ...
def post_detail(request, id):
    # Get the symbol_num values from the Results table
    symbol_nums = Results.objects.filter(key=id).values_list('symbol_num', flat=True)

    titledata = Downloads.objects.filter(key=id).values()

    # Get all the matching rows from the Students table
    students = Students.objects.filter(symbol_num__in=symbol_nums).values()


    # Pass the students queryset to the template context
    return render(request, 'result/post/detail.xhtml', {'students': students,
                                                        'titledata': titledata})