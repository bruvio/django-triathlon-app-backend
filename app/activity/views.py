from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from activity import serializers
# from activity.serializers import ActivitySerializer
from core.models import Activity


class BaseActivityViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):  # noqa: E501
    """Base viewset for userowned activity attributes, referenced by other classes"""  # noqa: E501
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)

        return queryset.filter(user=self.request.user).order_by('-name').distinct()  # noqa: E501


class ActivityViewSet(viewsets.ModelViewSet):
    """Manage Activities in the database"""
    serializer_class = serializers.ActivitySerializer
    queryset = Activity.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _params_to_ints(self, qs):
        """Convert a list of string ids to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieves the activities for the authenticated user"""
        queryset = self.queryset

        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'upload_image':
            return serializers.ActivityImageSerializer  # need to implement still  # noqa: E501

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new activity"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a activity"""
        activity = self.get_object()
        serializer = self.get_serializer(
            activity,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
