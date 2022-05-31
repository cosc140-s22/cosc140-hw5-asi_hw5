from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch
from .models import Product
from .forms import ProductFilterForm


def index(request):
    Product.objects.prefetch_related(Prefetch('productimage_set'))

    if (request.GET.get('sort') == 'age'):
        products = Product.objects.all().order_by('minimum_age_appropriate')
    elif (request.GET.get('sort') == 'price'):
        products = Product.objects.all().order_by('price')
    else:
        products = Product.objects.all().order_by('name')

    form = ProductFilterForm(request.GET)

    name_search = request.GET.get('name_search')
    if name_search:
        products = products.filter(name__icontains=name_search)

    min_price = request.GET.get('min_price')
    if min_price:
        products = products.filter(price__gte=min_price)

    max_price = request.GET.get('max_price')
    if max_price:
        products = products.filter(price__lte=max_price)

    context = {'products': products, 'form': form}
    return render(request, 'products/index.html', context)


def show(request, product_id):
    p = get_object_or_404(Product, pk=product_id)
    images = p.productimage_set.all()
    context = {'product': p, 'images': images}
    return render(request, 'products/show.html', context)
