from rest_framework import serializers


class AssistantQuerySerializer(serializers.Serializer):
    question = serializers.CharField(max_length=1000)
    context_type = serializers.ChoiceField(
        choices=["general", "nko", "event", "material", "news"],
        required=False,
        default="general",
    )
    context_id = serializers.CharField(max_length=64, required=False, allow_blank=True)

