from django.core.management.base import BaseCommand
from app.models import Board, WorkIn, PostIt, VoteIn
from django.contrib.auth.models import User
from faker import Faker
import random

fake = Faker()

class Command(BaseCommand):
    help = "Populates the db"

    def populate_users(self, n):
        i = 0
        while i < n:
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = "{}.{}@example.com".format(first_name, last_name)
            User.objects.create_user(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password='HJhknlj123'
            )
            i += 1

    def populate_boards(self, n):
        i = 0
        while i < n:
            board = Board()
            board.name = fake.catch_phrase()
            board.description = fake.sentence()
            board.save()
            i += 1

    def populate_work_in(self, boardsNumber):
        i = 0
        j = 0
        boards = Board.objects.all()
        for user in User.objects.all():
            if user.username == 'admin':
                continue
            workin = WorkIn()
            workin.user = user
            workin.board = boards[j]
            workin.team = 'D' if i < 4 else 'S'
            workin.is_leader = True if (i == 0 or i == 4) else False
            workin.save()
            i += 1
            if (i == 8):
                i = 0
                j = j + 1
            if (j > boardsNumber-1):
                break

    def populate_postit(self, n):
        i = 0
        status = ['O', 'A', 'R']
        sections = [s for s in range(9)]
        boards = Board.objects.all()
        while i < n:
            postit = PostIt()
            postit.title = fake.job()
            postit.description = fake.sentence()
            postit.section = random.choice(sections)
            postit.status = random.choice(status)
            postit.board = random.choice(boards)
            postit.save()
            i = i + 1
    
    def populate_vote_in(self):
        boards = Board.objects.all()
        votes = [0, 1, 2]
        for board in boards:
            workin = WorkIn.objects.filter(board=board)
            postits = PostIt.objects.filter(board=board)
            for work in workin:
                for postit in postits:
                    votein = VoteIn()
                    votein.user = work.user
                    votein.postit = postit
                    votein.vote = random.choice(votes)
                    votein.team = work.team
                    votein.save()

    def handle(self, *args, **kwargs):
        self.populate_users(100)
        self.populate_boards(10)
        self.populate_work_in(10)
        self.populate_postit(250)
        self.populate_vote_in()