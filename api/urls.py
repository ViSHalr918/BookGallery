from django.urls import path,include

from api import views

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register("v1/books",views.BookViewsetView,basename="books")
router.register("v1/reviews",views.ReviewUpdateDestroyView,basename="reviews")

urlpatterns = [
    

    path("books/",views.BooklistCreateView.as_view()),

    path("books/<int:pk>/",views.BookRetrieveUpdateDeleteView.as_view()),

    path("v2/books/",views.BookListView.as_view()),

    path("v2/books/<int:pk>/",views.Book2RetriveUpdateDeleteview.as_view())


]+router.urls