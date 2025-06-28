from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("all/", views.all, name="all"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("newlisting/", views.newlisting, name="newlisting"),
    path("<int:product_id>/", views.product, name="product"),
    path("<int:product_id>/bid/", views.bid, name="bid"),
    path("<int:product_id>/comment/", views.comment, name="comment"),
    path("<int:product_id>/sell/", views.sell, name="sell"),

]

