from django.contrib.auth.tokens import PasswordResetTokenGenerator


class ConfirmationCodeGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        if user.last_login is None:
            login_timestamp = ''
        else:
            login_timestamp = user.last_login.replace(
                microsecond=0, tzinfo=None
            )
        if user.password:
            return f'{user.pk}{user.password}{login_timestamp}{timestamp}'


default_token_generator = ConfirmationCodeGenerator()
