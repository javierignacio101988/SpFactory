from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import ContactoForm, ProductoForm, RegistrarFrom
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import permission_required
from rest_framework import viewsets
from .serializers import ProductoSerializer

class ProductoViewset(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    def get_queryset(self):
        productos = Producto.objects.all()
        nombre = self.request.GET.get('nombre')

        if nombre:
            productos = productos.filter(nombre__contains=nombre)

        return productos


def home(request):
    productos = Producto.objects.all()
    data = {
        'productos': productos
    }
    return render(request, 'app/home.html', data)

def contacto(request):
    data = {
        'form': ContactoForm()
    }
    if request.method == 'POST':
        formulario = ContactoForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Contacto agregado correctamente")
            #data["mensaje"] = "Contacto agregado"
        else:
            data["form"] = formulario
    return render(request,'app/contacto.html', data)

def galeria (request):
    return render(request, 'app/galeria.html')

@permission_required('app.add_producto')
def agregar_producto(request):

    data = {
        'form': ProductoForm()
    }
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Producto agregado correctamente")
            #data["mensaje"] = "Producto agregado correctamente"
            return redirect(to="listar_productos")
        else:
            messages.ERROR(request,"No se ha podido agregar el producto")
            data["form"] = formulario

    return render(request, 'app/producto/agregar.html', data)

@permission_required('app.view_producto')
def listar_productos(request):
    productos = Producto.objects.all()
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(productos, 3)
        productos = paginator.page(page)
    except:
        raise Http404
    data ={

        'entity': productos,
        'paginator': paginator

    }
    return render(request, 'app/producto/listar.html', data)

@permission_required('app.change_producto')
def modificar_producto(request, id):

    producto = get_object_or_404(Producto, id=id)

    data = {
        'form': ProductoForm(instance=producto)
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid:
            formulario.save()
            messages.success(request,"Producto modificado correctamente")
            return redirect(to="listar_productos")
        data["form"] = formulario

    return render(request, 'app/producto/modificar.html', data)

@permission_required('app.delete_producto')
def eliminar_producto(request, id):
    producto= get_object_or_404(Producto, id=id)
    producto.delete()
    messages.success(request, "Producto eliminado correctamente")
    return redirect(to="listar_productos")

def registro(request):

    data = {
        'form': RegistrarFrom()
    }
    if request.method == 'POST':
        formulario = RegistrarFrom(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Te has registrado correctamente")
            return redirect(to="home")
        data["form"] = formulario
    return render(request, 'registration/registro.html', data)