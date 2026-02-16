from django.db import models
from users.models import User

class LeaveRequest(models.Model):
    TYPE_CHOICES = (
        ('ANNUAL', 'Annuel'),
        ('SICK', 'Maladie'),
        ('MATERNITY', 'Maternité'),
        ('UNPAID', 'Sans solde'),
    )

    STATUS_CHOICES = (
        ('PENDING', 'En attente'),
        ('APPROVED', 'Accepté'),
        ('REJECTED', 'Rejeté'),
    )

    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    type_conge = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_debut = models.DateField()
    date_fin = models.DateField()
    raison = models.TextField()
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
