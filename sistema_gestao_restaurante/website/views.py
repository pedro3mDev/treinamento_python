from django.shortcuts import render
from management.models import ProductModel, CategoryModel

# Create your views here.

def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    
    context = {
        'products': ProductModel.objects.all(),
        'categories': CategoryModel.objects.all(),
    }
    # context = {"latest_question_list": 'latest_question_list'}
    return render(request, "website/index.html", context)