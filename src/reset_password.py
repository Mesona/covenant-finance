"""Instructions modified from https://dev.to/paurakhsharma/flask-rest-api-part-5-password-reset-2f2e"""

import datetime
from flask import request, render_template
from flask_jwt_extended import create_access_token, decode_token
from jwt.exceptions import ExpiredSignatureError, DecodeError, \
    InvalidTokenError
from static.errors import SchemaValidationError, InternalServerError, \
    EmailDoesNotExistsError, BadTokenError
from services.mail_service import send_email

def forgotPassword(user_email, user_id):
        print("INIT FORGOTPASSWORD")
        user_email = user_email
        user_id = user_id

        url = request.base_url + 'reset_password/'
        try:
            # Create log for someone spamming password recovery
            #if not email:
            #   raise SchemaValidationError

            #if not user:
            #    raise EmailDoesNotExistsError

            expires = datetime.timedelta(hours=24)
            reset_token = create_access_token(str(user_id), expires_delta=expires)
            print("recipients:", user_email)
            #print("TEXT BODY:", render_template('templates/reset_password.txt', url=url + reset_token))
            #print("HTML BODY:", render_template('templates/reset_password.html', url=url + reset_token))

            return send_email('Ars Magic Covenant Finance -- Reset Your Password',
                              sender='support@TBD',
                              recipients=[user_email],
                              text_body=render_template('templates/reset_password.txt',
                                                        url=url + reset_token),
                              html_body=render_template('templates/reset_password.html',
                                                        url=url + reset_token))
        #except SchemaValidationError:
        #    raise SchemaValidationError
        #except EmailDoesNotExistsError:
        #    raise EmailDoesNotExistsError
        except Exception as e:
            raise InternalServerError


#class ResetPassword():
#    def post(self):
#        try:
#            body = request.get_json()
#            reset_token = body.get('reset_token')
#            password = body.get('password')
#
#            if not reset_token or not password:
#                raise SchemaValidationError
#
#            user_id = decode_token(reset_token)['identity']
#
#            user = User.objects.get(id=user_id)
#
#            user.modify(password=password)
#            user.hash_password()
#            user.save()
#
#            return send_email('Ars Magica Covenant Finance Password reset successful',
#                              sender='support@TBD',
#                              recipients=[self.user_email],
#                              text_body='Password reset was successful',
#                              html_body='<p>Password reset was successful</p>')
#
#        #except SchemaValidationError:
#        #    raise SchemaValidationError
#        #except ExpiredSignatureError:
#        #    raise ExpiredTokenError
#        #except (DecodeError, InvalidTokenError):
#        #    raise BadTokenError
#        except Exception as e:
#            raise InternalServerError
