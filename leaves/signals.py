from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import LeaveRequest
from notifications.models import Notification
from users.models import User


def send_leave_email(subject, message, recipient):
    if not recipient.email:
        return

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [recipient.email],
        fail_silently=True,
    )


@receiver(post_save, sender=LeaveRequest)
def leave_request_notification(sender, instance, created, **kwargs):
    if created:
        managers = User.objects.filter(role='MANAGER')
        subject = f"Nouvelle demande de congé #{instance.id}"
        message = (
            f"{instance.employee.get_full_name() or instance.employee.username} a demandé un congé "
            f"du {instance.date_debut} au {instance.date_fin}.\n"
            f"Type : {instance.type_conge}.\n"
            f"Raison : {instance.raison}"
        )

        for manager in managers:
            Notification.objects.create(
                user=manager,
                message=f"Nouvelle demande de congé de {instance.employee.username}"
            )
            send_leave_email(subject, message, manager)

    else:
        if instance.statut in ['APPROVED', 'REJECTED']:
            status_text = 'approuvée' if instance.statut == 'APPROVED' else 'rejetée'
            Notification.objects.create(
                user=instance.employee,
                message=f"Votre demande de congé a été {status_text}."
            )

            subject = f"Votre demande de congé #{instance.id} a été {status_text}"
            message = (
                f"Votre demande de congé du {instance.date_debut} au {instance.date_fin} "
                f"a été {status_text}.\n"
                f"Type : {instance.type_conge}."
            )
            if instance.statut == 'REJECTED' and instance.rejection_reason:
                message += f"\nMotif du refus : {instance.rejection_reason}"

            send_leave_email(subject, message, instance.employee)
