from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.reverse import reverse

from todos import auth
from todos.models import Todo
from todos.serializers import TodoSerializer


# There is views.

@api_view(['GET'])
def index(request):
    return Response({
        'todos': reverse('todo_list', request=request)
    })


@api_view(['GET', 'POST'])
def todos_list(request):
    """get all todos."""

    owner = auth.parser(request)

    if request.method == 'GET':
        todos = Todo.objects.all().filter(owner=owner).order_by('-id')
        serializer = TodoSerializer(todos, many=True)
        res = {'count': len(todos), 'results': serializer.data}
        return Response(res)

    elif request.method == 'POST':
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=owner)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def todo_page_list(request, sort):
    """get todos by pagination"""

    todos = []
    owner = auth.parser(request)

    if request.method == 'GET':
        # sort by priority
        if sort == 'p':
            todos = Todo.objects.all().filter(owner=owner, finished=False).order_by('priority', '-id')
        # sort by expired
        elif sort == 'e':
            todos = Todo.objects.all().filter(owner=owner, finished=False).order_by('-expired', '-id')
        # default sort
        elif sort == 'd':
            todos = Todo.objects.all().filter(owner=owner, finished=False).order_by('-id')

        # 分页
        pg = PageNumberPagination()
        pg_todo = pg.paginate_queryset(queryset=todos, request=request)
        serializer = TodoSerializer(pg_todo, many=True)
        return pg.get_paginated_response(serializer.data)


@api_view(['GET'])
def todo_finished_list(request):
    """
    get all finished todos.
    """

    owner = auth.parser(request)

    if request.method == 'GET':
        todos = Todo.objects.all().filter(owner=owner, finished=True).order_by('-id')
        serializer = TodoSerializer(todos, many=True)
        res = {'count': len(todos), 'results': serializer.data}
        return Response(res)


@api_view(['GET', 'PUT', 'DELETE'])
def todo_detail(request, id):
    """single todos: get or put or delete."""

    owner = auth.parser(request)
    try:
        todo = Todo.objects.get(id=id)
    except Todo.DoesNotExist:
        return Response({'message': 'This todo not exist'}, status=status.HTTP_404_NOT_FOUND)

    # todos not belong to owner
    if todo.owner != owner:
        return Response({'message': 'This todo not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def register(request):
    """user register"""
    pass
