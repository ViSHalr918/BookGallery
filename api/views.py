from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Book,Review
from rest_framework import viewsets
from api.serializers import BookSerializers,ReviewSerializers
from rest_framework.decorators import action
from rest_framework import authentication,permissions
from rest_framework import generics
# Create your views here.


class BooklistCreateView(APIView):
    def get(self,request,*args,**kwargs):
        # data={"message":"return all books"}

        qs = Book.objects.all()  #a query set is available
        serializer_instance = BookSerializers(qs,many=True)  #serialization

        return Response(data=serializer_instance.data)
    

    def post(self,request,*args,**kwargs):
        serializer_instance=BookSerializers(data=request.data)   #deserialization
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(serializer_instance.errors)
        
   
class BookRetrieveUpdateDeleteView(APIView):
    def get(self,request,*args,**kwargs):
        id= kwargs.get("pk")
        qs = Book.objects.get(id=id)
        serializer_instance = BookSerializers(qs)
        return Response(data=serializer_instance.data)

    
    def put(self,request,*args,**kwargs): #put -> update
        id = kwargs.get("pk")
        book_obj = Book.objects.get(id=id)
        serializer_instance = BookSerializers(data=request.data,instance = book_obj)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)


        return Response(data)

    def delete(self,request,*args,**kwargs):
        id= kwargs.get('pk')
        Book.objects.get(id=id).delete()
        data = {"messages":"book delete view"}
        return Response(data)
    

class BookViewsetView(viewsets.ViewSet):

    authentication_classes = [authentication.BaseAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    # create,list,update,retrive,destroy
    def list(self,request,*args,**kwargs):
        qs = Book.objects.all()
        serializers_instance = BookSerializers(qs,many=True)
        return Response(data=serializers_instance.data)
    
    def create(self,request,*args,**kwargs):
        serializer_instance = BookSerializers(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(serializer_instance.errors)
        
    def retrive(self,request,*args,**kwargs):
        id = kwargs.get('pk')
        qs = Book.objects.get(id=id)
        serializer_instance = BookSerializers(qs)
        return Response(data=serializer_instance.data)
    
    def update(self,request,*args,**kwargs):
        id = kwargs.get('pk')
        book_obj = Book.objects.get(id=id)
        serializer_instance = BookSerializers(data=request.data,instance=book_obj)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(serializer_instance.errors)
        
    def destroy(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        Book.objects.get(id=id).delete()
        data = {"message":"deleted"}
        return Response(data)
    
    # custom method
    @action(methods=["GET"],detail=False)
    def genere_list(self,request,*args,**kwargs):
        
        genres = Book.objects.all().values_list("genre",flat=True).distinct()
        return Response(data=genres)
    
    @action(methods=["GET"],detail=False)
    def author_list(self,request,*args,**kwargs):
        
        author = Book.objects.all().values_list("author",flat=True).distinct()
        return Response(data=author)
    @action(methods=["POST"],detail=True)
    def add_review(self,request,*args,**kwargs):
        book_obj = kwargs.get("pk")
        book_object = Book.objects.get(id=book_obj)
        serializer_instance = ReviewSerializers(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save(book_obj=book_object)
            return Response(data=serializer_instance.data)
        else:
            return Response(serializer_instance.errors)
        
class ReviewUpdateDestroyView(viewsets.ViewSet):
    def destroy(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        Review.objects.get(id=id).delete()
        data = {"message":"Review deleted successfully"}
        return Response(data)
    
    def update(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        review_obj = Review.objects.get(id=id)
        serializer_instance = ReviewSerializers(data=request.data,instance=review_obj)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(serializer_instance.errors)
        
    def retrive(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        qs = Review.objects.get(id=id)
        serializer_instance = ReviewSerializers(qs)
        return Response(data=serializer_instance.data)

class BookListView(generics.ListCreateAPIView):
    serializer_class = BookSerializers
    queryset = Book.objects.all()

class Book2RetriveUpdateDeleteview(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializers
    queryset = Book.objects.all()