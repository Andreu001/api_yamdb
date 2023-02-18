from rest_framework import mixins, viewsets


class ModelMixinSet(mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    
    pass
