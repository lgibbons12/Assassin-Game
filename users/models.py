from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

# Create your models here.
class CustomUser(AbstractUser):
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"


    
class Player(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    is_dead = models.BooleanField(default=False)
    target_name = models.CharField(max_length=255, blank=True, null=True)
    target_pk = models.IntegerField(null=True, blank=True)
    kills = models.IntegerField(default=0)
    is_playing = models.BooleanField(default=True)
    is_winner = models.BooleanField(default=False)
    in_waiting = models.BooleanField(default=False)
    def set_target(self, target):
        self.target_name = target.user.name
        self.target_pk = target.pk
        self.save()

    def discovered(self):
        self.is_dead = True
        self.save()
    def get_killed(self):
        checker_instance, created = Checker.objects.get_or_create(target=self)

        checker_instance.target_confirm()
        checker_instance.save()

    


    def kill_target(self):
        targeting = Player.objects.get(pk = self.target_pk)
        checker_instance, created = Checker.objects.get_or_create(target=targeting)

        checker_instance.killer = self

        checker_instance.killer_confirm()
        checker_instance.save()

    @receiver(post_save, sender=CustomUser)
    def create_player(sender, instance, created, **kwargs):
        if created:
            Player.objects.create(user=instance)

class Checker(models.Model):
    target = models.ForeignKey('Player', related_name='target_checker', on_delete=models.CASCADE)
    killer = models.ForeignKey('Player', related_name='killer_checker', null=True, blank=True, on_delete=models.CASCADE)
    confirmations = models.IntegerField(default=0)
    target_confirmed = models.BooleanField(default=False)
    killer_confirmed = models.BooleanField(default=False)
    shown_to_target = models.BooleanField(default=False)
    shown_to_killer = models.BooleanField(default = False)



    def deletion(self):
        if self.shown_to_killer and self.shown_to_target:
            self.delete()
    def target_confirm(self):
        if not self.target_confirmed:
            self.confirmations += 1
            self.target_confirmed = True
            #self.checking()

    def killer_confirm(self):
        if not self.killer_confirmed:
            self.confirmations += 1
            self.killer_confirmed = True
            #self.checking()

    def checking(self):
        from .game import GameManager
        if self.confirmations == 2:
            # Do something when both target and killer are confirmed
            gm = GameManager()
            if gm.win_condition():
                return False
            self.target.is_dead = True
            self.target.in_waiting = False
            self.target.save()

            self.killer.kills += 1
            self.killer.in_waiting = False
            self.killer.save()
            
            gm.new_target(self.killer, self.target)

            return True
        return False
    