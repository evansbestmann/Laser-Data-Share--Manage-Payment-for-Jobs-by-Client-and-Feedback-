from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

##using the get_user_model method to pass the email as the username as django doesnt do this by default
##django uses username as username

class emailbackend(ModelBackend):
    def authenticate(self,username=None, password=None, **kwargs):
        UserModel=get_user_model()
        try:
            user=UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
