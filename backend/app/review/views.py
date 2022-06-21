from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Review, Photo, Reply
from .serializers import ReviewSerializer, PhotoSerializer, ReplySerializer


# Create your views here.
class ReviewListCreateView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class PhotoListCreateView(ListCreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class PhotoDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class ReplyListCreateView(ListCreateAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer


class ReplyDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer