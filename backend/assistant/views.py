from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import AssistantQuerySerializer
from .services import RagClient, RagServiceError


class QueryAssistantView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = AssistantQuerySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data

        client = RagClient()
        try:
            answer = client.query(
                question=payload["question"],
                user=request.user,
                context_type=payload.get("context_type"),
                context_id=payload.get("context_id"),
            )
        except RagServiceError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_502_BAD_GATEWAY)

        return Response(answer, status=status.HTTP_200_OK)
