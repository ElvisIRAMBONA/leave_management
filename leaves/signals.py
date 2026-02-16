from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LeaveRequest
from notifications.models import Notification
from users.models import User

@receiver(post_save, sender=LeaveRequest)
def leave_request_notification(sender, instance, created, **kwargs):

    # 1️⃣ Nouvelle demande → notifier les chefs
    if created:
        managers = User.objects.filter(role='MANAGER')
        for manager in managers:
            Notification.objects.create(
                user=manager,
                message=f"Nouvelle demande de congé de {instance.employee.username}"
            )

    # 2️⃣ Statut modifié → notifier l’employé
    else:
        if instance.statut in ['APPROVED', 'REJECTED']:
            Notification.objects.create(
                user=instance.employee,
                message=f"Votre demande de congé a été {instance.statut.lower()}"
            )
