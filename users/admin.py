from django.contrib import admin
from .models import CustomUser, Player, Checker, AgentGroup, Game
from .game import GameManager
from django.http import HttpResponse
import csv
import tempfile
from django.contrib.auth import get_user_model
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
    actions = ['assign_targets', 'discovered', 'killed_target', 'reset_elimination', 'add_players']
    list_display = ['user', 'is_dead', 'kills', 'is_playing', 'in_waiting']
    
    search_fields = ['user__first_name', 'user__last_name']
    

    def get_action_choices(self, request):
        # Get the default choices (including the blank choice represented by dashes)
        choices = super().get_action_choices(request)

        # Remove the first choice (the blank choice)
        choices.pop(0)

        # Add your custom choice (e.g., "Actions") at the beginning
        custom_choice = ("", "Actions:")
        choices.insert(0, custom_choice)

        return choices

    #specific filtration
    # Define custom list filters with custom names
    class IsDeadFilter(admin.SimpleListFilter):
        title = 'Is Eliminated?'  # Custom name for the filter
        parameter_name = 'is_eliminated'

        def lookups(self, request, model_admin):
            return (
                ('yes', 'Eliminated'),  # Custom names for filter options
                ('no', 'Active'),
            )

        def queryset(self, request, queryset):
            if self.value() == 'yes':
                return queryset.filter(is_dead=True)
            if self.value() == 'no':
                return queryset.filter(is_dead=False)

    class IsWaitingFilter(admin.SimpleListFilter):
        title = 'Is Waiting?'  # Custom name for the filter
        parameter_name = 'in_waiting'

        def lookups(self, request, model_admin):
            return (
                ('yes', 'Waiting'),  # Custom names for filter options
                ('no', 'Engaged'),
            )

        def queryset(self, request, queryset):
            if self.value() == 'yes':
                return queryset.filter(in_waiting=True)
            if self.value() == 'no':
                return queryset.filter(in_waiting=False)

    class IsPlayingFilter(admin.SimpleListFilter):
        title = 'Is Playing?'  # Custom name for the filter
        parameter_name = 'is_playing'

        def lookups(self, request, model_admin):
            return (
                ('yes', 'Playing'),  # Custom names for filter options
                ('no', 'Not In The Game'),
            )

        def queryset(self, request, queryset):
            if self.value() == 'yes':
                return queryset.filter(is_playing=True)
            if self.value() == 'no':
                return queryset.filter(is_playing=False)

    # Register custom list filters
    list_filter = (IsDeadFilter, IsWaitingFilter, IsPlayingFilter)

    def assign_targets(self, request, queryset):
        GameManager.assign_targets()

    def shuffle(self, request, queryset):
        GameManager.assign_targets(new_game=False)

    def discovered(self, request, queryset):
        for player in queryset:
            player.discovered()

    def killed_target(self, request, queryset):
        for player_instance in queryset:

            gm = GameManager()
            if gm.win_condition():
                return False
            player_instance.target.is_dead = True
            player_instance.target.in_waiting = False
            player_instance.target.save()

            player_instance.killer.kills += 1
            player_instance.killer.have_eliminated_today = True
            player_instance.killer.in_waiting = False
            player_instance.killer.save()
            
            gm.new_target(self.killer, self.target)

    def reset_elimination(self, request, queryset):
        for player in queryset:
            player.is_dead = False
            player.save()

   

    assign_targets.short_description = 'Assign Targets'
    discovered.short_description = 'Mark as Dead'
    killed_target.short_description = 'Kill Target'
    reset_elimination.short_description = 'Revive Player'
    

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class CheckerAdmin(admin.ModelAdmin):
    actions = ['checking']
    list_display = ['get_target_name', 'get_killer_name', 'confirmations', 'target_confirmed', 'killer_confirmed', 'action_performed']
    list_filter = ['target_confirmed', 'killer_confirmed', 'action_performed']


    class TargetConfirmedFilter(admin.SimpleListFilter):
        title = 'Target Confirmed?'  # Custom name for the filter
        parameter_name = 'target_confirmed'

        def lookups(self, request, model_admin):
            return (
                ('yes', 'Target Confirmed'),  # Custom names for filter options
                ('no', 'Target Waiting'),
            )

        def queryset(self, request, queryset):
            if self.value() == 'yes':
                return queryset.filter(is_playing=True)
            if self.value() == 'no':
                return queryset.filter(is_playing=False)
    
    class KillerConfirmedFilter(admin.SimpleListFilter):
        title = 'Killer Confirmed?'  # Custom name for the filter
        parameter_name = 'killer_confirmed'

        def lookups(self, request, model_admin):
            return (
                ('yes', 'Killer Confirmed'),  # Custom names for filter options
                ('no', 'Killer Waiting'),
            )

        def queryset(self, request, queryset):
            if self.value() == 'yes':
                return queryset.filter(is_playing=True)
            if self.value() == 'no':
                return queryset.filter(is_playing=False)
    
    class ActionPerformedFilter(admin.SimpleListFilter):
        title = 'Action Performed?'  # Custom name for the filter
        parameter_name = 'action_performed'

        def lookups(self, request, model_admin):
            return (
                ('yes', 'Action Performed'),  # Custom names for filter options
                ('no', 'Waiting for Action'),
            )

        def queryset(self, request, queryset):
            if self.value() == 'yes':
                return queryset.filter(is_playing=True)
            if self.value() == 'no':
                return queryset.filter(is_playing=False)

    # Register custom list filters
    list_filter = (TargetConfirmedFilter, KillerConfirmedFilter, ActionPerformedFilter)

    def get_action_choices(self, request):
        # Get the default choices (including the blank choice represented by dashes)
        choices = super().get_action_choices(request)

        # Remove the first choice (the blank choice)
        choices.pop(0)

        # Add your custom choice (e.g., "Actions") at the beginning
        custom_choice = ("", "Actions:")
        choices.insert(0, custom_choice)

        return choices
    
    def get_target_name(self, obj):
        return f"{obj.target.user.first_name} {obj.target.user.last_name}" if obj.target else None
    get_target_name.short_description = 'Target Name'

    def get_killer_name(self, obj):
        return f"{obj.killer.user.first_name} {obj.killer.user.last_name}" if obj.killer else None
    get_killer_name.short_description = 'Killer Name'

    def target_user(self, obj):
        return obj.target.user.name if obj.target else None
    target_user.short_description = 'Target User'

    def killer_user(self, obj):
        return obj.killer.user.name if obj.killer else None
    killer_user.short_description = 'Killer User'

    def checking(self, request, queryset):
        for obj in queryset:
            obj.checking()

    checking.short_description = 'Check and Perform Actions'

"""
class CheckerAdmin(admin.ModelAdmin):
    actions = ['checking']
    list_display = ['get_target_pk', 'get_killer_pk', 'confirmations', 'target_confirmed', 'killer_confirmed', 'action_performed']

    def get_target_pk(self, obj):
        return obj.target.pk if obj.target else None
    get_target_pk.short_description = 'Target PK'

    def get_killer_pk(self, obj):
        return obj.killer.pk if obj.killer else None
    get_killer_pk.short_description = 'Killer PK'
    list_filter = ['target_confirmed', 'killer_confirmed', 'action_performed']
    def target_user(self, obj):
        return obj.target.user.name

    def killer_user(self, obj):
        return obj.killer.user.name if obj.killer else None
    
    def target_pk(self, obj):
        return obj.target.pk
    
    def killer_pk(self, obj):
        return obj.killer.pk

    target_user.short_description = 'Target User'
    killer_user.short_description = 'Killer User'

    def checking(self, request, queryset):
        for obj in queryset:
            obj.checking()


"""

class AgentGroupAdmin(admin.ModelAdmin):
    actions = ['assignGroupTargets', 'replace_groups']
    list_display = ['group_name', 'get_players', 'is_out', 'is_playing']

    def get_players(self, obj):
        return ", ".join([f"{player.user.first_name} {player.user.last_name}" for player in obj.players.all()])

    get_players.short_description = 'Players'

    def assignGroupTargets(self, request, queryset):
        GameManager().assign_group_targets()
    
    def replace_groups(self, request, queryset):
        for obj in AgentGroup.objects.all():
            obj.players.clear()
            obj.save()
        
        
        Game.objects.all().delete()
        Game(state=1, placing_groups=True).save()
    
    
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Checker, CheckerAdmin)
admin.site.register(AgentGroup, AgentGroupAdmin)
admin.site.register(Game)
