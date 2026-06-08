from flask import Flask,render_template,redirect,request,session, url_for
import sqlite3
from resume_parser import extract_text
from skill_extractor import extract_skills
from analyser import analyze_resume
from decision import get_decision
from nlp_extractor import extract_resume_details
from jd_matcher import calculate_match
from flask import *
import google.generativeai as genai
import os

app = Flask(__name__)
genai.configure(api_key="AIzaSyAYAYDaG4nSMo2h4foECRuucagIKyydbS2Mo")
model = genai.GenerativeModel("gemini-2.5-flash")
app.secret_key="resume_screaning_project"


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login',methods=['post'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM reg WHERE email=? AND password=?",
        (email, password)
    )

    user = cursor.fetchone()

    conn.close()
    print("email entered:",email)
    print("password entered:",password)
    print("user found:",user)

    if user:
        session['name']=user[1]
        session['email']=user[2]
        return redirect('/home')
    else:
        return "Invalid Email or Password"


@app.route('/register',methods=['POST'])
def register():
    username=request.form.get('username')
    email=request.form.get('email')
    password=request.form.get('password')
    conn=sqlite3.connect('users.db')
    cursor=conn.cursor()
    cursor.execute("INSERT INTO reg(name,email,password) VALUES(?,?,?)",(username,email,password))
    conn.commit()
    conn.close()

    return redirect('/profile')

@app.route('/profile')
def profile():

    email = session.get('email')

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT name, age, gender, phone, email,
    academic_details, skills, interests,
    career_preference, languages, location,
    linkedin, github, photo, resume
    FROM profiles
    WHERE email = ?
    """, (email,))

    profile = cursor.fetchone()

    conn.close()

    return render_template(
        'profile.html',
        profile=profile
    )

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/home')
def home():
    resume_score=session.get('resume_score',0)
    hr_score=session.get('hr_score',0)
    technical_score=session.get('technical_score',0)
    interview_score=int((hr_score + technical_score)/2)
    readiness=int((resume_score + interview_score)/2)
    name=session.get('name','user')
    email = session.get('email')
    print("SESSION EMAIL=",email)
    profile_completion = 0

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT name, age, gender, phone, email,
    academic_details, skills, interests,
    career_preference, languages, location,
    linkedin, github, photo, resume
    FROM profiles
    WHERE email = ?
    """, (email,))
    
    profile = cursor.fetchone()
    print("PROFILE=",profile)
    conn.close()

    if profile:
        filled = sum(1 for field in profile if field and str(field).strip())
        total = len(profile)
        profile_completion = int((filled / total) * 100)
    return render_template(
        'home.html',
        name=name,
        readiness=readiness,
        resume_score=resume_score,
        interview_score=interview_score,
        profile_completion=profile_completion
    )

@app.route('/upload')
def upload():
    return render_template('upload.html')
    
@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    file=request.files['resume']
    filename=file.filename
    file.save(os.path.join('uploads',filename))
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE profiles SET resume=? WHERE email=?",
        (filename, session['email'])
    )

    conn.commit()
    conn.close()
    text = extract_text(file)

    details = extract_resume_details(text)
    skills = details["skills"]
    score, missing = analyze_resume(skills)
    decision=get_decision(score)
    session['resume_score']=score
    session['details'] = details
    session['skills'] = skills
    session['decision'] = decision
    session['resume_score'] = score
    jd_text = request.form['job_description']
    match_score = calculate_match(text, jd_text)

    if match_score >= 80:
        decision = "Highly Suitable"

    elif match_score >= 60:
        decision = "Suitable"

    else:
        decision = "Needs Improvement"

    return render_template(
        'analysis.html',
        skills=skills,
        details=details,
        score=score,
        match_score=match_score,
        missing=missing,
        decision=decision
    )
@app.route('/analysis')
def analysis():

    return render_template(
        'analysis.html',
        score=session.get('resume_score',0),
        skills=session.get('skills',[]),
        missing=session.get('missing',[]),
        decision=session.get('decision',''),
        details=session.get('details',{})
    )

@app.route('/career_analysis')
def career_analysis():

    score = session.get('resume_score', 0)

    skills = session.get('skills', [])

    return render_template(
        'career_analysis.html',
        score=score,
        skills=skills
    )

@app.route('/assessment')
def assessment():
    return render_template('assessment.html')

@app.route('/analyze-career', methods=['POST'])
def analyze_career():
    name = request.form['name']
    stage = request.form['stage']

    strengths = request.form.getlist('strengths')
    skills = request.form.getlist('skills')
    weaknesses = request.form.getlist('weaknesses')
    interests = request.form.getlist('interests')
    prompt = f"""
    Student Profile
    Name: {name}
    Career Stage:
    {stage}
    Strengths:
    {strengths}
    Skills:
    {skills}
    Weaknesses:
    {weaknesses}
    Interests:
    {interests}

    Act as an expert AI Career Advisor.
    Give:
    1. Career Fit Score (/100)
    2. Top 5 Career Paths
    3. Skill Gap Analysis
    4. Learning Roadmap
    5. Interview Readiness
    6. Resume Suggestions
    
    return ONLY pure HTML.
    DO NOT use markdown.
    do NOT include ```html or ``` tags.
    use<h1>, <h2>, <p>, <ul>, <li> 

    """
    try:
        print("sending request to gemini..")
        response = model.generate_content(prompt)
        result=response.text

    except Exception as e:
        result = f"""
        AI service temporarily unavailable.

        Error:
        {e}
        """
    return render_template(
        "result.html",
        result=result,
        name=name,
        stage=stage,
        strengths=strengths,
        skills=skills
    )
@app.route('/interview')
def interview():
    return render_template(
        'interview.html'
    )

@app.route('/technical_interview')
def technical_interview():

    skills = session.get('skills', [])

    questions = []

    if 'python' in [s.lower() for s in skills]:
        questions.append(
            "Explain Python decorators."
        )

    if 'sql' in [s.lower() for s in skills]:
        questions.append(
            "What are SQL JOINs?"
        )

    if 'html' in [s.lower() for s in skills]:
        questions.append(
            "Difference between HTML and HTML5?"
        )

    if 'css' in [s.lower() for s in skills]:
        questions.append(
            "What is Flexbox?"
        )

    if 'javascript' in [s.lower() for s in skills]:
        questions.append(
            "What are JavaScript closures?"
        )

    return render_template(
        'technical_interview.html',
        questions=questions
    )
@app.route('/hr_interview')
def hr_interview():

    questions = [
        "Tell me about yourself.",
        "Why should we hire you?",
        "What are your strengths?",
        "What are your weaknesses?",
        "Where do you see yourself in 5 years?"
    ]

    return render_template(
        'hr_interview.html',
        questions=questions
    )

@app.route('/evaluate_interview', methods=['POST'])
def evaluate_interview():

    answers = request.form.getlist('answers')

    score = 0

    for answer in answers:
        if len(answer.strip()) > 50:
            score += 20
        elif len(answer.strip()) > 50:
            score += 20

    session['interview_score'] = score

    return render_template(
        'interview_result.html',
        score=score
    )  

@app.route('/evaluate_hr', methods=['POST'])
def evaluate_hr():

    answers = request.form.getlist('answers')

    score = 0

    for answer in answers:

        if len(answer.strip()) > 50:
            score += 25

        elif len(answer.strip()) > 20:
            score += 15

    if score > 100:
        score = 100

    session['hr_score'] = score

    return render_template(
        'hr_result.html',
        score=score
    )

@app.route('/save_profile', methods=['POST'])
def save_profile():

    name = request.form.get('name')
    age = request.form.get('age')
    gender = request.form.get('gender')
    phone = request.form.get('phone')
    email = request.form.get('email')
    academic_details = request.form.get('academic_details')
    skills = request.form.get('skills')
    interests = request.form.get('interests')
    career_preference = request.form.get('career_preference')
    languages = request.form.get('languages')
    location = request.form.get('location')
    linkedin = request.form.get('linkedin')
    github = request.form.get('github')
    photo = request.form.get('photo')
    resume = request.form.get('resume')
   

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO profiles
    (
        name,age,gender,phone,email,
        academic_details,skills,interests,
        career_preference,languages,location,
        linkedin,github,photo,resume
    )
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """,
    (
        name,age,gender,phone,email,
        academic_details,skills,interests,
        career_preference,languages,location,
        linkedin,github,photo,resume
    ))

    conn.commit()
    conn.close()

    return redirect('/home')

if __name__ == '__main__':
    app.run(debug=True)