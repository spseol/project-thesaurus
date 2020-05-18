from rest_framework.serializers import ModelSerializer

from apps.audit.models import AuditLog


class AuditLogSerializer(ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'
