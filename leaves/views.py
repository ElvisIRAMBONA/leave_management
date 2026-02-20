from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import LeaveRequest
from .serializers import LeaveRequestSerializer

class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN' or user.role == 'MANAGER':
            return LeaveRequest.objects.all()
        return LeaveRequest.objects.filter(employee=user)
    
    def perform_create(self, serializer):
        serializer.save(employee=self.request.user)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        leave_request = self.get_object()
        if request.user.role not in ['MANAGER', 'ADMIN']:
            return Response({'error': 'Permission refusée'}, status=status.HTTP_403_FORBIDDEN)
        leave_request.statut = 'APPROVED'
        leave_request.save()
        return Response({'status': 'Demande approuvée'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        leave_request = self.get_object()
        if request.user.role not in ['MANAGER', 'ADMIN']:
            return Response({'error': 'Permission refusée'}, status=status.HTTP_403_FORBIDDEN)
        leave_request.statut = 'REJECTED'
        leave_request.save()
        return Response({'status': 'Demande rejetée'})