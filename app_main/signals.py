import requests
from datetime import datetime
from random import randint

from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from app_main.models import Point, User


@receiver(signal=post_save, sender=Point)
def send_message_on_point_create(sender, instance, created, *args, **kwargs):
    if created:
        user: User = instance.user
        amount: int = instance.amount
        description: str = instance.description

        if amount > 0:
            text = f"🟢 Sizga <b>{amount}</b> ball taqdim etildi\n\n"
        else:
            text = f"🔴 Sizdan <b>{amount}</b> ball olib tashlandi\n\n"

        text += f"Sabab: <i>{description}</i>\n"

        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": user.telegram_id,
            "text": text,
            "parse_mode": "HTML",
        }

        try:
            response = requests.post(url, json=payload, timeout=5)
            response.raise_for_status()
        except requests.RequestException as e:
            print("Telegram error:", e)



@receiver(signal=post_save, sender=User)
def set_activation_code(sender, instance, created, *args, **kwargs):
    if created:
        instance.activation_code = f"{instance.id}{instance.last_name[0].capitalize()}{randint(10, 50)}{instance.first_name[0]}"
        instance.save(update_fields=['activation_code'])
