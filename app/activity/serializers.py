from rest_framework import serializers

from core.models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer an Activity"""

    class Meta:
        model = Activity
        fields = (
            'id',
            'distance',
            'time_hours',
            'time_minutes',
            'time_seconds',
            'elevation',
            'sport',
            'date',
            'start_time',
            'title',
            'description',
            'type',
            'effort',
        )
        read_only_fields = ('id',)


class ActivityImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to activities"""

    class Meta:
        model = Activity
        fields = ('id', 'image')
        read_only_fields = ('id',)
