from django.db import models
from django.contrib.auth.models import User
from management.models import ProductModel

# Create your models here.
class InvoiceModel(models.Model):
    number = models.CharField(max_length=20, unique=True)
    created_at = models.DateField(auto_created=True)
    description = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    total_tax = models.DecimalField(max_digits=10, decimal_places=2)
    total_without_tax = models.DecimalField(max_digits=10, decimal_places=2)
    saved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    class Meta:
        permissions = [
            ("view_invoice", "Pode visualizar factura"),
            ("change_invoice", "Pode criar/editar factura"),
            ("delete_invoice", "Pode eliminar factura"),
        ]

    def __str__(self):
        return self.number

class InvoiceLineModel(models.Model):
    invoice = models.ForeignKey(InvoiceModel, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()