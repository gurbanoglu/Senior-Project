from django.db import models

# The 'RoomMember' model here permits the storing of a name,
# user ID, room name, and keeps track of whether the user is in
# a video meeting room.


class RoomMember(models.Model):
    m_name = models.CharField(max_length=200, verbose_name="Name")
    m_userID = models.CharField(max_length=1000, verbose_name="User ID")
    m_roomName = models.CharField(max_length=200, verbose_name="Room Name")
    m_insession = models.BooleanField(default=True, verbose_name="In Session")

    # Return back the user's name.
    def __str__(self):
        return self.m_name

    class Meta:
        verbose_name = "Room Member"
        verbose_name_plural = "Room Members"

# 7
