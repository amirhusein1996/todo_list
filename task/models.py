from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = 'l', _('Low')
        MEDIUM = 'm', _('Medium')
        HIGH = 'h', _('High')

    class Progress(models.TextChoices):
        AT_BEGINNING = 'beginning', _('At the Beginning')
        IN_PROGRESS = 'middle', _('In Progress')
        NEAR_COMPLETION = 'nearing', _('Near Completion')
        COMPLETED = 'completed', _('Completed')

    class Category(models.TextChoices):
        WORK = 'w', _('Work')
        PERSONAL = 'p', _('Personal')
        OTHER = 'o', _('Other')

    user = models.ForeignKey(verbose_name=_('User'), to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(verbose_name=_('Title'), max_length=100)
    description = models.TextField(verbose_name=_('Description'), null=True, blank=True)
    priority = models.CharField(verbose_name=_('Priority'), max_length=1, choices=Priority.choices)
    progress = models.CharField(verbose_name=_('Progress'), max_length=10, choices=Progress.choices,
                                default=Progress.AT_BEGINNING)
    category = models.CharField(verbose_name=_('Category'), choices=Category.choices, max_length=1)
    is_completed = models.BooleanField(verbose_name=_('Is completed'), blank=True, null=True,editable=False)
    deadline = models.DateField(verbose_name=_('Deadline'), null=True, blank=True)
    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Check if user set the task to Completed then automatically is_completed will be set to True
        otherwise will be False
        """

        if self.progress == Task.Progress.COMPLETED:
            self.is_completed = True
        else:
            self.is_completed = False

        """
        Calling full_clean method ensures that all validation, including the `clean` method, is run
        before saving. If any validation errors are raised, a `ValidationError`
        will be raised and the instance will not be saved.
        """
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):

        """
        It checks if the values of the
        'progress', 'priority', and 'category' fields are in the valid
        choices defined by the corresponding 'Choices' classes. If any of
        the values is not a valid choice, a ValidationError is raised.
        """
        super().clean()

        if self.progress not in [choice[0] for choice in Task.Progress.choices]:
            raise ValidationError({
                'progress': _('Invalid choice')
            })

        if self.priority not in [choice[0] for choice in Task.Priority.choices]:
            raise ValidationError({
                'priority': _('Invalid choice')
            })

        if self.category not in [choice[0] for choice in Task.Category.choices]:
            raise ValidationError({
                'category': _('Invalid choice')
            })

    def task_remaining_time(self):
        """ Returns the situation of the task """

        if self.is_completed:
            return _('Done')

        if self.deadline:
            time_delta = self.deadline - timezone.now().date()

            if time_delta.days < 0:
                return str(abs(time_delta.days)) + " " + _("days overdue")
            elif time_delta.days == 0:
                return _("Today")
            elif time_delta.days == 1:
                return _("Tomorrow")
            elif time_delta.days > 1:
                return str(time_delta.days) + " " + _('days left')

        return _("No deadline set")


class Tag(models.Model):
    """
    A tag is a custom label created by a user to categorize their todo items. Tags
    can be used to filter and organize todo items based on user-defined criteria.

    Attributes:
        user (ForeignKey): The user who created the tag.
        title (CharField): The name of the tag.

    Methods:
        save(*args, **kwargs): Overrides the default save method to limit the number of
            tags a user can create to a maximum of 5.
    """

    """
    If you see this docstring it means this Goal isn't implemented yet
    it's a todo  , in next update it will.
    """
    user = models.ForeignKey(verbose_name=_('User'), to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(verbose_name=_('Title'), max_length=255)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        :count: number of tags per user

        To limit the number of tag creations to a maximum of 5 per user
        """
        count = Tag.objects.filter(user=self.user).count()
        # Check if the user already has 5 categories
        if count >= 5:
            raise ValidationError(_("You have reached the maximum limit of tags."))

        super().save(*args, **kwargs)
