from django.db import models
from django.conf import settings
import uuid

# Create your models here.
User = settings.AUTH_USER_MODEL


class Room(models.Model):
    name = models.CharField(max_length=128)
    online = models.ManyToManyField(to=User, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4())

    def get_online_count(self):
        return self.online.count()

    def join(self, user):
        """A helper function to add a user to a Room and create an event object"""
        self.online.add(user)
        self.event_set.create(type="Join", user=user)
        self.save()

    def leave(self, user):
        """An helper function to remove users from group members when they \
                leave the group and create an event for the timestamp the user left the group"""
        self.online.remove(user)
        self.event_set.create(type="Left", user=user)
        self.save()

    def __str__(self):
        return f'{self.name} ({self.get_online_count()})'


class Message(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content} [{self.timestamp}]'


class Event(models.Model):
    """
    A model that holds all events related to a group like when a user joins the group or leaves.
    """
    CHOICES = [
        ("Join", "join"),
        ("Left", "left")
    ]
    type = models.CharField(choices=CHOICES, max_length=10)
    description = models.CharField(max_length=50, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.description = f"{self.user} {self.type} the {self.room.name} room"
        super().save(*args, kwargs)

    def __str__(self) -> str:
        return f"{self.description}"
