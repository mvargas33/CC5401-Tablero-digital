from django.urls import path
from rest_framework import routers
from .viewsets import (
    PostitViewSet,
    UserViewSet,
    BoardViewSet,
    WorkInViewSet,
)
from .views import (
    AuthenticationView,
    LogoutView,
)


urlpatterns = [
    path('login/', AuthenticationView.as_view()),
    path('logout/', LogoutView.as_view())
]

router = routers.SimpleRouter()

router.register('postit', PostitViewSet, basename='postit')
router.register('board', BoardViewSet, basename='board')
router.register('workin', WorkInViewSet, basename='workin')
router.register('user', UserViewSet)


urlpatterns += router.urls
