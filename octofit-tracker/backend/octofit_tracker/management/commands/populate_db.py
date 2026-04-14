from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection
from django.contrib.auth import get_user_model
from pymongo import MongoClient

# Sample data for superheroes, teams, activities, leaderboard, workouts
def get_sample_data():
    users = [
        {"name": "Tony Stark", "email": "tony@marvel.com", "team": "marvel"},
        {"name": "Steve Rogers", "email": "steve@marvel.com", "team": "marvel"},
        {"name": "Bruce Wayne", "email": "bruce@dc.com", "team": "dc"},
        {"name": "Clark Kent", "email": "clark@dc.com", "team": "dc"},
    ]
    teams = [
        {"name": "marvel", "members": ["tony@marvel.com", "steve@marvel.com"]},
        {"name": "dc", "members": ["bruce@dc.com", "clark@dc.com"]},
    ]
    activities = [
        {"user_email": "tony@marvel.com", "activity": "Running", "duration": 30},
        {"user_email": "steve@marvel.com", "activity": "Cycling", "duration": 45},
        {"user_email": "bruce@dc.com", "activity": "Swimming", "duration": 60},
        {"user_email": "clark@dc.com", "activity": "Flying", "duration": 120},
    ]
    leaderboard = [
        {"team": "marvel", "points": 150},
        {"team": "dc", "points": 180},
    ]
    workouts = [
        {"name": "Push Ups", "difficulty": "Easy"},
        {"name": "Pull Ups", "difficulty": "Medium"},
        {"name": "Squats", "difficulty": "Easy"},
        {"name": "Deadlift", "difficulty": "Hard"},
    ]
    return users, teams, activities, leaderboard, workouts

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']

        users, teams, activities, leaderboard, workouts = get_sample_data()

        # Clear collections
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Insert sample data
        db.users.insert_many(users)
        db.teams.insert_many(teams)
        db.activities.insert_many(activities)
        db.leaderboard.insert_many(leaderboard)
        db.workouts.insert_many(workouts)

        # Ensure unique index on email for users
        db.users.create_index([("email", 1)], unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data.'))
