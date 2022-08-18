from django.utils import timezone

from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

from .forms import CommentForm, LoginForm
from .models import Category, Product, Chat, Watchlist, Likelist, Rating
from cart.forms import CartAddProductForm

# Create your views here.
from .serializers import ProductSerializer
from .validation import validate_login
from itertools import chain


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()

    products = Product.objects.filter(available=True)
    for t in products:
        ids = Likelist.objects.filter(product_id=t.id)

    sproducts = ProductSerializer(products, many=True).data
    # for t in sproducts:
    #     likes = t.likes

    # prodlikes = Likelist.objects.filter(product_id=id)
    # prodlikes = Product.likes.all().count()
    # prodwatches = Product.watches.all().count()


    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        sproducts = ProductSerializer(products, many=True).data
    return render(request, 'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                    'products': products,
                   'sproducts': sproducts
                   })


def add_rating(request, id):
    user = request.user
    product = get_object_or_404(Product, id=id)
    value = request.POST.get("value")

    if not value:
        raise ValueError("value is required")

    if Rating.objects.filter(user=user, product=product).exists():
        rating = Rating.objects.get(user=user, product=product)
        rating.value = value
        rating.save()
    else:
        Rating.objects.create(user=user, product=product, value=value)

    return product_list(request, category_slug=None)


def product_detail(request, id, slug):

    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request, 'shop/product/detail.html', {'product': product})



def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()

    stats = []

    chat = Chat.objects.filter(product_id=id).order_by('time_sent')
    stats.append(chat)


    return render(request, 'shop/product/detail.html',
                    {'product': product,
                     'stats': stats,
                    'cart_product_form': cart_product_form})



def comment(request, id, slug):
    """
    Comment on an auction.

    Returns
    -------
    Function : bid_page(request, auction_id)
        Return the
    Function : index(request)
        If the user is not logged in.
    """
    try:
        if request.session['username']:
            user = User.objects.filter(username=request.session['username'])
            product = Product.objects.filter(id=id)
            if request.method == 'POST':
                form = CommentForm(request.POST)
                if form.is_valid():
                    msg = Chat()
                    msg.user_id = user[0]
                    msg.product_id = product[0]
                    msg.message = form.cleaned_data['comment']
                    msg.time_sent = timezone.now()
                    msg.save()
                    return product_detail(request, id, slug)

            return product_list(request, category_slug=None)
    except KeyError:
        return product_list(request, category_slug=None)

    return product_list(request, category_slug=None)



def list_users(request):

    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    # if category_slug:
    #     category = get_object_or_404(Category, slug=category_slug)
    #     products = products.filter(category=category)

    return render(request, 'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def watchlist(request, id):
    """
    Adds the auction to the user's watchlist.

    Returns
    -------
    Function : index(request)
    """
    try:
        if request.session['username']:
            user = User.objects.filter(username=request.session['username'])
            product = Product.objects.filter(id=id)

            w = Watchlist.objects.filter(product_id=id)
            if not w:
                watchlist_item = Watchlist()
                watchlist_item.product_id = product[0]
                watchlist_item.user_id = user[0]
                watchlist_item.save()
            else:
                w.delete()

            return watchlist_page(request)
    except KeyError:
        return product_list(request, category_slug=None)

    return product_list(request, category_slug=None)


def watchlist_page(request):
    """
    Disguises the index page to look
    like a page with the auctions the
    user is watching.

    Returns
    -------
    HTTPResponse
        The index page with auctions the user is watching.
    Function : index(request)
        If the user is not logged in.
    """
    try:
        if request.session['username']:
            user = User.objects.filter(username=request.session['username'])

            # product = Product.objects.none()
            # product = Watchlist.objects.filter(user_id=user[0])

            w = Watchlist.objects.filter(user_id=user[0])

            product = Product.objects.none()
            for item in w:
                a = Product.objects.filter(id=item.product_id.id)
                product = list(chain(product, a))

            return render(request, 'shop/product/watchlist.html', {
                'products': product,
                'user': user[0],
                'watchlist': product
            })
    except KeyError:
        return product_list(request, category_slug=None)


def likelist(request, id):
    """
    Adds the auction to the user's watchlist.

    Returns
    -------
    Function : index(request)
    """
    try:
        if request.session['username']:
            user = User.objects.filter(username=request.session['username'])
            product = Product.objects.filter(id=id)

            w = Likelist.objects.filter(product_id=id)
            if not w:
                watchlist_item = Likelist()
                watchlist_item.product_id = product[0]
                watchlist_item.user_id = user[0]
                watchlist_item.save()
            else:
                w.delete()

            return likelist_page(request)
    except KeyError:
        return product_list(request, category_slug=None)

    return product_list(request, category_slug=None)


def likelist_page(request):
    """
    Disguises the index page to look
    like a page with the auctions the
    user is watching.

    Returns
    -------
    HTTPResponse
        The index page with auctions the user is watching.
    Function : index(request)
        If the user is not logged in.
    """
    try:
        if request.session['username']:
            user = User.objects.filter(username=request.session['username'])

            # product = Product.objects.none()
            # product = Watchlist.objects.filter(user_id=user[0])

            w = Likelist.objects.filter(user_id=user[0])

            product = Product.objects.none()
            for item in w:
                a = Product.objects.filter(id=item.product_id.id)
                product = list(chain(product, a))

            return render(request, 'shop/product/likelist.html', {
                'products': product,
                'user': user[0],
                'likelist': product
            })
    except KeyError:
        return product_list(request, category_slug=None)

def login_page(request):
    """
    Login POST request.

    Returns
    -------
    Function
        Index page request
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            is_valid = validate_login(
                form.cleaned_data['username'],
                form.cleaned_data['password']
            )
            if is_valid:
                # Creates a session with 'form.username' as key.
                request.session['username'] = form.cleaned_data['username']
    # return index(request)
    return list_users(request)



def logout_page(request):
    """
    Deletes the session.

    Returns
    -------
    Function
        Index page request
    """
    try:
        del request.session['username']
    except:
        pass  # if there is no session pass
    # return index(request)
    return list_users(request)