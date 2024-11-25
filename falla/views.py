from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegistroUsuarioForm
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt
import random
from datetime import datetime, timedelta
import io

# Vista para generar un reporte de sismos
@login_required
def generar_reporte(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_sismos.pdf"'

    # Crear el documento PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Título del reporte
    elements.append(Paragraph("Reporte de Sismos", styles['Title']))
    elements.append(Spacer(1, 12))

    # Generar datos ficticios de sismos
    data = [["ID", "Fecha", "Magnitud"]]
    sismos = []
    for i in range(10):
        sismo_id = i + 1
        magnitud = round(random.uniform(4.0, 7.5), 1)
        fecha = datetime.now() - timedelta(days=random.randint(0, 365))
        fecha_str = fecha.strftime("%Y-%m-%d %H:%M:%S")
        data.append([sismo_id, fecha_str, magnitud])
        sismos.append((fecha, magnitud))

    # Tabla de datos de sismos
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))

    # Generar gráfico de magnitudes de sismos
    fechas = [sismo[0] for sismo in sismos]
    magnitudes = [sismo[1] for sismo in sismos]

    plt.figure(figsize=(10, 5))
    plt.plot(fechas, magnitudes, marker='o', linestyle='-', color='b')
    plt.xlabel('Fecha')
    plt.ylabel('Magnitud')
    plt.title('Magnitud de Sismos en el Tiempo')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Guardar el gráfico en un buffer y agregarlo al PDF como una imagen
    graph_buffer = io.BytesIO()
    plt.savefig(graph_buffer, format='png')
    graph_buffer.seek(0)
    plt.close()
    img = Image(graph_buffer)
    img.drawHeight = 4 * 72
    img.drawWidth = 6 * 72
    elements.append(Spacer(1, 12))

    # Añadir gráfico al PDF
    elements.append(Paragraph("Gráfico de Magnitud de Sismos", styles['Heading2']))
    elements.append(Spacer(1, 12))
    elements.append(img)

    # Construir el PDF
    doc.build(elements)
    response.write(buffer.getvalue())
    buffer.close()

    return response

# Vista para generar un reporte PDF de la evolución de apertura de la F.S.R
@login_required
def generar_reporte_fsr(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_fsr.pdf"'

    # Crear el documento PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Título del reporte
    elements.append(Paragraph("Reporte de Evolución de Apertura de la F.S.R", styles['Title']))
    elements.append(Spacer(1, 12))

    # Generar datos ficticios de la evolución de apertura
    data = [["Fecha", "Apertura (cm)"]]
    aperturas = []
    for i in range(10):
        apertura = round(random.uniform(0.5, 2.0), 2)
        fecha = datetime.now() - timedelta(days=random.randint(0, 365))
        fecha_str = fecha.strftime("%Y-%m-%d %H:%M:%S")
        data.append([fecha_str, apertura])
        aperturas.append((fecha, apertura))

    # Tabla de datos de apertura
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))

    # Generar gráfico de evolución de apertura
    fechas = [apertura[0] for apertura in aperturas]
    valores_apertura = [apertura[1] for apertura in aperturas]

    plt.figure(figsize=(10, 5))
    plt.plot(fechas, valores_apertura, marker='o', linestyle='-', color='r')
    plt.xlabel('Fecha')
    plt.ylabel('Apertura (cm)')
    plt.title('Evolución de Apertura de la F.S.R')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Guardar el gráfico en un buffer y agregarlo al PDF como una imagen
    graph_buffer = io.BytesIO()
    plt.savefig(graph_buffer, format='png')
    graph_buffer.seek(0)
    plt.close()
    img = Image(graph_buffer)
    img.drawHeight = 4 * 72
    img.drawWidth = 6 * 72
    elements.append(Spacer(1, 12))

    # Añadir gráfico al PDF
    elements.append(Paragraph("Gráfico de Evolución de Apertura", styles['Heading2']))
    elements.append(Spacer(1, 12))
    elements.append(img)

    # Construir el PDF
    doc.build(elements)
    response.write(buffer.getvalue())
    buffer.close()

    return response


# Vista para el registro de usuarios
def registrar(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('iniciar_sesion')
        else:
            return render(request, 'registro.html', {'form': form})
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registro.html', {'form': form})

# Vista para iniciar sesión
def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Vista para cerrar sesión
def cerrar_sesion(request):
    logout(request)
    return redirect('index')

# Vista para la página principal
def index(request):
    return render(request, 'index.html')


# Vista para analizar la evolución de apertura de la F.S.R
#@login_required
def evolucion_fsr_result1(request):
    if request.method == "POST":
        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_fin = request.POST.get("fecha_fin")

        if not fecha_inicio or not fecha_fin:
            return redirect('index')

        try:
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
        except ValueError:
            return redirect('index')

        if fecha_inicio > fecha_fin:
            return redirect('index')

        dias = (fecha_fin - fecha_inicio).days + 1
        evolucion_datos = []
        apertura_actual = round(random.uniform(0.5, 2.0), 2)

        for _ in range(dias):
            variacion = round(random.uniform(-0.1, 0.1), 2)
            apertura_actual = max(0.0, round(apertura_actual + variacion, 2))
            evolucion_datos.append(apertura_actual)

        fechas = [(fecha_inicio + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(dias)]
        evolucion = list(zip(fechas, evolucion_datos))

        context = {
            "evolucion": evolucion,
            "fecha_inicio": fecha_inicio.strftime("%Y-%m-%d"),
            "fecha_fin": fecha_fin.strftime("%Y-%m-%d"),
        }
        return render(request, "evolucion_fsr_result1.html", context)

    # Manejo del método GET para cargar la página inicial
    return render(request, "evolucion_fsr_result1.html")



# Vista para mostrar los resultados de la evolución de la F.S.R
#@login_required
def evolucion_fsr_result2(request):
    return render(request, 'evolucion_fsr_result2.html')
    

import random
from django.shortcuts import render

def efecto_domino_view(request):
    # Datos ficticios para simular los sismos
    lugares = ["Santiago", "Valparaíso", "Concepción", "La Serena", "Antofagasta"]
    sismos = []

    for _ in range(3):  # Generar datos para tres sismos
        sismo = {
            "lugar": random.choice(lugares),
            "fecha": f"{random.randint(1, 28)}/11/2024",
            "hora": f"{random.randint(0, 23)}:{random.randint(0, 59):02d}",
            "magnitud": round(random.uniform(5.0, 8.0), 1),
            "profundidad": random.randint(5, 50),  # en kilómetros
            "probabilidad_efecto_domino": round(random.uniform(0.1, 1.0), 2)  # probabilidad de desencadenar otro sismo
        }
        sismos.append(sismo)

    # Enviar los datos a la plantilla
    context = {
        'sismos': sismos,
    }
    return render(request, 'efecto_domino.html', context)
    