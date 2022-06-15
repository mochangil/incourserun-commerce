from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny

from app.example.models import Example
from app.example.paginations import ExamplePagination
from app.example.serializers import ExampleSerializer


class ExampleView(ListCreateAPIView):
    queryset = Example.objects.filter(is_active=True)
    # pagination_class = ExamplePagination
    serializer_class = ExampleSerializer
    permission_classes = [AllowAny]
