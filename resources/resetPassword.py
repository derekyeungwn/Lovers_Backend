import datetime, json, secrets
from flask import request, Response, Blueprint, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
import smtplib
from string import Template
import pathlib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import hashlib
from datetime import datetime, timedelta

from util.db import db
from forms.resetPasswordForm import ResetPasswordForm

resetPassword_bp = Blueprint('resetPassword', __name__)

@resetPassword_bp.route('/', methods=['POST'])
def reset_password():
    try:
        output = {}

        email = request.json.get('email', None)

        user = db.users.find_one({'email': email}, {'user_id': 1})
        if user is None:
            output['success'] = True
            return Response(json.dumps(output, default=str), mimetype='application/json', status=200)
              
        token = secrets.token_urlsafe()
        user_id = user['user_id']

        m = hashlib.md5()
        m.update(token.encode('utf-8'))
        hashValue = m.hexdigest()

        db.users.update_one({'user_id': user_id}, {'$push' : {'tokens' : {'token' : hashValue, 'token_create_datetime' : datetime.now()}}})

        #send email
        content = MIMEMultipart()
        content["subject"] = "Password Reset"
        content["from"] = "test@gmail.com"
        content["to"] = email
        template = Template(pathlib.Path('templates/resetPasswordEmailTemplate.html').read_text())
        body = template.substitute({'url' : 'https://www.derekyeungwn.com/api/v1/resetPassword/page?token=' + token})
        #body = template.substitute({'url' : 'http://localhost:8888/api/v1/resetPassword/page?token=' + token})
        content.attach(MIMEText(body, "html"))

        with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:
            try:
                smtp.ehlo()
                smtp.starttls()
                smtp.login("derekyeungwn@gmail.com", "uctwmvhehereymwb")
                smtp.send_message(content)
            except Exception as e:
                print(e)
                output['success'] = False
                output['error_message'] = 'Internal Server Error'
                return Response(json.dumps(output), mimetype='application/json', status=500)

        output['success'] = True

    except Exception as e:
        print(e)
        output['success'] = False
        output['error_message'] = 'Internal Server Error'
        return Response(json.dumps(output), mimetype='application/json', status=500)
    return Response(json.dumps(output, default=str), mimetype='application/json', status=200)

@resetPassword_bp.route('/page', methods=['GET', 'POST'])
def func():
    form = ResetPasswordForm(token = request.args.get('token'))
    if form.validate_on_submit():
        token = request.args.get('token')
        password = form.password.data

        m = hashlib.md5()
        m.update(token.encode('utf-8'))
        hashValue = m.hexdigest()

        user = db.users.find_one({'tokens.token':hashValue})

        if user is not None:
            for data in user['tokens']:
                if data['token'] == hashValue:
                    expiryDate = data['token_create_datetime'] + timedelta(days=10)
                    now = datetime.now()
                    if now < expiryDate:
                        m.update(password.encode('utf-8'))
                        m2 = hashlib.md5()
                        m2.update(password.encode('utf-8'))
                        hashValue = m2.hexdigest()
                        
                        #clear all generated tokens and reset the password
                        db.users.update_one({'user_id':user['user_id']}, {'$set':{'tokens':[], 'password': hashValue}})
                    
                    break
        
        return '成功'
    return render_template('resetPassword.html', form = form)