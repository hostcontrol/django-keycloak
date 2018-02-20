from django.contrib import admin, messages

from django_keycloak.models import Realm

import django_keycloak.services.permissions
import django_keycloak.services.realm


def refresh_open_id_connect_well_known(modeladmin, request, queryset):
    for realm in queryset:
        django_keycloak.services.realm.refresh_well_known_oidc(realm=realm)
    modeladmin.message_user(
        request=request,
        message='OpenID Connect .well-known refreshed',
        level=messages.SUCCESS
    )


refresh_open_id_connect_well_known.short_description = 'Refresh OpenID ' \
                                                       'Connect .well-known'


def refresh_uma_well_known(modeladmin, request, queryset):
    for realm in queryset:
        django_keycloak.services.realm.refresh_well_known_uma(realm=realm)
    modeladmin.message_user(
        request=request,
        message='UMA .well-known refreshed',
        level=messages.SUCCESS
    )


refresh_uma_well_known.short_description = 'Refresh UMA .well-known'


def refresh_certs(modeladmin, request, queryset):
    for realm in queryset:
        django_keycloak.services.realm.refresh_certs(realm=realm)
    modeladmin.message_user(
        request=request,
        message='Certificates refreshed',
        level=messages.SUCCESS
    )


refresh_certs.short_description = 'Refresh Certificates'


def clear_client_tokens(modeladmin, request, queryset):
    queryset.update(
        access_token=None,
        expires_before=None,
        refresh_token=None,
        refresh_expires_before=None
    )
    modeladmin.message_user(
        request=request,
        message='Tokens cleared',
        level=messages.SUCCESS
    )


clear_client_tokens.short_description = 'Clear client tokens'


def synchronize_permissions(modeladmin, request, queryset):
    for realm in queryset:
        django_keycloak.services.permissions.synchronize(realm=realm)


synchronize_permissions.short_description = 'Synchronize permissions'


class RealmAdmin(admin.ModelAdmin):

    actions = [
        refresh_open_id_connect_well_known,
        refresh_uma_well_known,
        refresh_certs,
        clear_client_tokens,
        synchronize_permissions
    ]

    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        ('Location', {
            'fields': ('server_url', 'internal_server_url', '_well_known_oidc',
                       '_well_known_uma')
        }),
        ('Credentials', {
            'fields': ('client_id', 'client_secret')
        })
    )

    readonly_fields = ('_well_known_oidc', '_well_known_uma')


admin.site.register(Realm, RealmAdmin)