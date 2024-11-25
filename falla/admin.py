from django.contrib import admin
from django.db import IntegrityError, transaction
from django.db.models import ProtectedError
from django.db import DatabaseError
from django.core.exceptions import ValidationError
from .models import Rol, Usuario, UsuarioExtendido, EstacionSismografica, Sensor, EventoSismico, Reporte, Alerta


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'rol')
    list_filter = ('rol',)
    search_fields = ('username', 'email')
    
    def save_model(self, request, obj, form, change):
        try:
            with transaction.atomic():
                obj.full_clean()  # Validate before saving
                super().save_model(request, obj, form, change)
        except ValidationError as e:
            self.message_user(request, f"Error de validación: {e}", level='error')
        except IntegrityError:
            self.message_user(request, "No se pudo actualizar el registro debido a problemas de integridad referencial.", level='error')
        except ProtectedError:
            self.message_user(request, "No se pudo eliminar el registro porque está protegido por otras dependencias.", level='error')
        except DatabaseError:
            self.message_user(request, "Ocurrió un error con la base de datos. Por favor, inténtelo de nuevo.", level='error')

    def delete_model(self, request, obj):
        try:
            with transaction.atomic():
                super().delete_model(request, obj)
        except ProtectedError:
            self.message_user(request, "No se pudo eliminar el registro porque está protegido por otras dependencias.", level='error')
        except IntegrityError:
            self.message_user(request, "No se pudo eliminar el registro debido a problemas de integridad referencial.", level='error')
        except DatabaseError:
            self.message_user(request, "Ocurrió un error con la base de datos al intentar eliminar el registro. Por favor, inténtelo de nuevo.", level='error')


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Rol)
admin.site.register(UsuarioExtendido)
admin.site.register(EstacionSismografica)
admin.site.register(Sensor)
admin.site.register(EventoSismico)
admin.site.register(Reporte)
admin.site.register(Alerta)
