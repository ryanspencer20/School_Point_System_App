from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models


class School(models.Model):
    """A registered school using the spirit points system."""

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=80, unique=True)
    contact_email = models.EmailField()
    is_active = models.BooleanField(
        default=False,
        help_text="Inactive schools cannot log in or manage points until approved.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class SchoolRegistration(models.Model):
    """Pending signup request before a school account is activated."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending review"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    school_name = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=120)
    contact_email = models.EmailField()
    message = models.TextField(
        blank=True,
        help_text="Optional note from the school about how they plan to use the app.",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    school = models.OneToOneField(
        School,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="registration",
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.school_name} ({self.get_status_display()})"


class SchoolYear(models.Model):
    """One academic year for a school; points are tracked per year."""

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="school_years",
    )
    name = models.CharField(
        max_length=9,
        validators=[MinLengthValidator(4)],
        help_text='Example: "2025-2026".',
    )
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ["-start_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["school", "name"],
                name="unique_school_year_name_per_school",
            ),
        ]

    def __str__(self):
        return f"{self.school.name} — {self.name}"


class SchoolMembership(models.Model):
    """Links a Django user to a school with a role. Passwords stay on auth.User."""

    class Role(models.TextChoices):
        ADMIN = "admin", "School admin"
        STAFF = "staff", "Staff (award points)"
        STUDENT = "student", "Student"
        VIEWER = "viewer", "Viewer (read-only)"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="school_memberships",
    )
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    role = models.CharField(max_length=20, choices=Role.choices)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["school__name", "user__username"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "school"],
                name="unique_user_membership_per_school",
            ),
        ]

    def __str__(self):
        return f"{self.user.get_username()} @ {self.school.name} ({self.get_role_display()})"


class Team(models.Model):
    """A spirit team / house within a school year."""

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="teams",
    )
    school_year = models.ForeignKey(
        SchoolYear,
        on_delete=models.CASCADE,
        related_name="teams",
    )
    name = models.CharField(max_length=100)
    color = models.CharField(
        max_length=7,
        default="#333333",
        help_text="Hex color for leaderboard display, e.g. #C0392B.",
    )
    motto = models.CharField(max_length=200, blank=True)
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["school_year", "name"],
                name="unique_team_name_per_school_year",
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.school_year.name})"


class TeamMembership(models.Model):
    """Optional assignment of a user to a team for a given year."""

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="team_memberships",
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["team", "user"],
                name="unique_user_on_team",
            ),
        ]

    def __str__(self):
        return f"{self.user.get_username()} → {self.team.name}"


class PointCategory(models.Model):
    """Reason grouping for awards, e.g. behavior, events, initiatives."""

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="point_categories",
    )
    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=80)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "point categories"
        constraints = [
            models.UniqueConstraint(
                fields=["school", "slug"],
                name="unique_point_category_slug_per_school",
            ),
        ]

    def __str__(self):
        return f"{self.school.name} — {self.name}"


class PointAward(models.Model):
    """A single points change for a team (+ or -)."""

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="point_awards",
    )
    school_year = models.ForeignKey(
        SchoolYear,
        on_delete=models.CASCADE,
        related_name="point_awards",
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="point_awards",
    )
    category = models.ForeignKey(
        PointCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="point_awards",
    )
    amount = models.IntegerField(
        help_text="Use positive numbers to award points and negative numbers to deduct.",
    )
    reason = models.CharField(max_length=255)
    awarded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="point_awards_given",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        sign = "+" if self.amount >= 0 else ""
        return f"{self.team.name}: {sign}{self.amount} ({self.reason})"
