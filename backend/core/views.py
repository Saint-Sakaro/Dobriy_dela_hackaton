from datetime import datetime

from django.conf import settings
from django.http import JsonResponse


def health_check(request):
    return JsonResponse(
        {
            "status": "ok",
            "time": datetime.utcnow().isoformat(),
            "debug": settings.DEBUG,
        }
    )

