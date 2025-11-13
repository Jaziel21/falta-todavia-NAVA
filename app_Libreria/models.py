# app_Libreria/models.py - VERSIÓN CON VALORES POR DEFECTO

from django.db import models
from django.utils import timezone

# ==========================================
# MODELO: EDITORIAL (ACTUALIZADO)
# ==========================================
class Editorial(models.Model):
    editorialid = models.AutoField(primary_key=True, verbose_name="ID Editorial")
    nombreeditorial = models.CharField(max_length=255, unique=True, verbose_name="Nombre de la editorial")
    direccion = models.CharField(max_length=255, verbose_name="Dirección", default="Sin dirección")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono", default="Sin teléfono")
    emailcontacto = models.EmailField(verbose_name="Email de contacto", default="sin@email.com")
    sitioweb = models.URLField(verbose_name="Sitio web", blank=True)
    paisorigen = models.CharField(max_length=50, verbose_name="País de origen", default="México")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Editorial"
        verbose_name_plural = "Editoriales"
        ordering = ['nombreeditorial']

    def __str__(self):
        return self.nombreeditorial

# ==========================================
# MODELO: AUTOR (ACTUALIZADO)
# ==========================================
class Autor(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID Autor")
    nombre = models.CharField(max_length=100, verbose_name="Nombre completo")
    nacionalidad = models.CharField(max_length=50, verbose_name="Nacionalidad", default="Desconocida")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento", default="1900-01-01")
    email = models.EmailField(verbose_name="Email de contacto", blank=True)
    activo = models.BooleanField(default=True, verbose_name="Autor activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

# ==========================================
# MODELO: LIBRO (ACTUALIZADO)
# ==========================================
class Libro(models.Model):
    GENEROS = [
        ('FIC', 'Ficción'),
        ('ROM', 'Romance'),
        ('TER', 'Terror'),
        ('CIE', 'Ciencia Ficción'),
        ('FAN', 'Fantasía'),
        ('HIS', 'Histórico'),
        ('BIO', 'Biografía'),
        ('INF', 'Infantil'),
    ]
    
    id = models.AutoField(primary_key=True, verbose_name="ID Libro")
    titulo = models.CharField(max_length=200, verbose_name="Título del libro")
    isbn = models.CharField(max_length=13, unique=True, verbose_name="ISBN")
    genero = models.CharField(max_length=3, choices=GENEROS, verbose_name="Género", default='FIC')
    precio = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Precio", default=0.00)
    stock = models.IntegerField(default=0, verbose_name="Cantidad en stock")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    
    # RELACIONES 1:MUCHOS
    autor = models.ForeignKey(
        Autor,
        on_delete=models.CASCADE,
        related_name='libros',
        verbose_name="Autor"
    )
    
    editorial = models.ForeignKey(
        Editorial,
        on_delete=models.CASCADE,
        related_name='libros',
        verbose_name="Editorial"
    )
    
    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libros"
        ordering = ['titulo']
    
    def __str__(self):
        return self.titulo
    
    def disponible(self):
        return self.stock > 0

# ==========================================
# MODELO: CLIENTE (ACTUALIZADO)
# ==========================================
class Cliente(models.Model):
    clienteid = models.AutoField(primary_key=True, verbose_name="ID Cliente")
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, verbose_name="Apellido", default="Sin Apellido")
    email = models.EmailField(unique=True, verbose_name="Email")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono", blank=True)
    direccion = models.CharField(max_length=255, verbose_name="Dirección", blank=True)
    fecharegistro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    preferenciasgenero = models.TextField(verbose_name="Preferencias de género", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# ==========================================
# MODELO: VENTA (ACTUALIZADO)
# ==========================================
class Venta(models.Model):
    ESTADOS = [
        ('PEN', 'Pendiente'),
        ('COM', 'Completada'),
        ('CAN', 'Cancelada'),
        ('DEV', 'Devuelta'),
    ]
    
    id = models.AutoField(primary_key=True, verbose_name="ID Venta")
    fecha_venta = models.DateTimeField(default=timezone.now, verbose_name="Fecha de venta")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total de la venta", default=0)
    estado = models.CharField(max_length=3, choices=ESTADOS, default='PEN', verbose_name="Estado de la venta")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    
    # RELACIONES 1:MUCHOS
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='ventas',
        verbose_name="Cliente"
    )
    
    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['-fecha_venta']
    
    def __str__(self):
        return f"Venta #{self.id} - {self.cliente.nombre}"
    
    def calcular_total(self):
        total = sum(detalle.subtotal for detalle in self.detalles.all())
        self.total = total
        self.save()
        return total

# ==========================================
# MODELO: DETALLE VENTA (ACTUALIZADO)
# ==========================================
class DetalleVenta(models.Model):
    detalleDeLaVentaid = models.AutoField(primary_key=True, verbose_name="ID Detalle Venta")
    cantidad = models.IntegerField(verbose_name="Cantidad", default=1)
    precioUnitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio unitario", default=0.00)
    iva = models.DecimalField(max_digits=5, decimal_places=2, default=16.00, verbose_name="IVA (%)")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Subtotal", default=0.00)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    
    # RELACIONES 1:MUCHOS
    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        related_name='detalles',
        verbose_name="Venta"
    )
    
    libro = models.ForeignKey(
        Libro,
        on_delete=models.PROTECT,
        related_name='detalles_venta',
        verbose_name="Libro"
    )
    
    class Meta:
        verbose_name = "Detalle de Venta"
        verbose_name_plural = "Detalles de Venta"

    def __str__(self):
        return f"Detalle #{self.detalleDeLaVentaid} - {self.libro.titulo}"
    
    def save(self, *args, **kwargs):
        # Calcular subtotal con IVA
        subtotal_sin_iva = self.cantidad * self.precioUnitario
        self.subtotal = subtotal_sin_iva * (1 + self.iva / 100)
        super().save(*args, **kwargs)
        # Actualizar total de la venta
        self.venta.calcular_total()