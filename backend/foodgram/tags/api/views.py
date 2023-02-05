from rest_framework import filters, permissions, viewsets

from tags.models import Tag
from .serializers import TagsSerializer


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (permissions.AllowAny, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    #lookup_field = 'slug' #with it cannot reach it by id only by slug
