from rest_framework import viewsets, status, serializers, mixins, filters
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import PostIt, Board, WorkIn, VoteIn
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from .serializer import (
    PostitSerializer,
    UserSerializer,
    BoardSerializer,
    WorkInSerializer,
    VoteInSerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .permissions import (
    UserViewSetPermission,
    WorkInViewSetPermission,
    PostitViewSetPermission,
)


class NoUpdateModelViewSet(mixins.CreateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    """Similar to a ModelViewSet, but without update actions.

    Used by WorkinViewSet.
    """


class PostitViewSet(viewsets.ModelViewSet):
    """Postits related to the current authenticated user."""

    permission_classes = [IsAuthenticated, PostitViewSetPermission]
    filterset_fields = ['title', 'section', 'status', 'board', 'id']

    def get_serializer_class(self):

        class NewPostItSerializer(PostitSerializer):
            # The user can only see boards related to him.
            board = serializers.PrimaryKeyRelatedField(
                queryset=Board.objects.filter(workin__user=self.request.user))

        return NewPostItSerializer

    def get_queryset(self):
        # Return only postits related to the current user.
        return PostIt.objects.filter(board__workin__user=self.request.user)

    def perform_update(self, serializer):
        # Overrides perform_update() to reset the votes of the post-it.
        postit = serializer.save()
        postit.reset_votes()
        postit.save()

    def vote_postit(self, request, vote):
        # Method for voting. Only team leaders can vote, only if the post-it is
        # open and the leader hasn't voted yet.
        postit = self.get_object()
        querySet = WorkIn.objects.filter(board=postit.board, user=request.user)
        if not querySet.exists() or not querySet[0].is_leader:
            self.permission_denied(
                request, 'El usuario actual no es líder de equipo en el tablero de este post-it')
        elif not postit.status == 'O':
            self.permission_denied(
                request, message='El post it no está en estado abierto.')

        user_team = querySet[0].team
        already_voted_msg = 'El líder de equipo ya votó.'
        if user_team == 'S':
            if postit.stakeholders_vote != 2:
                self.permission_denied(request, message=already_voted_msg)
            postit.stakeholders_vote = vote
        elif user_team == 'D':
            if postit.developers_vote != 2:
                self.permission_denied(request, message=already_voted_msg)
            postit.developers_vote = vote

        if postit.developers_vote == 1 and postit.stakeholders_vote == 1:
            postit.status = 'A'
        elif postit.developers_vote + postit.stakeholders_vote <= 1:
            postit.status = 'R'

        postit.save()
        serializer = self.get_serializer(postit)
        return Response(serializer.data)

    @action(detail=True, methods=['get', 'post'])
    def reject(self, request, pk=None):
        return self.vote_postit(request, 0)

    @action(detail=True, methods=['get', 'post'])
    def approve(self, request, pk=None):
        return self.vote_postit(request, 1)


class BoardViewSet(viewsets.ModelViewSet):
    """Boards related to the current authenticated user."""

    permission_classes = [IsAuthenticated]
    serializer_class = BoardSerializer
    filterset_fields = ['name', 'id']

    def get_queryset(self):
        # Return only boards related to the current user.
        return Board.objects.filter(workin__user=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            newBoard = Board.objects.get(id=response.data['id'])
            newBoard.project_leader = self.request.user
            newBoard.save()
            WorkIn.objects.create(
                user=request.user, board_id=response.data['id'])
        return response

    @action(detail=True, methods=['post'])
    def add_collaborator(self, request, pk=None):
        board = self.get_object()
        email = request.data['email']
        try:
            user = User.objects.get(username=email)
        except ObjectDoesNotExist:
            raise NotFound(detail='No existe un usuario con ese email.')
        workIn, created = WorkIn.objects.get_or_create(board=board, user=user)
        if not created:
            return Response({'detail': 'El usuario ya colabora en este tablero.'})
        serializer = WorkInSerializer(workIn)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=False)
    def delete(self, request):
        user_id = request.user.id
        project_leader = request.data['project_leader']
        if (user_id == project_leader):
            id = request.data['id']
            board = Board.objects.get(id=id)
            board.delete()
            return Response(status=status.HTTP_200_OK)

        else:
            self.permission_denied(
                request, message='El usuario actual no es el líder de proyecto.')


class WorkInViewSet(NoUpdateModelViewSet):
    """WorkIn relations related to the current authenticated user and his
    boards."""

    permission_classes = [IsAuthenticated, WorkInViewSetPermission]
    serializer_class = WorkInSerializer
    filterset_fields = ['user', 'is_leader', 'board', 'team', 'id']

    def get_serializer_class(self):

        class NewWorkInSerializer(WorkInSerializer):
            # The user can only see boards related to him.
            board = serializers.PrimaryKeyRelatedField(
                queryset=Board.objects.filter(workin__user=self.request.user))

        return NewWorkInSerializer

    def get_queryset(self):
        # Return only instances of WorkIn for boards related to the current user,
        # this includes the WorkIn instances related to collaborators,
        # and prefetch user for the WorkInSerializer.
        return WorkIn.objects.filter(
            board__workin__user=self.request.user).prefetch_related('user')

    @action(detail=True, methods=['get', 'put', 'post'])
    def pass_leader_privileges(self, request, pk=None):
        # Passes leader privileges from the current user to the user with
        # primary key pk.
        user_workin = self.get_object()
        target_workin = WorkIn.objects.get(
            user=request.data['user']['id'], board=user_workin.board)
        if not user_workin.is_leader:
            self.permission_denied(
                request, message='El usuario actual no es lider.')
        elif target_workin.team != user_workin.team:
            self.permission_denied(
                request, message='Los usuarios son de equipos diferentes.')
        target_workin.is_leader = True
        user_workin.is_leader = False
        target_workin.save()
        user_workin.save()
        serializer = self.get_serializer(target_workin)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def select_team(self, request, pk=None):
        # Selects the team for the current user in WorkIn relation.
        workIn = self.get_object()
        team = request.data['team']
        workIn.team = team
        serializer = self.get_serializer(workIn)
        boardWorkin = WorkIn.objects.filter(board=workIn.board)
        leaderExist = False
        for val in boardWorkin:
            if val.is_leader and val.team == team:
                leaderExist = True
                break
        if not leaderExist:
            workIn.is_leader = True
        workIn.save()
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def delete(self, request, pk=None):
        # Selects the team for the current user in WorkIn relation.
        user_id = request.user.id
        delete_user = request.data['delete_user']
        board_id = request.data['board']['id']
        board = Board.objects.get(id=board_id)
        workin = WorkIn.objects.get(user=delete_user, board=board_id)
        print(workin)
        if (board.project_leader.id == user_id and user_id != delete_user and workin.is_leader == False):
            workin.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            self.permission_denied(
                request, message='El usuario actual no es el líder de proyecto.')


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [UserViewSetPermission]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['username']
    search_fields = ['username']
