from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid


class MyUserManager(BaseUserManager):
    def create_user(self, username, full_name, password=None):
        if not username:
            raise ValueError('Users must have an email address')
        if not full_name:
            raise ValueError('Users must have a full name')

        user = self.model(
            username=self.normalize_email(username),
            full_name=full_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, full_name, password):
        user = self.create_user(
            username=self.normalize_email(username),
            full_name=full_name,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_verified = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username 				= models.EmailField(verbose_name="username", max_length=253, unique=True)
    full_name               = models.CharField(verbose_name="fullname", max_length=60)
    date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin				= models.BooleanField(default=False)
    is_staff				= models.BooleanField(default=False)
    is_superuser			= models.BooleanField(default=False)
    is_verified             = models.BooleanField(default=False)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name',]

    objects = MyUserManager()

    def __str__(self):
        return self.username

    # For checking permissions. to keep it simple all admsin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

#This is used for storing notification device ids
class OneSignalNotifications(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    player_id = models.CharField(max_length=120)



