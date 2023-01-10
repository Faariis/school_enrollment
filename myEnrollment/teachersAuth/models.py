from django.db import models
# Followed the tutorial https://www.youtube.com/watch?v=PUzgZrS_piQ&list=PLlameCF3cMEu-LbsQYUDUVkiZ2jc2rpLx
from django.core.mail import send_mail
from django.contrib.auth.models import UserManager,BaseUserManager,AbstractBaseUser, AbstractUser # AbstractUser, AbstractBaseUser


from django.contrib.auth import user_login_failed, user_logged_in
from django.contrib.auth.models import update_last_login
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from secondarySchools.models import SecondarySchool, CoursesSecondarySchool
from django.forms import ValidationError

def update_last_and_previous_login(sender, user, **kwargs):
    if user.last_login:
        user.previous_login = user.last_login
        user.last_login = timezone.now()
        user.save(update_fields=["previous_login", "last_login"])

user_logged_in.disconnect(update_last_login, dispatch_uid="update_last_login")
user_logged_in.connect(update_last_and_previous_login, dispatch_uid="update_last_and_previous_login")

class ExManager(models.Manager):
    def get_queryset(self):
        return super(ExManager, self).get_queryset().all()

# We need to add username as required field in order to create the superuser on CLI
# Because of that we have to override create_superuser()
class CustomUserManager(UserManager):
    #use_in_migrations = True
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            password= password,
            email=self.normalize_email(email),
            **extra_fields
        )
        # change password to hash,
        # tested we still have to do in serializer - I guess this is related
        # to saving user from admin ?
        user.set_password(password)
        update_last_and_previous_login(None, user)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        user = self.model(
            first_name= first_name,
            last_name= last_name,
            password= password,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.is_superuser=True
        user.is_staff=True
        user.set_password(password)
        user.save(using=self._db)
        return user


class Teacher(AbstractUser):
    class Meta:
        verbose_name = ('Nastavnik')
        verbose_name_plural = ('Nastavnici')
        ordering = ['email']
        db_table= 'teachers'
        constraints = [
            #models.CheckConstraint(check=models.Q(age__gte=18), name='age_gte_18'),
            models.UniqueConstraint(fields=['id','email', 'course_code'],
                                    name='composite-pk-id-email-course')
        ]
    # Django by default creates username as unique and as USERNAME_FIELD, we have to override it
    username= None
    # It must be unique since it is USERNAME_FIELD, but we want to allow multiple records in table
    email= models.EmailField(max_length = 50, unique= True)
    password= models.CharField(max_length = 255)
    # There is no need to add canton of teacher,
    # since if we know school it, we can get through canton using school_canton_code
    # Many teachers can belong to single school
    school_id= models.ForeignKey(SecondarySchool,
                                 on_delete=models.CASCADE,
                                 related_name='school_id')
    course_code= models.ForeignKey(CoursesSecondarySchool,
                                 on_delete=models.CASCADE,
                                 related_name='course_code')
    previous_login = models.DateTimeField(_("previous login"), blank=True, null=True)
    objects = CustomUserManager() # objects is _default_manager, default models.Manager()
    ab_ob= ExManager()
    # We want that Django logs in with email and password
    USERNAME_FIELD = 'email'
    EMAIL_FIELD= 'email'
    # Required fields is used by createsuperuser(), no need for username_field and password
    # AbstractUser has fields which we can use for superuser()
    # If canton_code is added, in CLI it is expecting object instance.
    REQUIRED_FIELDS = ['first_name','last_name']
    def __str__(self):
        return f'{self.email}'

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    # def _do_update(self, base_qs, using, pk_val, values, update_fields, forced_update):
    #     return True

    # def validate_unique(self, *args, **kwargs):
    #     # super(Teacher, self).validate_unique(*args, **kwargs)
    #     qs = Teacher.objects.filter(email=self.email)
    #     if qs.filter(school_id__id=self.school_id).exists():
    #         raise ValidationError({'school_id':['school_id must be unique',]})
    # def save(self, *args, **kwargs):
    #     self.validate_unique()
    #     super(Teacher, self).save(*args, **kwargs)
    # def get_unique_for_date_validators(self):
    #     return True 
