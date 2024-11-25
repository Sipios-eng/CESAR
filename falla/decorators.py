# decorators.py
from django.http import HttpResponseForbidden
from functools import wraps

def role_required(roles):
    """
    Decorador para restringir acceso según el rol del usuario.
    :param roles: Lista de roles permitidos para acceder a la vista.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                user_role = request.user.rol.nombre if hasattr(request.user, 'rol') and request.user.rol else None
                if user_role in roles:
                    return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
        return _wrapped_view
    return decorator
