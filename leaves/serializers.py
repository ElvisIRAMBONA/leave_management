from rest_framework import serializers
from django.utils.timezone import localdate
from .models import LeaveRequest
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']

class LeaveRequestSerializer(serializers.ModelSerializer):
    employee_details = UserSerializer(source='employee', read_only=True)
    
    class Meta:
        model = LeaveRequest
        fields = ['id', 'employee', 'employee_details', 'type_conge', 'date_debut', 
                  'date_fin', 'raison', 'statut', 'rejection_reason', 'created_at']
        read_only_fields = ['created_at']
    
    def validate(self, data):
        if data['date_debut'] > data['date_fin']:
            raise serializers.ValidationError("La date de début doit être avant la date de fin")

        today = localdate()
        if data['date_debut'] < today:
            raise serializers.ValidationError("La date de début du congé doit être aujourd'hui ou une date future")

        employee = self.context['request'].user if 'request' in self.context else None
        if employee:
            overlapping_leaves = LeaveRequest.objects.filter(
                employee=employee,
                statut__in=['PENDING', 'APPROVED'],
            )
            if self.instance:
                overlapping_leaves = overlapping_leaves.exclude(pk=self.instance.pk)

            if overlapping_leaves.filter(date_debut__lte=data['date_fin'], date_fin__gte=data['date_debut']).exists():
                raise serializers.ValidationError(
                    "Vous avez déjà un congé en cours ou en attente qui se chevauche avec ces dates"
                )

        return data
