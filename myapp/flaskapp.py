import os
from flask import Flask, render_template, url_for, flash, redirect, request, send_from_directory, abort, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from forms import RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt
from database import db
from models import User
from utils.gpt_generate import chat_development
from utils.text_pp import parse_response, create_ppt, create_ppt_v2
from dotenv import load_dotenv

load_dotenv()  # This loads the .env file

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
bcrypt = Bcrypt(app)
db.init_app(app)


# Configure Flask-Login
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', user=current_user)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form, user=current_user)


@app.route("/login", methods=['GET', 'POST'])
def login():
    # if the user is already authenticated, redirect them to home page
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form, user=current_user)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/generator', methods=['GET', 'POST'])
def generate():
    # data = { 
    #         "Modules" : 15, 
    #         "Subject" : "Data Structures and Algorithms", 
    #     } 
    if request.method == 'POST':
        print(request.content_type)
        custom_template = request.files['custom_template']
        print(custom_template)
        # file_input.save(f'./uploads/{file_input.filename}')
        number_of_slide = request.form.get('number_of_slide')
        user_text = request.form.get('user_text')
        template_choice = request.form.get('template_choice')
        presentation_title = request.form.get('presentation_title')
        presenter_name = request.form.get('presenter_name')
        insert_image = 'insert_image' in request.form

        user_message = f"I want you to come up with the idea for the PowerPoint. The number of slides is {number_of_slide}. " \
                       f"The content is: {user_text}.The title of content for each slide must be unique, " \
                       f"and extract the most important keyword within two words for each slide. Summarize the content for each slide. "
        
        

        # assistant_response = chat_development(user_message)
        # # Check the response (for debug)
        # print(f"Assistant Response:\n{assistant_response}")
        slides_content = {"slides":[{"title":"Introduction – Overview of AI Growth","layout":{"type":"Title","sections":[{"position":"top","type":"title","content":"The Future of AI"},{"position":"center","type":"subtitle","content":"Overview of AI Growth"},{"position":"background","type":"image","description":"Futuristic tech design"}]}},{"title":"Key Trends – AI in Healthcare, Finance, and Education","layout":{"type":"Grid","sections":[{"position":"top","type":"title","content":"Key Trends in AI"},{"position":"main","type":"three-columns","columns":[{"heading":"Healthcare","points":["Diagnostics","Personalized Medicine"],"icon":"🏥"},{"heading":"Finance","points":["Fraud Detection","Algorithmic Trading"],"icon":"💰"},{"heading":"Education","points":["Adaptive Learning","AI Tutors"],"icon":"🎓"}]}]}},{"title":"Challenges – Ethical Concerns and Job Displacement","layout":{"type":"List","sections":[{"position":"top","type":"title","content":"AI Challenges"},{"position":"main","type":"two-columns","columns":[{"heading":"Ethical Concerns","points":["Bias","Privacy","Accountability"],"icon":"⚖️"},{"heading":"Job Displacement","points":["Automation impact","Reskilling needs"],"icon":"🛠️"}]}]}},{"title":"Conclusion – Summary and Future Outlook","layout":{"type":"Summary","sections":[{"position":"top","type":"title","content":"Conclusion"},{"position":"main","type":"bullets","items":["AI is transforming industries","Key trends in healthcare, finance, and education","Addressing ethical concerns and job displacement"]},{"position":"bottom","type":"highlight","content":"The future of AI is promising, but responsible development is key."}]}}]}
        # print(type(slides_content))
        # create_ppt([], custom_template, presentation_title, presenter_name, insert_image)
        create_ppt_v2([], custom_template, presentation_title, presenter_name, insert_image)
    # return jsonify(data)

    return render_template('generator.html', title='Generate')


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        return send_from_directory('generated', filename, as_attachment=True)

    except FileNotFoundError:
        abort(404)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=5001, debug=True)
