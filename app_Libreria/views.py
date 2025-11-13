# app_Libreria/views.py - REEMPLAZAR COMPLETAMENTE

from django.shortcuts import render, redirect, get_object_or_404
from .models import Autor, Editorial, Libro, Cliente, Venta, DetalleVenta
from django.utils import timezone

# ==========================================
# VISTAS PARA PÁGINA PRINCIPAL
# ==========================================

def inicio_libreria(request):
    contexto = {
        'titulo': 'Sistema de Administración Libreria AJMG 1194',
        'now': timezone.now()
    }
    return render(request, 'inicio.html', contexto)

# ==========================================
# VISTAS PARA MODELO AUTOR
# ==========================================

def agregar_autor(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        nacionalidad = request.POST.get('nacionalidad')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        email = request.POST.get('email')
        activo = True if request.POST.get('activo') == 'on' else False

        Autor.objects.create(
            nombre=nombre,
            nacionalidad=nacionalidad,
            fecha_nacimiento=fecha_nacimiento,
            email=email,
            activo=activo,
        )
        return redirect('ver_autores')

    return render(request, 'autor/agregar_autor.html')

def ver_autores(request):
    autores = Autor.objects.all()
    return render(request, 'autor/ver_autores.html', {'autores': autores})

def actualizar_autor(request, autor_id):
    autor = get_object_or_404(Autor, id=autor_id)
    return render(request, 'autor/actualizar_autor.html', {'autor': autor})

def realizar_actualizacion_autor(request, autor_id):
    autor = get_object_or_404(Autor, id=autor_id)
    if request.method == 'POST':
        autor.nombre = request.POST.get('nombre')
        autor.nacionalidad = request.POST.get('nacionalidad')
        autor.fecha_nacimiento = request.POST.get('fecha_nacimiento')
        autor.email = request.POST.get('email')
        autor.activo = True if request.POST.get('activo') == 'on' else False
        autor.save()
        return redirect('ver_autores')
    return redirect('actualizar_autor', autor_id=autor_id)

def borrar_autor(request, autor_id):
    autor = get_object_or_404(Autor, id=autor_id)
    if request.method == 'POST':
        autor.delete()
        return redirect('ver_autores')
    return render(request, 'autor/borrar_autor.html', {'autor': autor})

# ==========================================
# VISTAS PARA MODELO EDITORIAL (CORREGIDAS)
# ==========================================

def agregar_editorial(request):
    if request.method == 'POST':
        nombreeditorial = request.POST.get('nombreeditorial')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        emailcontacto = request.POST.get('emailcontacto')
        sitioweb = request.POST.get('sitioweb')
        paisorigen = request.POST.get('paisorigen')

        Editorial.objects.create(
            nombreeditorial=nombreeditorial,
            direccion=direccion,
            telefono=telefono,
            emailcontacto=emailcontacto,
            sitioweb=sitioweb,
            paisorigen=paisorigen,
        )
        return redirect('ver_editoriales')

    return render(request, 'editorial/agregar_editorial.html')

def ver_editoriales(request):
    editoriales = Editorial.objects.all()
    return render(request, 'editorial/ver_editoriales.html', {'editoriales': editoriales})

def actualizar_editorial(request, editorial_id):
    editorial = get_object_or_404(Editorial, editorialid=editorial_id)
    return render(request, 'editorial/actualizar_editorial.html', {'editorial': editorial})

def realizar_actualizacion_editorial(request, editorial_id):
    editorial = get_object_or_404(Editorial, editorialid=editorial_id)
    if request.method == 'POST':
        editorial.nombreeditorial = request.POST.get('nombreeditorial')
        editorial.direccion = request.POST.get('direccion')
        editorial.telefono = request.POST.get('telefono')
        editorial.emailcontacto = request.POST.get('emailcontacto')
        editorial.sitioweb = request.POST.get('sitioweb')
        editorial.paisorigen = request.POST.get('paisorigen')
        editorial.save()
        return redirect('ver_editoriales')
    return redirect('actualizar_editorial', editorial_id=editorial_id)

def borrar_editorial(request, editorial_id):
    editorial = get_object_or_404(Editorial, editorialid=editorial_id)
    if request.method == 'POST':
        editorial.delete()
        return redirect('ver_editoriales')
    return render(request, 'editorial/borrar_editorial.html', {'editorial': editorial})

# ==========================================
# VISTAS PARA MODELO LIBRO
# ==========================================

def agregar_libro(request):
    if request.method == 'POST':
        try:
            titulo = request.POST.get('titulo')
            isbn = request.POST.get('isbn')
            genero = request.POST.get('genero')
            precio = request.POST.get('precio')
            stock = request.POST.get('stock')
            editorial_id = request.POST.get('editorial')
            autor_id = request.POST.get('autor')
            
            # CORREGIDO: Usar editorialid para buscar la editorial
            editorial = Editorial.objects.get(editorialid=editorial_id)
            autor = Autor.objects.get(id=autor_id)
            
            libro = Libro.objects.create(
                titulo=titulo,
                isbn=isbn,
                genero=genero,
                precio=precio,
                stock=stock,
                editorial=editorial,
                autor=autor
            )
            
            return redirect('ver_libros')
            
        except Exception as e:
            autores = Autor.objects.filter(activo=True)
            editoriales = Editorial.objects.all()  # CORREGIDO: Obtener todas las editoriales
            generos = Libro.GENEROS
            return render(request, 'libro/agregar_libro.html', {
                'autores': autores,
                'editoriales': editoriales,  # CORREGIDO: Pasar editoriales al template
                'generos': generos,
                'error': f'Error al crear el libro: {str(e)}'
            })
    
    # GET request - mostrar formulario
    autores = Autor.objects.filter(activo=True)
    editoriales = Editorial.objects.all()  # CORREGIDO: Obtener todas las editoriales
    generos = Libro.GENEROS
    return render(request, 'libro/agregar_libro.html', {
        'autores': autores,
        'editoriales': editoriales,  # CORREGIDO: Pasar editoriales al template
        'generos': generos
    })
def ver_libros(request):
    libros = Libro.objects.all().select_related('autor', 'editorial')
    return render(request, 'libro/ver_libros.html', {'libros': libros})

def actualizar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    autores = Autor.objects.filter(activo=True)
    editoriales = Editorial.objects.all()
    generos = Libro.GENEROS
    
    return render(request, 'libro/actualizar_libro.html', {
        'libro': libro,
        'autores': autores,
        'editoriales': editoriales,
        'generos': generos
    })

def realizar_actualizacion_libro(request, libro_id):
    if request.method == 'POST':
        try:
            libro = get_object_or_404(Libro, id=libro_id)
            
            libro.titulo = request.POST.get('titulo')
            libro.isbn = request.POST.get('isbn')
            libro.genero = request.POST.get('genero')
            libro.precio = request.POST.get('precio')
            libro.stock = request.POST.get('stock')
            
            editorial_id = request.POST.get('editorial')
            autor_id = request.POST.get('autor')
            
            # CORREGIDO: Usar editorialid para buscar la editorial
            libro.editorial = Editorial.objects.get(editorialid=editorial_id)
            libro.autor = Autor.objects.get(id=autor_id)
            
            libro.save()
            
            return redirect('ver_libros')
            
        except Exception as e:
            libro = get_object_or_404(Libro, id=libro_id)
            autores = Autor.objects.filter(activo=True)
            editoriales = Editorial.objects.all()  # CORREGIDO: Obtener todas las editoriales
            generos = Libro.GENEROS
            return render(request, 'libro/actualizar_libro.html', {
                'libro': libro,
                'autores': autores,
                'editoriales': editoriales,  # CORREGIDO: Pasar editoriales al template
                'generos': generos,
                'error': f'Error al actualizar: {str(e)}'
            })
    
    return redirect('actualizar_libro', libro_id=libro_id)

def borrar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    
    if request.method == 'POST':
        libro.delete()
        return redirect('ver_libros')
    
    return render(request, 'libro/borrar_libro.html', {'libro': libro})

# ==========================================
# VISTAS PARA MODELO CLIENTE (ACTUALIZADAS)
# ==========================================

def agregar_cliente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        preferenciasgenero = request.POST.get('preferenciasgenero')

        Cliente.objects.create(
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            direccion=direccion,
            preferenciasgenero=preferenciasgenero,
        )
        return redirect('ver_clientes')

    return render(request, 'cliente/agregar_cliente.html')

def ver_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'cliente/ver_clientes.html', {'clientes': clientes})

def actualizar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, clienteid=cliente_id)
    return render(request, 'cliente/actualizar_cliente.html', {'cliente': cliente})

def realizar_actualizacion_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, clienteid=cliente_id)
    if request.method == 'POST':
        cliente.nombre = request.POST.get('nombre')
        cliente.apellido = request.POST.get('apellido')
        cliente.email = request.POST.get('email')
        cliente.telefono = request.POST.get('telefono')
        cliente.direccion = request.POST.get('direccion')
        cliente.preferenciasgenero = request.POST.get('preferenciasgenero')
        cliente.save()
        return redirect('ver_clientes')
    return redirect('actualizar_cliente', cliente_id=cliente_id)

def borrar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, clienteid=cliente_id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('ver_clientes')
    return render(request, 'cliente/borrar_cliente.html', {'cliente': cliente})

# ==========================================
# VISTAS PARA MODELO VENTA
# ==========================================

def agregar_venta(request):
    if request.method == 'POST':
        try:
            cliente_id = request.POST.get('cliente')
            estado = request.POST.get('estado')
            
            cliente = Cliente.objects.get(clienteid=cliente_id)
            
            venta = Venta.objects.create(
                cliente=cliente,
                estado=estado
            )
            
            return redirect('ver_ventas')
            
        except Exception as e:
            clientes = Cliente.objects.all()
            return render(request, 'venta/agregar_venta.html', {
                'clientes': clientes,
                'error': f'Error al crear la venta: {str(e)}'
            })
    
    clientes = Cliente.objects.all()
    return render(request, 'venta/agregar_venta.html', {
        'clientes': clientes
    })

def ver_ventas(request):
    ventas = Venta.objects.all().select_related('cliente')
    return render(request, 'venta/ver_ventas.html', {'ventas': ventas})

def actualizar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    clientes = Cliente.objects.all()
    
    return render(request, 'venta/actualizar_venta.html', {
        'venta': venta,
        'clientes': clientes
    })

def realizar_actualizacion_venta(request, venta_id):
    if request.method == 'POST':
        try:
            venta = get_object_or_404(Venta, id=venta_id)
            
            cliente_id = request.POST.get('cliente')
            estado = request.POST.get('estado')
            
            cliente = Cliente.objects.get(clienteid=cliente_id)
            
            venta.cliente = cliente
            venta.estado = estado
            venta.save()
            
            return redirect('ver_ventas')
            
        except Exception as e:
            venta = get_object_or_404(Venta, id=venta_id)
            clientes = Cliente.objects.all()
            return render(request, 'venta/actualizar_venta.html', {
                'venta': venta,
                'clientes': clientes,
                'error': f'Error al actualizar la venta: {str(e)}'
            })
    
    return redirect('actualizar_venta', venta_id=venta_id)

def borrar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    
    if request.method == 'POST':
        venta.delete()
        return redirect('ver_ventas')
    
    return render(request, 'venta/borrar_venta.html', {'venta': venta})

# ==========================================
# VISTAS PARA DETALLES VENTA (ACTUALIZADAS CON IVA)
# ==========================================

def ver_detalles_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    detalles = venta.detalles.all().select_related('libro')
    return render(request, 'detalle_venta/ver_detalles.html', {
        'venta': venta,
        'detalles': detalles
    })

def agregar_detalle_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    
    if request.method == 'POST':
        try:
            libro_id = request.POST.get('libro')
            cantidad = int(request.POST.get('cantidad'))
            precioUnitario = float(request.POST.get('precioUnitario'))
            iva = float(request.POST.get('iva', 16.00))
            
            libro = Libro.objects.get(id=libro_id)
            
            # Verificar stock disponible
            if libro.stock < cantidad:
                libros = Libro.objects.filter(stock__gt=0)
                return render(request, 'detalle_venta/agregar_detalle.html', {
                    'venta': venta,
                    'libros': libros,
                    'error': f'Stock insuficiente. Solo hay {libro.stock} unidades disponibles.'
                })
            
            # Crear el detalle de venta con IVA
            detalle = DetalleVenta.objects.create(
                venta=venta,
                libro=libro,
                cantidad=cantidad,
                precioUnitario=precioUnitario,
                iva=iva
            )
            
            # Actualizar stock del libro
            libro.stock -= cantidad
            libro.save()
            
            # Recalcular total de la venta
            venta.calcular_total()
            
            return redirect('ver_detalles_venta', venta_id=venta.id)
            
        except Exception as e:
            libros = Libro.objects.filter(stock__gt=0)
            return render(request, 'detalle_venta/agregar_detalle.html', {
                'venta': venta,
                'libros': libros,
                'error': f'Error al agregar detalle: {str(e)}'
            })
    
    libros = Libro.objects.filter(stock__gt=0)
    return render(request, 'detalle_venta/agregar_detalle.html', {
        'venta': venta,
        'libros': libros
    })

def actualizar_detalle_venta(request, detalle_id):
    detalle = get_object_or_404(DetalleVenta, detalleDeLaVentaid=detalle_id)
    libros = Libro.objects.all()
    
    return render(request, 'detalle_venta/actualizar_detalle.html', {
        'detalle': detalle,
        'libros': libros
    })

def realizar_actualizacion_detalle_venta(request, detalle_id):
    if request.method == 'POST':
        try:
            detalle = get_object_or_404(DetalleVenta, detalleDeLaVentaid=detalle_id)
            libro_anterior = detalle.libro
            cantidad_anterior = detalle.cantidad
            
            # Obtener nuevos valores
            libro_id = request.POST.get('libro')
            cantidad = int(request.POST.get('cantidad'))
            precioUnitario = float(request.POST.get('precioUnitario'))
            iva = float(request.POST.get('iva', 16.00))
            
            libro_nuevo = Libro.objects.get(id=libro_id)
            
            # Manejar cambios en libro y cantidad
            if libro_anterior != libro_nuevo or cantidad != cantidad_anterior:
                # Restaurar stock del libro anterior
                libro_anterior.stock += cantidad_anterior
                libro_anterior.save()
                
                # Verificar stock del nuevo libro
                if libro_nuevo.stock < cantidad:
                    libros = Libro.objects.all()
                    return render(request, 'detalle_venta/actualizar_detalle.html', {
                        'detalle': detalle,
                        'libros': libros,
                        'error': f'Stock insuficiente. Solo hay {libro_nuevo.stock} unidades disponibles.'
                    })
                
                # Actualizar stock del nuevo libro
                libro_nuevo.stock -= cantidad
                libro_nuevo.save()
            
            # Actualizar el detalle con IVA
            detalle.libro = libro_nuevo
            detalle.cantidad = cantidad
            detalle.precioUnitario = precioUnitario
            detalle.iva = iva
            detalle.save()
            
            # Recalcular total de la venta
            detalle.venta.calcular_total()
            
            return redirect('ver_detalles_venta', venta_id=detalle.venta.id)
            
        except Exception as e:
            detalle = get_object_or_404(DetalleVenta, detalleDeLaVentaid=detalle_id)
            libros = Libro.objects.all()
            return render(request, 'detalle_venta/actualizar_detalle.html', {
                'detalle': detalle,
                'libros': libros,
                'error': f'Error al actualizar detalle: {str(e)}'
            })
    
    return redirect('actualizar_detalle_venta', detalle_id=detalle_id)

def borrar_detalle_venta(request, detalle_id):
    detalle = get_object_or_404(DetalleVenta, detalleDeLaVentaid=detalle_id)
    venta_id = detalle.venta.id
    
    if request.method == 'POST':
        # Restaurar stock antes de eliminar
        libro = detalle.libro
        libro.stock += detalle.cantidad
        libro.save()
        
        # Eliminar detalle
        detalle.delete()
        
        # Recalcular total de la venta
        detalle.venta.calcular_total()
        
        return redirect('ver_detalles_venta', venta_id=venta_id)
    
    return render(request, 'detalle_venta/borrar_detalle.html', {'detalle': detalle})