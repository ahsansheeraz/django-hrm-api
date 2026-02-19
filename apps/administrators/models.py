from django.db import models
from django.utils import timezone

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AdministratorRole(TimeStampedModel):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=100)
    adminsistrators_roles_status = models.BooleanField(default=True)

    class Meta:
        db_table = "adminsistrators_roles"

    def __str__(self):
        return self.role_name


class Administrator(TimeStampedModel):
    id = models.AutoField(primary_key=True)

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)

    first_name = models.CharField(max_length=100)
    mid_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)

    phone = models.CharField(max_length=20, blank=True, null=True)
    designation = models.CharField(max_length=150, blank=True, null=True)
    photo = models.ImageField(upload_to="admin_photos/", blank=True, null=True)

    role = models.ForeignKey(
        AdministratorRole,
        on_delete=models.SET_NULL,
        null=True,
        db_column="role_id"
    )

    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)

    last_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "adminsistrators"

    def __str__(self):
        return self.username
