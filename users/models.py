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
    agent_name = models.CharField(max_length=255, blank=True, null=True)
    kills = models.IntegerField(default=0)
    is_playing = models.BooleanField(default=True)
    is_winner = models.BooleanField(default=False)
    in_waiting = models.BooleanField(default=False)
    have_eliminated_today = models.BooleanField(default=False)

    def set_target(self, target):
        self.target_name = target.user.name
        self.target_pk = target.pk
        self.save()
    
    def agent_selection(self, callsign):
        self.agent_name = callsign
        self.save()
    def discovered(self):
        self.is_dead = True
        self.save()
    def get_killed(self):
        checker_instance, created = Checker.objects.get_or_create(target=self)

        checker_instance.target_confirm()
        checker_instance.save()

    def self_defense_killed(self):
        targeting = Player.objects.filter(is_dead=False, is_playing=True, target_pk=self.pk).first()
        if targeting is None:
            from .game import GameManager
            GameManager()._refresh_targets()
        # Check if a Checker with target=targeting and self_defense=True already exists
        existing_checker = Checker.objects.filter(target=targeting, self_defense=True).first()

        if existing_checker:
            # If the Checker already exists, update the killer and confirmations
            existing_checker.killer = self
            existing_checker.killer_confirm()
            existing_checker.save()
        else:
            # If the Checker doesn't exist, create a new one with the killer assigned
            checker_instance = Checker.objects.create(target=targeting, killer=self, self_defense=True)
            checker_instance.killer_confirm()  # Assuming you want to confirm the killer immediately
            checker_instance.save()

        # Additional actions or save the player if needed
       
    
    def self_defense_died(self):
        # Check if a Checker with target=self and self_defense=True already exists
        existing_checker = Checker.objects.filter(target=self, self_defense=True).first()

        if existing_checker:
            # If the Checker already exists, update the confirmations
            existing_checker.target_confirm()
            existing_checker.save()
        else:
            # If the Checker doesn't exist, create a new one with the target confirmed
            checker_instance = Checker.objects.create(target=self, self_defense=True)
            checker_instance.target_confirm()


    def kill_target(self):
        targeting = Player.objects.filter(is_dead=False, is_playing=True, pk=self.target_pk).first()

        # Check if a Checker with the target=targeting already exists
        existing_checker = Checker.objects.filter(target=targeting).first()

        if existing_checker:
            # If the Checker already exists, update the killer and confirmations
            existing_checker.killer = self
            existing_checker.killer_confirm()
            existing_checker.save()
        else:
            # If the Checker doesn't exist, create a new one with the killer assigned
            checker_instance = Checker.objects.create(target=targeting, killer=self)
            checker_instance.killer_confirm()  # Assuming you want to confirm the killer immediately
            checker_instance.save()
        # Additional actions or save the player if needed
        

    @receiver(post_save, sender=CustomUser)
    def create_player(sender, instance, created, **kwargs):
        if created:
            Player.objects.create(user=instance)

class Checker(models.Model):
    target = models.ForeignKey('Player', related_name='target_checker', null=True, blank=True, on_delete=models.CASCADE)
    killer = models.ForeignKey('Player', related_name='killer_checker', null=True, blank=True, on_delete=models.CASCADE)
    confirmations = models.IntegerField(default=0)
    self_defense = models.BooleanField(default=False)
    target_confirmed = models.BooleanField(default=False)
    killer_confirmed = models.BooleanField(default=False)
    action_performed = models.BooleanField(default=False)



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
        if self.self_defense and self.confirmations == 2 and self.action_performed == False:
            gm = GameManager()
            if gm.win_condition():
                return False
            
            self.target.is_dead = True
            self.target.in_waiting = False
            self.target.save()

            self.killer.kills += 1
            self.killer.have_eliminated_today = True
            self.killer.in_waiting = False
            self.killer.save()

            self.action_performed = True
            self.save()

            return True

        if self.confirmations == 2 and self.action_performed == False:
            # Do something when both target and killer are confirmed
            gm = GameManager()
            if gm.win_condition():
                return False
            self.target.is_dead = True
            self.target.in_waiting = False
            self.target.save()

            self.killer.kills += 1
            self.killer.have_eliminated_today = True
            self.killer.in_waiting = False
            self.killer.save()
            
            gm.new_target(self.killer, self.target)

            self.action_performed = True
            self.save()

            return True

        if self.action_performed == True:
            if self.killer.target_pk == self.target.pk:
                print("There has been an error")
        return False
    