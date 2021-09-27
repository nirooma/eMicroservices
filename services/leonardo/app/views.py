from django.shortcuts import render
from django.http import JsonResponse
import datetime
from django.conf import settings
import platform


def health_check(request) -> JsonResponse:
    return JsonResponse({
        "Status": 200,
        "Timestamp": datetime.datetime.now().ctime(),
        "DebugMode": settings.DEBUG,
        "OperatingSystem": platform.uname(),
        # "DockerMode": settings.DOCKER_MODE,
        # "AppMode": settings.APP_ENVIRONMENT,
    })
