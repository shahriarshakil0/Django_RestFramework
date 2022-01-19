from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import authentication
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import AritcleSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics,mixins
from rest_framework.authentication import SessionAuthentication,BaseAuthentication
from rest_framework.permissions import IsAuthenticated

#********************************************************************************************************************#
# Functiom Based Http Response
# @csrf_exempt
# def article_list(request):
#     if request.method == 'GET':
#         articles = Article.objects.all()
#         serializer = AritcleSerializer(articles, many = True)
#         return JsonResponse(serializer.data, safe = False)

#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = AritcleSerializer(data=data)

#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)

#         else:
#             return JsonResponse(serializer.errors, status=400)

# @csrf_exempt
# def article_detail(request, pk):
#     try:
#         article = Article.objects.get(pk=pk)
#     except Article.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = AritcleSerializer(article)
#         return JsonResponse(serializer.data)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = AritcleSerializer(article,data=data)

#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)

#         else:
#             return JsonResponse(serializer.errors, status=400)

#     elif request.method == 'DELETE':
#         article.delete()
#         return HttpResponse(status=204)

#********************************************************************************************************************#
# Functiom Based RestFramework Response
# @api_view(['GET','POST'])
# def article_list(request):
#     if request.method == 'GET':
#         articles = Article.objects.all()
#         serializer = AritcleSerializer(articles, many = True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = AritcleSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET','PUT','DELETE'])
# def article_detail(request, pk):
#     try:
#         article = Article.objects.get(pk=pk)
#     except Article.DoesNotExist:
#         return HttpResponse(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = AritcleSerializer(article)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
       
#         serializer = AritcleSerializer(article,data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)

#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         article.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#********************************************************************************************************************#
#class based API View

class ArticleAPIView(APIView):

    authentication_classes = [SessionAuthentication, BaseAuthentication]
    permission_classes = [IsAuthenticated ]

    def get(self,request):
        articles = Article.objects.all()
        serializer = AritcleSerializer(articles, many = True)
        return Response(serializer.data)

    def post(self,request):
        serializer = AritcleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetails(APIView):

    authentication_classes = [SessionAuthentication, BaseAuthentication]
    permission_classes = [IsAuthenticated ]

    def get_object(self,id):
        try:
            return Article.objects.get(id=id)
        except Article.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self,request,id):
        article = self.get_object(id)
        serializer = AritcleSerializer(article)
        return Response(serializer.data)

    def put(self,request,id):
        article = self.get_object(id)
        serializer = AritcleSerializer(article,data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id):
        article = self.get_object(id)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#********************************************************************************************************************#
#class based Generic,mixins view

class GenericAPIView(generics.GenericAPIView,mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
 mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    serializer_class = AritcleSerializer
    queryset = Article.objects.all()
    lookup_field = 'id'

    authentication_classes = [SessionAuthentication, BaseAuthentication]
    permission_classes = [IsAuthenticated ]

    def get(self, request,id):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)
    



