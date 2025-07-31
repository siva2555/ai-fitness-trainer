Overview

The Fitness Tracking System is a web-based application that helps users monitor their fitness journey, track workouts, get diet recommendations, and engage in 30-day challenges. The system also incorporates AI-based pose estimation to assist users in evaluating their exercise form using live camera feed.

Features

User Registration: Users can register by entering weight, height, and a unique ID.

BMI Calculation & Diet Recommendations: Provides personalized diet advice based on BMI.

Water Intake Suggestion: Calculates daily recommended water intake.

Exercise Tracking: Users can log gym and yoga workouts.

30-Day Challenges: Includes structured gym and yoga workout challenges.

Live Pose Estimation: AI-powered real-time posture evaluation using a webcam.

Daily Exercise Summary: Displays total workout time per day.

Technologies Used

Backend: Flask (Python)

Database: SQLite

Frontend: HTML, CSS, JavaScript

AI Model: PoseNet (for real-time pose estimation)
Mediapipe
Installation & Setup
ComputerVision
Prerequisites

Ensure you have the following installed on your system:

Python 3.x

Flask

Flask-SQLAlchemy

TensorFlow.js (for PoseNet)

A working webcam (for AI pose estimation)

Steps to Run Locally

Clone the repository:

git clone https://github.com/yourusername/fitness-tracking-system.git
cd fitness-tracking-system

Create a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Set up the database:

python -c "from app import db; db.create_all()"

Run the application:

python app.py

Open your browser and go to:

http://127.0.0.1:5000/

Database Structure

The application uses SQLite as the database, with the following table structure:

ExerciseSession Table

Column

Type

Description

id

Integer (PK)

Unique session ID

user_id

String

User's unique identifier

exercise_type

String

Type of exercise (Yoga/Gym)

exercise_id

Integer

ID of the performed exercise

start_time

DateTime

Time when the session started

duration

Integer

Duration in minutes

date

Date

Date of exercise

AI-Based Pose Estimation

The AI model used in this project is PoseNet, which detects human body keypoints and evaluates posture. It is integrated using TensorFlow.js to:

Identify key body joints

Analyze user posture

Provide feedback on exercise form

How Pose Estimation Works

The webcam captures a live video feed.

PoseNet processes the video and extracts keypoints (head, shoulders, arms, legs, etc.).

A function evaluates the detected pose and provides corrective feedback based on confidence scores.

Live Camera Access

The system utilizes getUserMedia API in JavaScript to access the user's webcam:

navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    video.srcObject = stream;
  })
  .catch(error => {
    console.error("Error accessing camera: ", error);
  });

Deployment

You can deploy the app on platforms like Heroku or Render:

Deploy on Heroku

Install Heroku CLI:

npm install -g heroku

Login to Heroku:

heroku login

Create a Heroku app:

heroku create fitness-tracker-app

Push the project to Heroku:

git push heroku main

Open the deployed app:

heroku open

Screenshots

Home Page



Yoga Exercise Page



Live Pose Estimation



Future Enhancements

Integration with Wearable Devices (Fitbit, Apple Watch, etc.)

AI-driven Personalized Workout Plans

Mobile App for Android & iOS

Advanced pose correction system with feedback animation


Contact

For any queries, contact: 6303048434

Email: sivavarma2555@gmail.com

GitHub: siva2555
