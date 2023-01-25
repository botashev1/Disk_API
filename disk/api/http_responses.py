from django.http import JsonResponse
from rest_framework import status


def get_404():
    return JsonResponse({'code': status.HTTP_404_NOT_FOUND, 'message': 'Item not found'},
                        status=status.HTTP_404_NOT_FOUND)


def get_400():
    return JsonResponse({'code': status.HTTP_400_BAD_REQUEST, 'message': 'Validation Failed'},
                        status=status.HTTP_400_BAD_REQUEST)


def get_200(data):
    return JsonResponse(data, status=status.HTTP_200_OK)