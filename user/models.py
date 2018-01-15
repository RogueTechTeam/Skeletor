from django.db import models
from django.utils import timezone
from sorl.thumbnail import ImageField

from django_extensions.db.fields import ModificationDateTimeField
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.mail import EmailMessage

class UserManager(BaseUserManager):
    
    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        #if not email:
        #    raise ValueError('The given email address must be set')
        #email = ShrinkUserManager.normalize_email(email)
        user = self.model(username=email, email=email, is_staff=False, is_active=True,
                          last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.save(using=self._db)
        return u

class User(AbstractBaseUser):
    email = models.EmailField(_('email address'), max_length=254, unique=True, db_index=True)
    username = models.SlugField(_('username'), unique=True)
    
    type = models.CharField(max_length=7, choices = (('User','User'),('Parent','Parent')), default='User')
    
    parent = models.ForeignKey('User', related_name = 'children', blank=True, null=True)
    
    newsletter = models.BooleanField(_('newsletter'), help_text=_('Subscribe to newsletter.'), default=False)
    invited_others = models.BooleanField(_('invited others'), default=False)
    
    is_staff = models.BooleanField(
        _('staff status'), default=False, help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(
        _('active'), default=False,
        help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting '
                    'accounts.'))
    
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    updated = ModificationDateTimeField()
    #updated = ModificationDateTimeField()
    deleted = models.DateTimeField(_('deleted'), null=True, blank=True)
    
    picture = ImageField(_('picture'), upload_to='tutor-images/', default='tutor-images/defaultUser.png')
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    slug_field = 'email'
    
    # Only email and password is required to create a user account but this is how you'd require other fields.
    REQUIRED_FIELDS = ['password']
    
    def __unicode__( self ):
        return self.get_full_name()
    
    def get_full_name(self):
        return self.username
    
    def get_short_name(self):
        return self.username
    
    @property
    def is_superuser(self):
        return self.is_staff
    
    def has_perm(self, perm, obj=None):
        return self.is_staff
    
    def has_module_perms(self, app_label):
        return self.is_staff
    
    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User with content type HTML.
        """
        # It's possible to send multi-part text / HTML email by following these instructions:
        # https://docs.djangoproject.com/en/1.5/topics/email/#sending-alternative-content-types
        msg = EmailMessage(subject, message, from_email, [self.email])
        msg.content_subtype = 'html'  # Main content is now text/html
        msg.send()

