from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.
class PositionModel(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    description = models.TextField()

    class Meta:
        permissions = [
            ("view_position", "Pode visualizar Cargo/Função"),
            ("change_position", "Pode criar/editar Cargo/Função"),
            ("delete_position", "Pode eliminar Cargo/Função"),
        ]
    
    def __str__(self):
        return self.group.name

class EmployeeModel(models.Model):
    __name__='employeers'

    name = models.CharField(null=False, max_length=50)
    salary = models.DecimalField(null=False, default=25000, decimal_places=2, max_digits=12)
    email = models.CharField(null=True, max_length=100)
    description = models.TextField()
    status = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    position = models.ForeignKey(PositionModel, on_delete=models.SET_NULL, null=True)

    class Meta:
        permissions = [
            ("view_employee", "Pode visualizar Funcionário"),
            ("change_employee", "Pode criar/editar Funcionário"),
            ("delete_employee", "Pode eliminar Funcionário"),
        ]

    def __str__(self):
        return self.name