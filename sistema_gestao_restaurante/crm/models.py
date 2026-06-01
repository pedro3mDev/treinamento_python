from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CustomerModel(models.Model):
    __name__='customers'

    name = models.CharField(null=False, max_length=50)
    nif = models.CharField(null=False, max_length=14)
    phone_number = models.CharField(null=True, max_length=20)
    address = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        permissions = [
            ("view_customer", "Pode visualizar cliente"),
            ("change_customer", "Pode criar/editar cliente"),
            ("delete_customer", "Pode eliminar cliente"),
        ]

    def __str__(self):
        return self.name