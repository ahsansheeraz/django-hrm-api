# from django.contrib import admin
# """
# from .models import Client, ClientRequest, ClientUser

# @admin.register(Client)
# class ClientAdmin(admin.ModelAdmin):
#     list_display = (
#         "id",
#         "company_name",
#         "email",
#         "is_active",
#         "created_at",
#     )

#     list_filter = (
#         "is_active",
#         "created_at",
#     )

#     search_fields = (
#         "company_name",
#         "email",
#     )

#     ordering = ("-created_at",)

#     readonly_fields = ("created_at",)



# @admin.register(ClientRequest)
# class ClientRequestAdmin(admin.ModelAdmin):
#     list_display = (
#         "id",
#         "client",
#         "status",
#         "requested_at",
#     )

#     list_filter = (
#         "status",
#         "requested_at",
#     )

#     search_fields = (
#         "client__company_name",
#         "client__email",
#     )

#     actions = ["approve_requests", "reject_requests"]

#     def approve_requests(self, request, queryset):
#         queryset.update(status="approved")

#     approve_requests.short_description = "Approve selected client requests"

#     def reject_requests(self, request, queryset):
#         queryset.update(status="rejected")

#     reject_requests.short_description = "Reject selected client requests"


# @admin.register(ClientUser)
# class ClientUserAdmin(admin.ModelAdmin):
#     list_display = (
#         "id",
#         "user",
#         "client",
#         "role",
#         "is_active",
#     )

#     list_filter = (
#         "role",
#         "is_active",
#     )

#     search_fields = (
#         "user__username",
#         "user__email",
#         "client__company_name",
#     )



# @admin.register(ClientRequest)
# class ClientRequestAdmin(admin.ModelAdmin):
#     readonly_fields = (
#         "client",
#         "status",
#         "requested_at",
#     )

#     def has_add_permission(self, request):
#         return False



# def get_queryset(self, request):
#     qs = super().get_queryset(request)
#     if request.user.is_superuser:
#         return qs
#     return qs.none()
