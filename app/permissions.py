from rest_framework.permissions import BasePermission
from .models import WorkIn, Board


class UserViewSetPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            self.message = 'Un usuario autenticado no puede crear nuevos usuarios.'
            return view.action != 'create'
        self.message = 'Un usuario no autenticado solo puede ver OPTIONS y crear nuevos usuarios.'
        return request.method == 'OPTIONS' or view.action == 'create'

    def has_object_permission(set, request, view, obj):
        if view.action in ['update', 'partial_update', 'destroy']:
            self.message = 'Un usuario solo puede actualizar o destruir su propia información.'
            return request.user == obj
        return True


class WorkInViewSetPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if view.action == 'destroy':
            self.message = 'No se puede eliminar a otros usuarios del tablero.'
            return request.user == obj.user
        if view.action == 'select_team':
            if obj.team != 'U':
                self.message = 'Por ahora no se puede cambiar de equipo.'
                return False
            self.message = 'No se puede modificar a otros usuarios.'
            return request.user == obj.user
        return True


class PostitViewSetPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update'] and \
                request.data.get('board') != obj.board.id:
            self.message = 'No está permitido mover el postit de tablero.'
            return False
        return True
