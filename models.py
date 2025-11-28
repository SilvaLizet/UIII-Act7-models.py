from django.db import models

class GeneroLiterario(models.Model):
    id_genero = models.AutoField(primary_key=True)
    nombre_genero = models.CharField(max_length=50)
    descripcion = models.TextField()
    es_ficcion = models.BooleanField(default=False)
    epoca_popular = models.CharField(max_length=50)
    publico_objetivo = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Género Literario"
        verbose_name_plural = "Géneros Literarios"

    def __str__(self):
        return self.nombre_genero


class AutorEditorial(models.Model):
    id_autor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    biografia = models.TextField()
    email = models.EmailField(max_length=100)
    sitio_web = models.URLField(max_length=255, null=True, blank=True)
    fecha_fallecimiento = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Editor(models.Model):
    id_editor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=20)
    fecha_contratacion = models.DateField()
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    especialidad_genero = models.CharField(max_length=100)
    departamento = models.CharField(max_length=50)
    dni = models.CharField(max_length=20, unique=True)

    class Meta:
        verbose_name = "Editor"
        verbose_name_plural = "Editores"

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Distribuidor(models.Model):
    id_distribuidor = models.AutoField(primary_key=True)
    nombre_distribuidor = models.CharField(max_length=100)
    contacto_principal = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    direccion_almacen = models.CharField(max_length=255)
    pais_distribucion = models.CharField(max_length=50)
    tipo_distribucion = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Distribuidor"
        verbose_name_plural = "Distribuidores"

    def __str__(self):
        return self.nombre_distribuidor


class LibroEditorial(models.Model):
    id_libro = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    # Relación Muchos a Uno con Autor
    autor_principal = models.ForeignKey(AutorEditorial, on_delete=models.CASCADE, related_name='libros')
    isbn = models.CharField(max_length=13, unique=True)
    fecha_publicacion = models.DateField()
    num_paginas = models.IntegerField()
    # Relación Muchos a Uno con Genero
    genero = models.ForeignKey(GeneroLiterario, on_delete=models.SET_NULL, null=True, related_name='libros')
    precio_tapa = models.DecimalField(max_digits=10, decimal_places=2)
    stock_almacen = models.IntegerField(default=0)
    # Relación Muchos a Uno con Editor
    editor = models.ForeignKey(Editor, on_delete=models.SET_NULL, null=True, related_name='libros_editados')
    estado_publicacion = models.CharField(max_length=50) # Sugerencia: Usar choices en el futuro
    formato = models.CharField(max_length=50) # Ej: Tapa dura, digital, etc.

    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libros"

    def __str__(self):
        return self.titulo


class ContratoAutor(models.Model):
    id_contrato = models.AutoField(primary_key=True)
    # Relación Muchos a Uno con Libro
    libro = models.ForeignKey(LibroEditorial, on_delete=models.CASCADE, related_name='contratos')
    # Relación Muchos a Uno con Autor
    autor_principal = models.ForeignKey(AutorEditorial, on_delete=models.CASCADE, related_name='contratos')
    fecha_firma = models.DateField()
    porcentaje_regalias = models.DecimalField(max_digits=5, decimal_places=2)
    monto_adelanto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_fin_contrato = models.DateField()
    clausulas_especiales = models.TextField(null=True, blank=True)
    # Nota: No se proporcionó tabla de Agente Literario, se deja como IntegerField
    # Si existiera la tabla, sería un ForeignKey.
    id_agente_literario = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Contrato de Autor"
        verbose_name_plural = "Contratos de Autores"

    def __str__(self):
        return f"Contrato {self.id_contrato} - {self.libro.titulo}"


class EnvioLibros(models.Model):
    id_envio = models.AutoField(primary_key=True)
    # Relación Muchos a Uno con Libro
    libro = models.ForeignKey(LibroEditorial, on_delete=models.CASCADE, related_name='envios')
    # Relación Muchos a Uno con Distribuidor
    distribuidor = models.ForeignKey(Distribuidor, on_delete=models.CASCADE, related_name='envios')
    fecha_envio = models.DateTimeField()
    cantidad_enviada = models.IntegerField()
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2)
    estado_envio = models.CharField(max_length=50) # Ej: En tránsito, Entregado
    fecha_recepcion_esperada = models.DateField(null=True, blank=True)
    numero_seguimiento = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = "Envío de Libros"
        verbose_name_plural = "Envíos de Libros"

    def __str__(self):
        return f"Envío #{self.id_envio} - {self.distribuidor.nombre_distribuidor}"
