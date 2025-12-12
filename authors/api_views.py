from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Author
from .serializers import AuthorSerializer
from django.shortcuts import get_object_or_404

class AuthorListAPI(APIView):
    def get(self, request):
        qs = Author.objects.all()
        serializer = AuthorSerializer(qs, many=True, context={"request": request})
        return Response(serializer.data)

class AuthorDetailAPI(APIView):
    def get(self, request, pk):
        obj = get_object_or_404(Author, pk=pk)
        serializer = AuthorSerializer(obj, context={"request": request})
        return Response(serializer.data)
