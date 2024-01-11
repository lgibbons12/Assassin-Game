from django.contrib import admin
from .models import CustomUser, Player, Checker
from .game import GameManager

class PlayerAdmin(admin.ModelAdmin):
    actions = ['kill_player', 'assign_targets']
    list_display = ['user_name', 'is_dead', 'target_name', 'kills', 'is_playing']

    def assign_targets(self, request, queryset):
        gm = GameManager()
        gm.assign_targets()

    def kill_player(self, request, queryset):
        for player in queryset:
            target = Player.objects.get(pk=player.target_pk)
            print(f"{player.user.name} is going to kill their target {target.user.name}")
            print(f"The target's target is {target.target_name}, so it should be the players afer")
            target.get_killed()
            player.kill_target()

        

    def user_name(self, obj):
        return obj.user.name

    user_name.short_description = 'User Name'



admin.site.register(CustomUser)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Checker)