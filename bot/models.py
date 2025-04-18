from django.db import models

# Create your models here.


class User(models.Model):
    chat_id = models.BigIntegerField(null=True, blank=True, default=0)
    role = models.CharField(max_length=255, null=True, blank=True,
                            choices=[('ADMIN', 'Admin'), ('USER', 'Foydalanuvchi')],
                            default='USER')
    def __str__(self):
        return self.chat_id

class ChannelsToSubscribe(models.Model):
    link = models.CharField(max_length=255)

    def __str__(self):
        return self.link
class VideoInformation(models.Model):
    video_number=models.IntegerField( default=0)
    video_title=models.CharField(max_length=255)
    video_id=models.TextField(null=True, blank=True)
    def __str__(self):
        return self.video_id

class MagicWord(models.Model):
    word=models.CharField(max_length=255)

    def __str__(self):
        return self.word