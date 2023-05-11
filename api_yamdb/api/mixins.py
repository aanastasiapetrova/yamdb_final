from rest_framework import viewsets
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)


class CreateMixin(CreateModelMixin, viewsets.GenericViewSet):
    pass


class ListCreateDestroyMixin(ListModelMixin,
                             CreateModelMixin,
                             DestroyModelMixin,
                             viewsets.GenericViewSet):
    pass


class ListCreateMixin(ListModelMixin,
                      CreateModelMixin,
                      viewsets.GenericViewSet):
    pass
