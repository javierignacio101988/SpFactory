from django.db import models

# Create your models here.
class Marca(models.Model):
    nombre = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=30)
    precio = models.IntegerField()
    descripcion = models.TextField()
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    fecha_producto = models.DateField()
    imagen = models.ImageField(upload_to="productos", null=True)

    def __str__(self):
        return self.nombre

opciones_motivo = [
    [0, "felicitaciones"],
    [1, "reclamos"],
    [2, "sugerencias"],
    [3, "consultas"]

]

class Contacto(models.Model):
    nombre = models.CharField(max_length=60)
    correo = models.EmailField()
    motivo_consulta = models.IntegerField(choices=opciones_motivo)
    mensaje = models.TextField()

    def __str__(self):
        return self.nombre