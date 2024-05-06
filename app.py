from flask import Flask, render_template, request
import numpy as np
import joblib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

# Load the saved model
model = joblib.load('hepatitis_model.sav')

# Email configuration
email_host = 'smtp.gmail.com'  # Update to SMTP host for Gmail
email_port = 587  # Default SMTP port for TLS/STARTTLS
email_user = 'majorprojectvel@gmail.com'  # Your Gmail address
email_password = 'xjetrsvwcsbzpwze'  # Your Gmail password or app password

def send_email(subject, body, recipient):
    try:
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(email_host, email_port)
        server.starttls()
        server.login(email_user, email_password)
        text = msg.as_string()
        server.sendmail(email_user, recipient, text)
        server.quit()
        return True  # Email sent successfully
    except Exception as e:
        print(f"Error sending email: {e}")
        return False  # Email sending failed

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the input values from the form
        age = float(request.form['age'])
        sex = float(request.form['sex'])
        alb = float(request.form['alb'])
        alp = float(request.form['alp'])
        alt = float(request.form['alt'])
        ast = float(request.form['ast'])
        bil = float(request.form['bil'])
        che = float(request.form['che'])
        chol = float(request.form['chol'])
        crea = float(request.form['crea'])
        ggt = float(request.form['ggt'])
        prot = float(request.form['prot'])
        recipient_email = request.form['recipient_email']
        
        # Create a numpy array from the input values
        input_data = np.array([[age, sex, alb, alp, alt, ast, bil, che, chol, crea, ggt, prot]])

        # Make a prediction using the loaded model
        prediction = model.predict(input_data)
        restext = ""
        
        # Determine the prediction message
        if prediction[0] == 0:
            restext = "You are negative for Hepaptits-C"
        elif prediction[0] == 1:
            restext = "You are positive for Hepatitis-C and the type is Normal hepatitis"
        elif prediction[0] == 2:
            restext = "You are positive for Hepatitis-C and the type is Fibrosis"
        elif prediction[0] == 3:
            restext = "You are positive for Hepatitis-C and the type is Cirrohsis"
        else:
            restext = "You are a suspected Blood donor"
        
        # Send email with prediction result
        email_sent = send_email('Hepatitis C Prediction Result', restext, recipient_email)

        if email_sent:
            return render_template('result.html', prediction=restext)
        else:
            return "Error sending email. Please try again later."
    
    # Render the input form if the method is GET
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
