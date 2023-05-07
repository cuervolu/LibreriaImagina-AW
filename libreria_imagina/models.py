from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.
class DetallePedido(models.Model):
    id_detalle_pedido = models.BigAutoField(primary_key=True, db_column='id_detalle_pedido', verbose_name='ID Detalle Pedido')
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE)
    libro = models.ForeignKey('Libro', on_delete=models.CASCADE)
    cantidad = models.IntegerField(null=False)
    precio_unitario = models.IntegerField(null=False)

    class Meta:
        db_table = 'detalle_pedido'
    
    def __str__(self):
        return str(self.id_detalle_pedido)


class Region(models.Model):
    id_region = models.IntegerField(primary_key=True, db_column='id_region', verbose_name='ID Region')
    nombre = models.CharField(max_length=50, null=False)
    numero_romano = models.CharField(max_length=10, null=False, verbose_name='Número romano')
    class Meta:
        db_table = 'region'
    
    def __str__(self):
        return self.nombre

class Comuna(models.Model):
    id_comuna = models.BigAutoField(primary_key=True, db_column='id_comuna', verbose_name='ID Comuna')
    nombre_comuna = models.CharField(max_length=50)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'comuna'
    
    def __str__(self):
        return self.nombre_comuna


    
class Direccion(models.Model):
    id_direccion = models.BigAutoField(primary_key=True, db_column='id_direccion', verbose_name='ID Direccion')
    direccion = models.CharField(max_length=100, null=True)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)

    class Meta:
        db_table = 'direccion'
    
    def __str__(self):
        return self.direccion
    
class Envio(models.Model):
    id_envio = models.BigAutoField(primary_key=True, db_column='id_envio', verbose_name='ID Envio')
    repartidor = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE)
    fecha_envio = models.DateField(blank=True, null=True)
    direccion = models.ForeignKey('Direccion', on_delete=models.CASCADE)
    class Meta:
        db_table = 'envio'
    
    def __str__(self):
        return self.id_envio
    
    def validate_repartidor(self):
        if self.repartidor.tipo_usuario != TipoUsuario.REPARTIDOR.value:
            raise ValidationError(
                _('El repartidor asignado debe ser de tipo "Repartidor".')
            )

    def clean(self):
        super().clean()
        self.validate_repartidor()


class EstadoMantenimiento(models.TextChoices):
    COMPLETADO = 'Completado'
    EN_PROCESO = 'En Proceso'
    CANCELADO = 'Cancelado'


class EstadoPedido(models.TextChoices):
    VALIDACION = 'Validación'
    PREPARACION = 'Preparación'
    REPARTO = 'Reparto'
    ENTREGADO = 'Entregado'
    CANCELADO = 'Cancelado'
    ESTADOPEDIDO_CHOICES = [
        (VALIDACION, 'Validación'),
        (PREPARACION, 'Preparación'),
        (REPARTO, 'Reparto'),
        (ENTREGADO, 'Entregado'),
        (CANCELADO, 'Cancelado'),
    ]
    estado = models.CharField(
        max_length=150,
        choices=ESTADOPEDIDO_CHOICES,
        default=VALIDACION,
    )

    def __str__(self):
        return self.estado


class Categoria(models.TextChoices):
    FICTION = "Fiction"
    GENERAL = "General"
    HISTORICAL = "Historical"
    SUSPENSE = "Suspense"
    THRILLERS = "Thrillers"
    COMPUTERS = "Computers"
    CATEGORIAS_CHOICES = [
        (FICTION, "Fiction"),
        (GENERAL, "General"),
        (HISTORICAL, "Historical"),
        (SUSPENSE, "Suspense"),
        (THRILLERS, "Thrillers"),
        (COMPUTERS, "Computers"),
    ]
    nombre = models.CharField(
        max_length=200,
        choices=CATEGORIAS_CHOICES,
        default=GENERAL,
    )

    def __str__(self):
        return self.nombre

class Libro(models.Model):
    id_libro = models.BigAutoField(primary_key=True, db_column='ID_LIBRO', verbose_name='ID Libro')
    nombre_libro = models.CharField(max_length=100, null=False)
    descripcion = models.TextField(null=False)
    autor = models.CharField(max_length=100, null=False)
    editorial = models.CharField(max_length=100, null=False)
    precio_unitario = models.BigIntegerField(null=False)
    cantidad_disponible = models.BigIntegerField(null=False)
    portada = models.CharField(max_length=255, null=False)
    fecha_publicacion = models.DateField(null=True)
    categoria = models.CharField(max_length=200, choices=Categoria.choices, default=Categoria.GENERAL)

    class Meta:
        db_table = 'libro'
        
    def __str__(self):
        return self.nombre_libro

class TipoMantenimiento(models.TextChoices):
    FISICO = 'Mantenimiento Físico'
    CONTENIDO = 'Contenido'
    PREVENTIVO = 'Preventivo'

class Mantenimiento(models.Model):
    id_mantenimiento = models.BigAutoField(primary_key=True, db_column='id_mantenimiento', verbose_name='ID Mantenimiento')
    cliente = models.ForeignKey('Usuario',on_delete=models.CASCADE, related_name='Cliente')
    tecnico = models.ForeignKey('Usuario',on_delete=models.CASCADE,related_name='Técnico')
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fecha_solicitud = models.DateField(null=False)
    tipo_mantenimiento = models.CharField(max_length=50, choices=TipoMantenimiento.choices, default=TipoMantenimiento.FISICO)
    estado_mantenimiento = models.CharField(max_length=50, choices=EstadoMantenimiento.choices, default=EstadoMantenimiento.EN_PROCESO)

    class Meta:
        db_table = 'mantenimiento'
    
    def __str__(self):
        return self.id_mantenimiento
    
    def validate_cliente(self):
        if self.cliente.tipo_usuario != TipoUsuario.CLIENTE.value:
            raise ValidationError(
                _('El usuario asignado debe ser de tipo "Cliente".')
            )
    def validate_tecnico(self):
        if self.tecnico.tipo_usuario != TipoUsuario.TECNICO.value:
            raise ValidationError(
                _('El usuario asignado debe ser de tipo "Técnico".')
            )

    def clean(self):
        super().clean()
        self.validate_cliente()
        self.validate_tecnico()


class Pedido(models.Model):
    id_pedido = models.BigAutoField(primary_key=True, db_column='id_pedido', verbose_name='ID Pedido')
    cliente = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    fecha_pedido = models.DateField(blank=True, null=True)
    fecha_entrega_estimada = models.DateField(blank=True, null=True)
    estado_pedido = models.CharField(max_length=150, choices=EstadoPedido.choices, default=EstadoPedido.VALIDACION)
    monto_total = models.BigIntegerField(null=False)

    class Meta:
        db_table = 'pedido'
        
    def __str__(self):
        return self.id_pedido
    
    def validate_cliente(self):
        if self.cliente.tipo_usuario != TipoUsuario.CLIENTE.value:
            raise ValidationError(
                _('El usuario asignado debe ser de tipo "Cliente".')
            )

    def clean(self):
        super().clean()
        self.validate_cliente()
class TipoUsuario(models.TextChoices):
    ADMIN = 'Admin'
    REPARTIDOR = 'Repartidor'
    TECNICO = 'Técnico'
    CLIENTE = 'Cliente'
    ENCARGADO_BODEGA = 'Encargado de Bodega'


class Transaccion(models.Model):
    id_transaccion = models.BigAutoField(primary_key=True, db_column='id_transaccion', verbose_name='ID Transaccion')
    pedido = models.ForeignKey(Pedido,on_delete=models.CASCADE)
    total_transaccion = models.BigIntegerField()

    class Meta:
        db_table = 'transaccion'
        
    def __str__(self):
        return self.id_transaccion


class UsuarioManager(BaseUserManager):
    def create_user(self, rut, nombre, apellido, username, correo, telefono, password=None, tipo_usuario=TipoUsuario.CLIENTE.value):
        if not rut:
            raise ValueError('El usuario debe tener un rut válido')

        usuario = self.model(
            rut=rut,
            nombre=nombre,
            apellido=apellido,
            username=username,
            correo=correo,
            telefono=telefono,
            tipo_usuario=tipo_usuario,
        )

        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, rut, nombre, apellido, username, correo, telefono, password, tipo_usuario=TipoUsuario.ADMIN.value):
        usuario = self.create_user(
            rut=rut,
            nombre=nombre,
            apellido=apellido,
            username=username,
            correo=correo,
            telefono=telefono,
            tipo_usuario=tipo_usuario,
            password=password,
        )

        usuario.is_superuser = True
        usuario.is_staff = True
        usuario.save(using=self._db)
        return usuario

class Usuario(AbstractBaseUser, PermissionsMixin):
    rut = models.CharField(unique=True, max_length=10)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    username = models.CharField(unique=True, max_length=30)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    direccion = models.ForeignKey(Direccion, on_delete=models.SET_NULL, null=True, blank=True)
    tipo_usuario = models.CharField(max_length=50, choices=TipoUsuario.choices, default=TipoUsuario.CLIENTE)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'rut'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'username', 'correo', 'telefono']

    objects = UsuarioManager()
    
    def save(self, *args, **kwargs):
        if self.direccion:
            # Si el usuario ha ingresado una dirección, crea una nueva dirección
            direccion = Direccion.objects.create(direccion=self.direccion.direccion, comuna=self.direccion.comuna)
            self.direccion = direccion
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre + ' ' + self.apellido

    def get_full_name(self):
        return self.nombre + ' ' + self.apellido

    def get_short_name(self):
        return self.nombre
    class Meta:
        db_table = 'usuario'
        
class Carrito(models.Model):
    id_carrito = models.BigAutoField(primary_key=True, db_column='ID_CARRITO', verbose_name='ID Carrito')
    libros = models.ManyToManyField(Libro)
    cantidad = models.IntegerField(default=0)
    total_pagar = models.IntegerField(default=0)
    usuario_rut = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'db_items_carrito'
    
    def __str__(self):
        return self.id_carrito
    
