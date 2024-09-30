from rest_framework import serializers
from api.models import Book,Review


class ReviewSerializers(serializers.ModelSerializer):
    book_obj = serializers.StringRelatedField()   #to represent the name 
    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ["id","book_obj"]

class BookSerializers(serializers.ModelSerializer):
    # reviews = ReviewSerializers(read_only=True,many=True)
    reviews = serializers.SerializerMethodField()
    # review_count = serializers.CharField
    review_count = serializers.SerializerMethodField(read_only=True)
    # avg_rating = serializers.FloatField
    avg_rating = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Book
        # fields = "__all__"    #for all fields in model
        
        fields = ["id","title","author","language","price","genre","reviews","review_count","avg_rating"]

    def get_review_count(self,obj):

        return Review.objects.filter(book_obj=obj).count()
    
    def get_avg_rating(self,obj):
        reviews = Review.objects.filter(book_obj = obj)
        avg = 0
        if reviews:
            avg = sum([r.rating for r in reviews])/self.get_review_count(obj)
        return avg

    def get_reviews(self,obj):
        qs = Review.objects.filter(book_obj = obj)

        serializer_instance = ReviewSerializers(qs,many=True)
        return serializer_instance.data
        



