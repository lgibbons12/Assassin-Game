from django.contrib import admin
from .models import CustomUser, Player, Checker
from .game import GameManager
from django.http import HttpResponse
import csv
import tempfile

def save_info(queryset):
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
class PlayerAdmin(admin.ModelAdmin):
    actions = ['assign_targets', 'save_info','discovered', 'admin_process_kill', 'double_or_no', 'shuffle',
               'all_have_not_eliminated_today']
    list_display = ['user_name', 'is_dead', 'kills', 'is_playing', 'in_waiting']
    list_filter = ['is_dead', 'in_waiting', 'have_eliminated_today']
    search_fields = ['target_name']

    def assign_targets(self, request, queryset):
        gm = GameManager()
        gm.assign_targets()
    
    def all_have_not_eliminated_today(self, request, queryset):
        for obj in Player.objects.filter(is_playing=True, is_dead=False):
            obj.have_eliminated_today = False
            obj.save()

    def shuffle(self, request, queryset):
        response = save_info(queryset)  # Call save_info and store the response
        GameManager().assign_targets(new_game=False)
        return response
        
    def discovered(self, request, queryset):
        for obj in queryset:
            obj.discovered()

    def double_or_no(modeladmin, request, queryset):
        alive_players = Player.objects.filter(is_dead=False)

        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            for player_instance in alive_players:
                target_count = Player.objects.filter(target_pk=player_instance.pk).count()

                if target_count == 0:
                    temp_file.write(f"{player_instance.user.name} has not been targeted by anyone.\n")
                elif target_count > 1:
                    temp_file.write(f"{player_instance.user.name} has been targeted by more than one person.\n")

            # Provide the download link for the temp file
            temp_file_path = temp_file.name

        # Return the file response for download
        with open(temp_file_path, 'r') as file:
            response = HttpResponse(file.read(), content_type='text/plain')
            response['Content-Disposition'] = f'attachment; filename=double_or_no_results.txt'

        return response


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
        response = save_info(queryset)
        return response


    user_name.short_description = 'User Name'

class CheckerAdmin(admin.ModelAdmin):
    actions = ['checking']
    list_display = ['target_user', 'killer_user', 'confirmations', 'target_confirmed', 'killer_confirmed', 'action_performed']
    list_filter = ['target_confirmed', 'killer_confirmed', 'action_performed']
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
