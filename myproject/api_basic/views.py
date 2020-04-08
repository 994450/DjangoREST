from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET','POST'])
def article_list(request):
    if request.method =='GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles,many=True)
        return  Response(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(data, data=data)
        if serializer.isvalid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def article_detail(request,pk):
    try:
        article=Article.object.get(pk=pk)
    except Article.DoseNotExist:
        return HttpResponse(status=404)
    if request.method =='GET':
        serializer = ArticleSerializer(article)
        return  JsonResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(data, data=data)
        if serializer.isvalid():
            serializer.save()
            return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)


    elif request.method == 'DELETE':
        article.delete()
        return HttpResponse(status=204)