from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)

# Configure the SQLite database.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# In-memory storage for registered users.
users = {}

def calculate_bmi(weight, height):
    """Calculate BMI given weight (kg) and height (m)."""
    try:
        bmi = weight / (height ** 2)
    except ZeroDivisionError:
        bmi = 0
    return round(bmi, 2)

def get_diet_recommendations(bmi):
    """Provide diet recommendations based on BMI."""
    if bmi < 18.5:
        category = "Underweight"
        advice = ("Increase calorie intake with nutrient-dense foods such as nuts, dried fruits, whole grains, "
                  "lean proteins, and healthy fats. Consider adding smoothies and energy-dense snacks.")
    elif 18.5 <= bmi < 24.9:
        category = "Normal weight"
        advice = ("Maintain a balanced diet rich in fruits, vegetables, whole grains, lean proteins, and healthy fats. "
                  "Keep up with regular physical activity.")
    elif 25 <= bmi < 29.9:
        category = "Overweight"
        advice = ("Adopt a diet low in saturated fats and sugars. Emphasize fruits, vegetables, whole grains, and lean proteins. "
                  "Monitor portion sizes and increase fiber intake.")
    else:
        category = "Obese"
        advice = ("Consult a healthcare provider for personalized advice. Focus on a calorie-restricted diet that is rich in nutrients, "
                  "and incorporate regular physical activity.")
    return category, advice

def calculate_water_intake(weight):
    water_intake_liters = (weight * 35) / 1000
    return round(water_intake_liters, 2)
class ExerciseSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), nullable=False, index=True)
    exercise_type = db.Column(db.String(20), nullable=False)
    exercise_id = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.date.today)

    def __repr__(self):
        return f'<ExerciseSession {self.user_id} {self.exercise_type} {self.exercise_id} {self.date}>'

# ---------------------------
# Data for Exercises
# ---------------------------
# Custom Yoga Exercises – 5 exercises.
yoga_exercises = [
    {"id": 1, "name": "Mountain Pose", "description": "Stand tall with feet together, shoulders relaxed, and arms at your sides."},
    {"id": 2, "name": "Downward Dog", "description": "Start on all fours, then lift your hips up and back to form an inverted V shape."},
    {"id": 3, "name": "Warrior II", "description": "Stand with legs wide apart, turn your right foot out, and bend your right knee while extending your arms."},
    {"id": 4, "name": "Tree Pose", "description": "Stand on one leg and place the sole of your other foot on your inner thigh to maintain balance."},
    {"id": 5, "name": "Child's Pose", "description": "Sit back on your heels, lean forward, and stretch your arms out, resting your forehead on the ground."}
]

# Custom Gym Exercises – 5 exercises.
gym_exercises = [
    {"id": 1, "name": "Bench Press", "description": "A compound exercise for chest, shoulders, and triceps."},
    {"id": 2, "name": "Squat", "description": "A fundamental lower-body exercise to build strength in legs and glutes."},
    {"id": 3, "name": "Deadlift", "description": "An exercise that works your back, glutes, and hamstrings."},
    {"id": 4, "name": "Overhead Press", "description": "Targets shoulders and triceps for upper body strength."},
    {"id": 5, "name": "Pull-Up", "description": "A bodyweight exercise that strengthens your back and biceps."}
]

# ---------------------------
# Routes
# ---------------------------
@app.route('/', methods=['GET', 'POST'])
def registration():
    """
    Registration page:
    - GET: Render registration form.
    - POST: Process form, calculate BMI, store user, and redirect to home.
    """
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        weight = float(request.form.get('weight'))
        height = float(request.form.get('height'))
        bmi = calculate_bmi(weight, height)
        user = {
            "user_id": user_id,
            "weight": weight,
            "height": height,
            "bmi": bmi,
            "registered_at": datetime.datetime.now().isoformat()
        }
        users[user_id] = user
        return redirect(url_for('home', user_id=user_id))
    return render_template('registration.html')

@app.route('/home')
def home():
    """Home page with navigation links for Yoga, Gym, 30-Day Challenges, and Diet Recommendations."""
    user_id = request.args.get('user_id', '')
    return render_template('home.html', user_id=user_id)

# Yoga Routes
@app.route('/yoga_exercises')
def yoga_exercises_page():
    """Display a list of yoga exercises."""
    user_id = request.args.get('user_id', '')
    return render_template('yoga_exercises.html', user_id=user_id, exercises=yoga_exercises)

@app.route('/yoga_exercise/<int:exercise_id>')
def yoga_exercise_detail(exercise_id):
    """Display details for a selected yoga exercise."""
    user_id = request.args.get('user_id', '')
    exercise = next((ex for ex in yoga_exercises if ex['id'] == exercise_id), None)
    if not exercise:
        return "Exercise not found", 404
    return render_template('yoga_exercise_detail.html', user_id=user_id, exercise=exercise)

# Gym Routes
@app.route('/gym_exercises')
def gym_exercises_page():
    """Display a list of gym exercises."""
    user_id = request.args.get('user_id', '')
    return render_template('gym_exercises.html', user_id=user_id, exercises=gym_exercises)

@app.route('/gym_exercise/<int:exercise_id>')
def gym_exercise_detail(exercise_id):
    """Display details for a selected gym exercise."""
    user_id = request.args.get('user_id', '')
    exercise = next((ex for ex in gym_exercises if ex['id'] == exercise_id), None)
    if not exercise:
        return "Exercise not found", 404
    return render_template('gym_exercise_detail.html', user_id=user_id, exercise=exercise)
@app.route('/diet_recommendations')
def diet_recommendations():
    user_id = request.args.get('user_id', '')
    user = users.get(user_id)
    if not user:
        return "User not found", 404

    bmi = user['bmi']
    weight = user['weight']
    category, advice = get_diet_recommendations(bmi)
    water_intake = calculate_water_intake(weight)

    return render_template('diet_recommendations.html', user_id=user_id, bmi=bmi,
                           category=category, advice=advice, water_intake=water_intake)
def get_30_day_gym_challenge_plan():
    plan = []
    for day in range(1, 31):
        if day % 7 == 0:
            exercises = "Rest Day: Light stretching and recovery."
        else:
            bench_press = 10 + (day * 2)
            squats = 12 + (day * 2)
            deadlift = 8 + (day * 2)
            overhead_press = 10 + (day * 2)
            pull_up = 5 + (day // 2)
            exercises = (f"Bench Press: {bench_press} reps, Squat: {squats} reps, Deadlift: {deadlift} reps, "
                         f"Overhead Press: {overhead_press} reps, Pull-Up: {pull_up} reps")
        plan.append({"day": day, "exercises": exercises})
    return plan

@app.route('/30_day_gym_challenge')
def gym_challenge():
    user_id = request.args.get('user_id', '')
    challenge_plan = get_30_day_gym_challenge_plan()
    return render_template('30_day_gym_challenge.html', user_id=user_id, challenge_plan=challenge_plan)

# 30-Day Yoga Challenge Route
def get_30_day_yoga_challenge_plan():
    plan = []
    routines = [
       "Perform 3 rounds of Sun Salutations (2 minutes each).",
       "Hold Mountain Pose and Downward Dog for 3 rounds (2 minutes each).",
       "Perform 3 rounds of Warrior II (1.5 minutes each side) and Tree Pose (1.5 minutes each side).",
       "Hold Child's Pose for 3 rounds (3 minutes each).",
       "Practice deep breathing and mindful meditation for 10 minutes.",
       "Perform a combination of Mountain, Warrior, and Downward Dog in sequence."
    ]
    for day in range(1, 31):
        if day % 7 == 0:
            exercises = "Rest Day: Focus on meditation, mindful breathing, and gentle stretching."
        else:
            routine_index = (day - 1) % len(routines)
            exercises = routines[routine_index]
        plan.append({"day": day, "exercises": exercises})
    return plan

@app.route('/30_day_yoga_challenge')
def yoga_challenge():
    user_id = request.args.get('user_id', '')
    challenge_plan = get_30_day_yoga_challenge_plan()
    return render_template('30_day_yoga_challenge.html', user_id=user_id, challenge_plan=challenge_plan)
@app.route('/daily_time')
def daily_time():
    user_id = request.args.get('user_id')
    date_str = request.args.get('date')
    if date_str:
        query_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        query_date = datetime.date.today()

    sessions = ExerciseSession.query.filter_by(user_id=user_id, date=query_date).all()
    total_minutes = sum(session.duration for session in sessions)
    return jsonify({"user_id": user_id, "date": query_date.isoformat(), "total_minutes": total_minutes})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
