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


class ClientRequest(TimeStampedModel):
    id = models.AutoField(primary_key=True)

    company_email = models.EmailField()
    password_hash = models.CharField(max_length=255)
    company_phone = models.CharField(max_length=20)
    company_name = models.CharField(max_length=255)
    company_website = models.URLField(blank=True, null=True)

    industry_type = models.CharField(max_length=150)
    company_size = models.CharField(max_length=50)

    request_status = models.CharField(max_length=50)

    approved_by_administrator = models.ForeignKey(
        Administrator,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="approved_by_administrator_id"
    )

    approved_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "clients_requests"

    def __str__(self):
        return self.company_name


class Client(TimeStampedModel):
    id = models.AutoField(primary_key=True)

    request = models.OneToOneField(
        ClientRequest,
        on_delete=models.CASCADE,
        unique=True,
        db_column="request_id"
    )

    password_hash = models.CharField(max_length=255)
    company_logo = models.ImageField(upload_to="client_logos/", blank=True, null=True)

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    last_login = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "clients"

    def __str__(self):
        return f"Client #{self.id}"


class ClientRole(TimeStampedModel):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=100)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "client_roles"

    def __str__(self):
        return self.role_name


class ClientUser(TimeStampedModel):
    id = models.AutoField(primary_key=True)

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        db_column="client_id"
    )

    role = models.ForeignKey(
        ClientRole,
        on_delete=models.SET_NULL,
        null=True,
        db_column="role_id"
    )

    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)

    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "client_users"

    def __str__(self):
        return self.email
