from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.
class CustomUser(AbstractUser):
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"


    
class Player(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    is_dead = models.BooleanField(default=False)
    target_name = models.CharField(max_length=255, blank=True, null=True)
    target_pk = models.IntegerField(default = None)
    kills = models.IntegerField(default=0)
    is_playing = models.BooleanField(default=True)
    def set_target(self, target):
        self.target_name = target.user.name
        self.target_pk = target.pk
        self.save()

    def get_killed(self):
        self.is_dead = True
        self.save()

    def new_target(self):
        # Implement logic to randomly choose a new target
        pass

    def kill_target(self):
        pass

class Checker(models.Model):
    target = models.ForeignKey('Player', related_name='target_checker', on_delete=models.CASCADE)
    killer = models.ForeignKey('Player', related_name='killer_checker', null=True, blank=True, on_delete=models.CASCADE)
    confirmations = models.IntegerField(default=0)
    target_confirmed = models.BooleanField(default=False)
    killer_confirmed = models.BooleanField(default=False)

    def target_confirm(self):
        if not self.target_confirmed:
            self.confirmations += 1
            self.target_confirmed = True
            self.checking()

    def killer_confirm(self):
        if not self.killer_confirmed:
            self.confirmations += 1
            self.killer_confirmed = True
            self.checking()

    def checking(self):
        if self.confirmations == 2:
            # Do something when both target and killer are confirmed
            self.target.user.is_dead = True
            self.kill()
    