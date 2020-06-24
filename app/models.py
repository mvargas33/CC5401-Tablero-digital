from django.db import models
from django.contrib.auth.models import User


# Tableros
class Board(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    project_leader = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return "{}".format(self.name)


# Relación usuario-tablero
class WorkIn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    is_leader = models.BooleanField(default=False)
    team_choices = [('D', 'Developer'), ('S', 'Stakeholder'), ('U', 'Unassigned')]
    team = models.CharField(max_length=1, choices=team_choices, default='U')

    def __str__(self):
        return 'User: {} in Board: {}'.format(self.user.username, self.board.name)

# Post-its
class PostIt(models.Model):
    title = models.CharField(max_length=90)
    description = models.TextField()
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    vote_choices = [
        (0, 'No'),
        (1, 'Si'),
        (2, 'No contestado')
    ]
    stakeholders_vote = models.IntegerField(choices=vote_choices, default=2)
    developers_vote = models.IntegerField(choices=vote_choices, default=2)
    status_choices = [
        ('O', 'Open'),      # En votación 
        ('A', 'Approvecd'), # Aprovado
        ('R', 'Rejected'),  # Rechazado
        ('F', 'Filed')      # Archivado
    ]
    status = models.CharField(max_length=1, choices=status_choices, default='O')
    section_choices = [
        (0, 'Objetivos'),
        (1, 'Usuarios'),
        (2, 'Fuentes'),
        (3, 'Conceptos'),
        (4, 'Métricas e Indicadores'),
        (5, 'Generación de Conceptos'),
        (6, 'Generación de Métricas'),
        (7, 'Visualización, Notificación y Acción'),
        (8, 'Entorno')
    ]
    section = models.IntegerField(choices=section_choices)
    
    def __str__(self):
        return '"{}" in Board: "{}"'.format(self.title, self.board.name)

    def reset_votes(self):
        self.stakeholders_vote = 2
        self.developers_vote = 2
        self.status = 'O'


# Votos de los usuarios en los post-its
class VoteIn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    postit = models.ForeignKey(PostIt, on_delete=models.CASCADE)
    vote_choices = [
        (0, 'No'),
        (1, 'Si'),
        (2, 'No contestado')
    ]
    vote = models.IntegerField(choices=vote_choices, default=2)
    team_choices = [('D', 'Developer'), ('S', 'Stakeholder')]
    team = models.CharField(max_length=1, choices=team_choices)

    def __str__(self):
        return 'Vote of {} in Post-it "{}"'.format(self.user.username, self.postit.title)

    class Meta:
        unique_together = (("user", "postit"),)