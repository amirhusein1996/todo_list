from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import reverse



class CustomUserManager(UserManager):
    "Is_active will remain False until email confirmation."

    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")

        extra_fields.setdefault('is_active', False)
        return super().create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField(_("email address"), unique=True) # it's not unique by default

    activation_code = models.CharField(verbose_name=_('Activation Code'), max_length=255, null=True)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    objects = CustomUserManager()


    def get_activation_url(self):
        return reverse("account:activation_view" , args=[self.activation_code])

    def get_reset_pasword_url(self):
        return reverse("account:reset_password_confirmation_view" , args=[self.activation_code])

class UserExtraInfo(models.Model):
    """
    To make the main User model lighter
    """
    class Gender(models.TextChoices):
        GENDER_MALE = 'M' , _("Male")
        GENDER_FEMALE = 'F' , _("Female")

    user = models.OneToOneField(to=User,on_delete=models.CASCADE , db_index=True)

    gender = models.CharField(
        max_length=1, null=True,
        choices=Gender.choices,
        verbose_name=_("Gender"),
    )
    first_name = models.CharField(_("First name"), max_length=150, blank=True)
    last_name = models.CharField(_("Last name"), max_length=150, blank=True)

    birthdate = models.DateField(verbose_name=_('Birthdate'),blank=True, null=True)

    avatar = models.ImageField( verbose_name=_('Avatar') ,
                                upload_to='images/user_profiles/',
                                blank=True, null=True,
                               )

    class Meta:
        verbose_name = _("User Extra Information")
        verbose_name_plural = _("User Extra Informations")

    def get_fullname(self):
        if self.first_name or self.last_name:
            """ returns firstname and lastname with space between
            or only first name or last name
            otherwise None"""
            return (self.first_name.title() + " " + self.last_name.title()).strip()



    def __str__(self):
        return self.get_fullname() or self.user.username

@receiver(signal=post_save, sender = User)
def user_extra(sender , instance , created , **kwargs):
    if created:
        """
        Whenever a new user signs up and new instance of User creates ,
        it will create new instance of UserExtraInfo
        """
        UserExtraInfo.objects.create(user=instance)