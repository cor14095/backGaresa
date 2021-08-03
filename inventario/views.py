from django.shortcuts import render
from .models import Product
from .serializers import ProductSerializer

# Create your views here.
class PostViewSet(ListCreateAPIView):
    queryset = Product.objects.all()
    #pagination_class = CustomPagination
    #permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Post.objects.all()
        created_by = self.request.query_params.get('created_by', None)
        if created_by not in [None, '']:
            queryset = queryset.filter(created_by_id=created_by)
        return queryset

    def post(self, request, format=None):
        serializer = PostSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(created_by = request.user)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)