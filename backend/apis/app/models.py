from django.db import models
from django.utils import timezone

class User(models.Model):
    """Model representing Flexing Users."""
    
    full_name = models.CharField(max_length=50, default='Flexer')
    phone_number = models.CharField(max_length=15, unique=True)  # Use a more appropriate max length for phone numbers
    bio = models.CharField(max_length=100, default="Hey, I'm flexing! 💪")
    created = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated = models.DateTimeField(auto_now=True)  # Automatically set on update

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created']


class OneTimePassword(models.Model):
    """Model representing One-Time Passwords for Users."""
    
    PENDING = 'pending'
    VERIFIED = 'verified'
    EXPIRED = 'expired'

    OTP_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (VERIFIED, 'Verified'),
        (EXPIRED, 'Expired'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otps')
    password = models.CharField(max_length=6)  # Consider using a CharField for OTPs (for better flexibility)
    status = models.CharField(max_length=8, choices=OTP_STATUS_CHOICES, default=PENDING)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"OTP for {self.user.full_name} - {self.get_status_display()}"

    class Meta:
        verbose_name = 'One-Time Password'
        verbose_name_plural = 'One-Time Passwords'
        ordering = ['-created']
        indexes = [
            models.Index(fields=['user', 'status']),
        ]


class FlexChats(models.Model):
    """Model representing Flex chats for Users."""
    
    SENT = 'sent'
    DELIVERED = 'delivered'
    READ = 'read'

    MESSAGE_STATUSES = [
        (SENT, 'Sent'),
        (DELIVERED, 'Delivered'),
        (READ, 'Read'),
    ]

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_id')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver_id')
    message = models.TextField(max_length=500)
    status = models.CharField(max_length=8, choices=MESSAGE_STATUSES, default=SENT)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"OTP for {self.user.full_name} - {self.get_status_display()}"

    class Meta:
        verbose_name = 'Flex Chat Massage'
        verbose_name_plural = 'Flex Chat Massages'
        ordering = ['-created']