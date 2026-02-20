from rest_framework import serializers
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
        return data
