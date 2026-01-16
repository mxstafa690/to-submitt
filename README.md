# FitTrack - Gym Management System

This is a gym management system built with Flask for the backend and a simple web interface for the frontend.

## What it does

The system manages gym members, subscriptions, payments, classes, and workout plans. It has different user roles like admin, trainer, reception, and regular members.

## Requirements

- Python 3.8 or higher
- MySQL database
- Virtual environment

## Setup Instructions

1. Create and activate virtual environment:
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Install dependencies:
```bash
pip install -r server/requirements.txt
```

3. Configure database:
- Copy config.ini.template to config.ini
- Edit config.ini with your MySQL username and password:
```
[mysql]
host = localhost
port = 3306
user = root
password = YOUR_PASSWORD
database = fittrack
```

## Running the Application

IMPORTANT: You must run the seed script first before running the app!

1. First, run the seed script to create the database and initial data:
```bash
cd server
python seed.py
```

2. Then run the Flask app:
```bash
python app.py
```

The API will be running at http://localhost:5000

## Project Structure

```
FitTrack/
├── server/
│   ├── app.py              # Main Flask application
│   ├── seed.py             # Database seeding script
│   ├── models/             # Database models
│   ├── routes/             # API endpoints
│   ├── services/           # Business logic
│   ├── schemas/            # Data validation
│   └── tests/              # API tests
├── web-app/                # Frontend application
└── config.ini              # Database configuration
```

## API Endpoints

All endpoints are under /api prefix:

- /api/health - Check if API is running
- /api/members - Manage gym members
- /api/plans - Subscription plans
- /api/subscriptions - Member subscriptions
- /api/payments - Payment records
- /api/checkins - Member check-ins
- /api/classes - Gym classes
- /api/workout-plans - Workout plans

## Testing

There are .http test files in the server/tests directory. You can use VS Code REST Client extension to run them.

## Technologies Used

- Flask - Web framework
- SQLAlchemy - Database ORM
- PyMySQL - MySQL driver
- Pydantic - Data validation
- MySQL - Database

## Notes

- Make sure MySQL is running before starting the application
- Don't commit config.ini file with your password
- The seed script creates some initial data (plans, classes, etc.)
