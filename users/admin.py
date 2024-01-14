from django.contrib import admin
from .models import CustomUser, Player, Checker
from .game import GameManager

class PlayerAdmin(admin.ModelAdmin):
    actions = ['kill_player', 'assign_targets']
    list_display = ['user_name', 'is_dead', 'target_name', 'kills', 'is_playing', 'in_waiting']

    def assign_targets(self, request, queryset):
        gm = GameManager()
        gm.assign_targets()

    def kill_player(self, request, queryset):
        for player in queryset:
            target = Player.objects.get(pk=player.target_pk)
            print(f"{player.user.name} is going to kill their target {target.user.name}")
            print(f"The target's target is {target.target_name}, so it should be the players after")
            target.get_killed()
            player.kill_target()

    def user_name(self, obj):
        return obj.user.name

    user_name.short_description = 'User Name'

class CheckerAdmin(admin.ModelAdmin):
    actions = ['checking']
    list_display = ['target_user', 'killer_user', 'confirmations', 'target_confirmed', 'killer_confirmed', 'shown_to_target', 'shown_to_killer']

    def target_user(self, obj):
        return obj.target.user.name

    def killer_user(self, obj):
        return obj.killer.user.name if obj.killer else None

    target_user.short_description = 'Target User'
    killer_user.short_description = 'Killer User'

    def checking(self, request, queryset):
        for obj in queryset:
            obj.checking()

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Checker, CheckerAdmin)
