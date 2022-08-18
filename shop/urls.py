from django.urls import path
from . import views
app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list' ),
    path('login/', views.login_page, name='login_view'),
    path('logout/', views.logout_page, name='logout_view'),
    path('watchlist/', views.watchlist_page, name='watchlist_page'),
    path('watchlist/<int:id>/', views.watchlist, name='watchlist'),
    path('likelist/', views.likelist_page, name='likelist_page'),
    path('likelist/<int:id>/', views.likelist, name='likelist'),
    path('add_rating/<int:p_id>/', views.add_rating, name='addrating'),
    path('<slug:category_slug>', views.product_list, name='product_list_by_category' ),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail' ),
    path('<int:id>/<slug:slug>/comment/', views.comment, name='comment'),

]