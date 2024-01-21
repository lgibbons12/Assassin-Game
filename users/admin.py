from django.contrib import admin
from .models import CustomUser, Player, Checker
from .game import GameManager
from django.http import HttpResponse
import csv

class PlayerAdmin(admin.ModelAdmin):
    actions = ['assign_targets', 'save_info', 'admin_process_kill', 'discovered']
    list_display = ['user_name', 'is_dead', 'target_name', 'kills', 'is_playing', 'in_waiting']

    def assign_targets(self, request, queryset):
        gm = GameManager()
        gm.assign_targets()

    def discovered(self, request, queryset):
        for player_instance in queryset:
            player_instance.discovered()
            player_instance.save()

    def admin_process_kill(self, request, queryset):
        for player_instance in queryset:
           
            targeting = Player.objects.get(pk=player_instance.target_pk)
            gm = GameManager()

            player_instance.kills += 1
            player_instance.in_waiting = False
            player_instance.save()


            gm.new_target(player_instance, targeting)

    def user_name(self, obj):
        return obj.user.name
    
    def save_info(self, request, queryset):
        # Define the response as a CSV file
        response = HttpResponse(content_type='text/csv')
        file_path = 'static/users/players_export.csv'
        response['Content-Disposition'] = f'attachment; filename="{file_path}"'


        # Create a CSV writer
        csv_writer = csv.writer(response)

        # Write header row
        header_row = ['User ID', 'Username', 'Email', 'Is Dead', 'Target Name', 'Target PK', 'Kills', 'Is Playing', 'Is Winner', 'In Waiting']
        csv_writer.writerow(header_row)

        # Write data rows
        for player in queryset:
            data_row = [player.user.id, player.user.username, player.user.email, player.is_dead, player.target_name,
                        player.target_pk, player.kills, player.is_playing, player.is_winner, player.in_waiting]
            csv_writer.writerow(data_row)

        return response


    user_name.short_description = 'User Name'

class CheckerAdmin(admin.ModelAdmin):
    actions = ['checking']
    list_display = ['target_user', 'killer_user', 'confirmations', 'target_confirmed', 'killer_confirmed', 'action_performed']

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
