from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from . import serializer
from .serializer import PersonFilterSet
from ..models import Person

from djgentelella.models import Notification


class PersonViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    serializer_class = serializer.PersonDataTableSerializer
    queryset = Person.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ['name', 'num_children', ]  # for the global search
    filterset_class = PersonFilterSet
    ordering_fields = ['name', 'num_children', 'born_date', 'last_time']
    ordering = ('-num_children',)  # default order

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data = self.paginate_queryset(queryset)
        response = {'data': data, 'recordsTotal': Person.objects.count(),
                    'recordsFiltered': queryset.count(),
                    'draw': self.request.GET.get('draw', 1)}
        return Response(self.get_serializer(response).data)


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = serializer.NotificationDataTableSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ['user', 'state', ]
    ordering_fields = ['message_type', 'creation_date', 'description', 'link', 'state']
    ordering = ('-creation_date',)

    def list(self, request, *args, **kwargs):
        queryset = super().get_queryset().filter(user=self.request.user)
        data = self.paginate_queryset(queryset)
        response = {'data': data, 'recordsTotal': Notification.objects.count(),
                    'recordsFiltered': queryset.count(),
                    'draw': self.request.GET.get('draw', 1)}

        return Response(self.get_serializer(response).data)
