from rest_framework import status

from .models import Application

from .serializers import ApplicationSerializer

from rest_framework import permissions
from application.permissions import IsApplicationPosterOrAdmin

from rest_framework import generics
from rest_framework.response import Response

from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from recruitmentapi.utils.custom_exceptions import BadRequest


class ApplicationView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        queryset = Application.objects.all()
        if not self.request.user.is_admin:
            user_id = self.request.user.id
            if user_id is not None:
                queryset = queryset.filter(posted_by__id=user_id)
        return queryset

    def list(self, request, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Application(s) successfully retrieved",
                    "result": serializer.data}
        return Response(response)

    def perform_create(self, serializer):
        if self.request.user.is_admin:
            raise BadRequest({'message': "Admins can't post an application."},
                             code=status.HTTP_400_BAD_REQUEST)

        try:
            if self.request.user.application:
                raise BadRequest({'message': "You have already posted an application."
                                             " Delete that to post a new application"},
                                 code=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            pass

        serializer.save(posted_by=self.request.user, posted_at=timezone.now())

    def create(self, request, *args, **kwargs):
        response_obj = super(ApplicationView, self).create(request, args, kwargs)
        response = {"status_code": status.HTTP_201_CREATED,
                    "message": "Application successfully posted",
                    "result": response_obj.data}
        return Response(response)


class ApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated & IsApplicationPosterOrAdmin]

    queryset = Application.objects.all()
    lookup_url_kwarg = "application_id"
    serializer_class = ApplicationSerializer

    def retrieve(self, request, *args, **kwargs):
        super(ApplicationDetailView, self).retrieve(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        data = serializer.data
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Application successfully retrieved",
                    "result": data}
        return Response(response)

    def perform_update(self, serializer):
        if self.request.user.is_admin:
            raise BadRequest({'message': "Admins can't update an application."},
                             code=status.HTTP_400_BAD_REQUEST)

        serializer.save(updated_at=timezone.now())

    def patch(self, request, *args, **kwargs):
        super(ApplicationDetailView, self).patch(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Application successfully updated",
                    "result": data}
        return Response(response)

    def delete(self, request, *args, **kwargs):
        super(ApplicationDetailView, self).delete(request, args, kwargs)
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Application successfully deleted"}
        return Response(response)
