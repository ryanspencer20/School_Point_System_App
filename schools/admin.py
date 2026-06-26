from django.contrib import admin

from .models import (
    PointAward,
    PointCategory,
    School,
    SchoolMembership,
    SchoolRegistration,
    SchoolYear,
    Team,
    TeamMembership,
)


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "contact_email", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "slug", "contact_email")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(SchoolRegistration)
class SchoolRegistrationAdmin(admin.ModelAdmin):
    list_display = ("school_name", "contact_name", "contact_email", "status", "submitted_at")
    list_filter = ("status",)
    search_fields = ("school_name", "contact_name", "contact_email")
    readonly_fields = ("submitted_at",)


@admin.register(SchoolYear)
class SchoolYearAdmin(admin.ModelAdmin):
    list_display = ("name", "school", "start_date", "end_date", "is_current")
    list_filter = ("school", "is_current")
    search_fields = ("name", "school__name")


@admin.register(SchoolMembership)
class SchoolMembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "school", "role", "is_active", "joined_at")
    list_filter = ("role", "is_active", "school")
    search_fields = ("user__username", "user__email", "school__name")


class TeamMembershipInline(admin.TabularInline):
    model = TeamMembership
    extra = 0


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "school", "school_year", "color", "display_order")
    list_filter = ("school", "school_year")
    search_fields = ("name", "school__name")
    inlines = [TeamMembershipInline]


@admin.register(PointCategory)
class PointCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "school", "slug")
    list_filter = ("school",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(PointAward)
class PointAwardAdmin(admin.ModelAdmin):
    list_display = ("team", "amount", "reason", "category", "awarded_by", "created_at")
    list_filter = ("school", "school_year", "category")
    search_fields = ("reason", "team__name", "school__name")
    readonly_fields = ("created_at",)
