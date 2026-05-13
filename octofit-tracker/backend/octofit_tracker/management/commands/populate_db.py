from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from django.conf import settings
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']

        # Clear collections
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Teams
        marvel = {'name': 'Team Marvel', 'description': 'Earth’s mightiest heroes'}
        dc = {'name': 'Team DC', 'description': 'Justice League'}
        marvel_id = db.teams.insert_one(marvel).inserted_id
        dc_id = db.teams.insert_one(dc).inserted_id

        # Users
        users = [
            {'name': 'Tony Stark', 'email': 'tony@marvel.com', 'team_id': marvel_id},
            {'name': 'Steve Rogers', 'email': 'steve@marvel.com', 'team_id': marvel_id},
            {'name': 'Bruce Wayne', 'email': 'bruce@dc.com', 'team_id': dc_id},
            {'name': 'Clark Kent', 'email': 'clark@dc.com', 'team_id': dc_id},
        ]
        db.users.insert_many(users)
        db.users.create_index([('email', 1)], unique=True)

        # Activities
        activities = [
            {'user_email': 'tony@marvel.com', 'activity': 'Running', 'duration': 30},
            {'user_email': 'steve@marvel.com', 'activity': 'Cycling', 'duration': 45},
            {'user_email': 'bruce@dc.com', 'activity': 'Swimming', 'duration': 60},
            {'user_email': 'clark@dc.com', 'activity': 'Flying', 'duration': 120},
        ]
        db.activities.insert_many(activities)

        # Workouts
        workouts = [
            {'name': 'HIIT', 'description': 'High Intensity Interval Training'},
            {'name': 'Strength', 'description': 'Strength training'},
        ]
        db.workouts.insert_many(workouts)

        # Leaderboard
        leaderboard = [
            {'user_email': 'clark@dc.com', 'score': 100},
            {'user_email': 'tony@marvel.com', 'score': 90},
            {'user_email': 'bruce@dc.com', 'score': 80},
            {'user_email': 'steve@marvel.com', 'score': 70},
        ]
        db.leaderboard.insert_many(leaderboard)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
