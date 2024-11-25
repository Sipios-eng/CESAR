from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('evolucion/result1/', views.evolucion_fsr_result1, name='evolucion_fsr_result1'),
    path('evolucion/result2/', views.evolucion_fsr_result2, name='evolucion_fsr_result2'),
    path('iniciar_sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('generar_reporte/', views.generar_reporte, name='generar_reporte'),
    path('generar_reporte_fsr/', views.generar_reporte_fsr, name='generar_reporte_fsr'),
    path('registrar/', views.registrar, name='registrar'),
    path('efecto_domino/', views.efecto_domino_view, name='efecto_domino'),
]
