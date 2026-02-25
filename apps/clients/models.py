from django.db import models
from django.utils import timezone

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class ClientRequest(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey("Client", on_delete=models.CASCADE, db_column="client_id")
    company_phone = models.CharField(max_length=20)
    company_website = models.URLField(blank=True, null=True)
    industry_type = models.CharField(max_length=150)
    company_size = models.CharField(max_length=50)

    request_status = models.CharField(max_length=50, default="pending")
    approved_by_administrator = models.ForeignKey(
        "administrators.Administrator",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="approved_by_administrator_id"
    )
    approved_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "clients_requests"

    def __str__(self):
        return f"Request #{self.id} - Client {self.client.company_name}"


class Client(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=255)
    company_email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    company_phone = models.CharField(max_length=20, blank=True, null=True)
    company_website = models.URLField(blank=True, null=True)
    industry_type = models.CharField(max_length=150, blank=True, null=True)
    company_size = models.CharField(max_length=50, blank=True, null=True)
    company_logo = models.ImageField(upload_to="client_logos/", blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "clients"

    def __str__(self):
        return self.company_name

    @property
    def is_authenticated(self):
        # This makes DRF happy for permission checks
        return True
    
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
    client = models.ForeignKey(Client, on_delete=models.CASCADE, db_column="client_id")
    role = models.ForeignKey(ClientRole, on_delete=models.SET_NULL, null=True, db_column="role_id")
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
