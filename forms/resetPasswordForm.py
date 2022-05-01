from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, HiddenField
from wtforms.validators import InputRequired, EqualTo, Length

class ResetPasswordForm(FlaskForm):
   password = PasswordField('新密碼', [
      InputRequired('請輸人新密碼')
      #,Length(min=8, message='too short')      
   ]) 
   confirmPassword = PasswordField('重新輸入新密碼', [
      InputRequired(),
      EqualTo('password', message='Passwords must match.')
   ]) 
   token = HiddenField()
   submit = SubmitField('OK')