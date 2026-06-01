from django.shortcuts import render, redirect
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.conf import settings
from django.contrib import messages
from management.models import ProductModel, CategoryModel
from .models import InvoiceModel, InvoiceLineModel
from datetime import date, datetime

# Create your views here.

@login_required
def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    
    context = {
        'products': ProductModel.objects.all(),
        'categories': CategoryModel.objects.all(),
    }
    # context = {"latest_question_list": 'latest_question_list'}
    return render(request, "point_of_sale/index.html", context)

@login_required
def create_invoice(request):
    try:
        if request.method == 'POST':
            # data = request.POST

            # print(data)
            # client = request.POST.getlist('select2_customer')[0]
            produts = request.POST.getlist('product')
            quantity = request.POST.getlist('quantity')
            prices = request.POST.getlist('price')
            taxs = request.POST.getlist('tax')
            new_invoice = InvoiceModel.objects.create(
                created_at=datetime.now(),
                number="FR "+str(date.today().year)+"/"+str(InvoiceModel.objects.all().count()+1),
                total=0,
                total_tax=0,
                total_without_tax=0,
                saved_by = request.user
            )
            for product_id, quantity, price, tax in zip(produts, quantity, prices, taxs):
                InvoiceLineModel.objects.create(
                    invoice=new_invoice,
                    product_id=product_id,
                    quantity=int(quantity),
                    unit_price=float(price),
                )
                new_invoice.total_without_tax += float(price) * int(quantity)
                new_invoice.total_tax += (float(price) * int(quantity)) * (int(tax)/float(100))
                new_invoice.total += round((float(price) * int(quantity)) * ((int(tax)/float(100))+1))

            # f_.store = store
            # f_.paid = True
            # f_.customer_id = int(client) if client else None
            # document.save_signature()
            # document.enc_signature()
            new_invoice.save()
            messages.success(request, 'Factura criado com sucesso!')
            return HttpResponseRedirect(reverse('point_of_sale:print_invoice', kwargs={'fatura_id':new_invoice.pk}))

    except Exception as erro:
        print(erro)
        messages.error(
            request,
            str(erro)
        )
        return HttpResponseRedirect(reverse('point_of_sale:index'))

    # if request.method == 'POST':
    #     print(request.POST.getlist('quantity'))
    #     print(request.POST.getlist('product'))
    #     print(request.POST.getlist('price'))
    #     print(request.POST)
    #     data = zip(
    #         request.POST.getlist('quantity'),
    #         request.POST.getlist('product'),
    #         request.POST.getlist('price'),
    #     )
    #     for quantity, product, price in data:
    #         print(quantity, product, price)
    #     # form = FaturaForm(request.POST)
    #     # if form.is_valid():
    #     #     fatura = form.save()
    #         # Redirecionar para a página de impressão com o ID da fatura
    #     return HttpResponseRedirect(reverse('point_of_sale:print_invoice', kwargs={'fatura_id':1}))
    #     # return redirect('print_invoice', fatura_id='fatura.id')
            

@login_required
def print_invoice(request, fatura_id):
    # fatura = get_object_or_404(Fatura, id=fatura_id)
    invoice=InvoiceModel.objects.get(pk=fatura_id)
    lines=InvoiceLineModel.objects.filter(invoice=invoice)
    context={
        'invoice':invoice,
        'lines':lines,
    }
    print(context)
    return render(request, 'point_of_sale/print_invoice.html', context)