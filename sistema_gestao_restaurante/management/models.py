from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TaxModel(models.Model):
    __name__='taxes'

    name = models.CharField(null=False, max_length=100)
    description = models.TextField()
    percentage = models.IntegerField(default=0)
    saved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        permissions = [
            ("view_tax", "Pode visualizar imposto"),
            ("change_tax", "Pode criar/editar imposto"),
            ("delete_tax", "Pode eliminar imposto"),
        ]

    def __str__(self):
        return self.name

class CategoryModel(models.Model):
    __name__='categories'

    name = models.CharField(null=False, max_length=150)
    description = models.TextField()
    saved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        permissions = [
            ("view_category", "Pode visualizar categoria"),
            ("change_category", "Pode criar/editar categoria"),
            ("delete_category", "Pode eliminar categoria"),
        ]

    def __str__(self):
        return self.name

class ProductModel(models.Model):
    __name__='products'

    name = models.CharField(null=False, max_length=50)
    code = models.CharField(null=False, max_length=50)
    price = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    description = models.TextField()
    tax_id = models.ForeignKey(TaxModel, on_delete=models.CASCADE)
    category_id = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    arquivo = models.ImageField(upload_to='arquivos/', null=True, blank=True)
    saved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        permissions = [
            ("view_product", "Pode visualizar producto"),
            ("change_product", "Pode criar/editar producto"),
            ("delete_product", "Pode eliminar producto"),
        ]

    def __str__(self):
        return self.name

class ReserveModel(models.Model):
    __name__='products'

    name = models.CharField(null=False, max_length=50)
    phone_number = models.CharField(null=False, max_length=50)
    email = models.CharField(null=False, max_length=50)
    how_many_number = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    date = models.DateField(auto_created=True)

    class Meta:
        permissions = [
            ("view_reserve", "Pode visualizar reserva"),
            ("change_reserve", "Pode criar/editar reserva"),
            ("delete_reserve", "Pode eliminar reserva"),
        ]

    def __str__(self):
        return self.name

class PaymentMethodModel(models.Model):
    __name__='payment_method'

    name = models.CharField(null=False, max_length=100)
    description = models.TextField()
    use_bank = models.BooleanField(default=False, null=False)
    is_active = models.BooleanField(default=True, null=False)
    saved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        permissions = [
            ("view_payment_method", "Pode visualizar metodo de pagamento"),
            ("change_payment_method", "Pode criar/editar metodo de pagamento"),
            ("delete_payment_method", "Pode eliminar metodo de pagamento"),
        ]

    def __str__(self):
        return self.name

class PaymentModel(models.Model):
    __name__='payment_method'

    amount_received = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    change = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    total_paid = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=True, null=False)
    saved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        permissions = [
            ("view_payment", "Pode visualizar pagamento"),
            ("change_payment", "Pode criar/editar pagamento"),
            ("delete_payment", "Pode eliminar pagamento"),
        ]

    def __str__(self):
        return self.name

class PaymentlineModel(models.Model):
    __name__='payment_line_method'

    amount_received = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    payment = models.ForeignKey(PaymentModel, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethodModel, on_delete=models.CASCADE)
    saved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        permissions = [
            ("view_payment_line", "Pode visualizar linha de pagamento"),
            ("change_payment_line", "Pode criar/editar linha de pagamento"),
            ("delete_payment_line", "Pode eliminar linha de pagamento"),
        ]

    def __str__(self):
        return self.name
