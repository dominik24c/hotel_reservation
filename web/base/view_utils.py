from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response


def create_view_handlers(view_obj, request: Request, message: dict, *args, **kwargs) -> Response:
    serializer = view_obj.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    view_obj.perform_create(serializer)
    headers = view_obj.get_success_headers(serializer.data)
    return Response(message, status=status.HTTP_201_CREATED, headers=headers)
