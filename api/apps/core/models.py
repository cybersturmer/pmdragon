import os
import uuid
from enum import Enum

import bleach
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Max, F
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import re

from libs.cryptography import hashing
from libs.helpers.datetimepresets import day_later

url_validator = RegexValidator(r'^[a-zA-Z0-9]{3,20}$',
                               _('From 3 to 20 letters and numbers are allowed'))


class UploadPersonsDirections(Enum):
    AVATAR = 'avatar'


def image_upload_location(instance, filename) -> str:
    """
    Getting prefix by checking is it instance of ..."""
    direction = {
        isinstance(instance, Person): UploadPersonsDirections.AVATAR.value
    }[True]

    name, extension = os.path.splitext(filename)
    uniq_name = uuid.uuid4().hex

    path = f'person_{instance.user.id}/images/{direction}_{uniq_name}{extension}'

    return path


def clean_useless_newlines(data):
    return data.replace('<p></p>', '')


def clean_html(data):
    return bleach \
        .clean(data,
               tags=settings.BLEACH_ALLOWED_TAGS,
               attributes=settings.BLEACH_ALLOWED_ATTRIBUTES,
               protocols=settings.BLEACH_ALLOWED_PROTOCOLS,
               strip=settings.BLEACH_STRIPPING)


def get_mentioned_user_ids(data):
    return re.findall(r'data-mentioned-user-id="(\d{1,10})"', data)


class Person(models.Model):
    """
    Person should be connected to user.
    Person can be invited, but have to fill of this information by himself
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                verbose_name=_('User of system'),
                                on_delete=models.CASCADE,
                                related_name='person')

    phone = models.CharField(max_length=128,
                             verbose_name=_('Phone number'),
                             null=True,
                             blank=True)

    updated_at = models.DateTimeField(verbose_name=_('Updated at'),
                                      auto_now=True)

    avatar = models.ImageField(
        upload_to=image_upload_location,
        null=True
    )

    @property
    def username(self):
        return self.user.username

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def email(self):
        return self.user.email

    @property
    def is_active(self):
        return self.user.is_active

    @property
    def created_at(self):
        return self.user.date_joined

    class Meta:
        db_table = 'core_person'
        ordering = ['-updated_at']
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

    def __str__(self):
        email = self.username
        result_name = email

        if self.first_name and self.last_name:
            result_name = f'{self.first_name} {self.last_name}'

        return result_name

    __repr__ = __str__


class Workspace(models.Model):
    """
    Workspaces allow system to isolate teams between each other.
    Managers or analytics can work separately from main team,
    but also need a self scrum board.
    """
    prefix_url = models.CharField(verbose_name=_('Prefix URL'),
                                  db_index=True,
                                  unique=True,
                                  help_text=_('String should contain from 3 to 20 letters and numbers '
                                              'without special chars'),
                                  validators=[url_validator],
                                  max_length=20)

    participants = models.ManyToManyField(Person,
                                          verbose_name=_('Participants of workplace'),
                                          related_name='workspaces',
                                          blank=True)

    created_by = models.ForeignKey(Person,
                                   verbose_name=_('Owner'),
                                   null=True,
                                   on_delete=models.SET_NULL)

    created_at = models.DateTimeField(verbose_name=_('Created at'),
                                      auto_now_add=True)

    class Meta:
        db_table = 'core_workspace'
        ordering = ['-created_at']
        verbose_name = _('Workspace')
        verbose_name_plural = _('Workspaces')

    def __str__(self):
        return self.prefix_url

    __repr__ = __str__


class PersonParticipationRequestAbstractValidManager(models.Manager):
    """
    Get not expired Person registration requests manager
    We also have to filter already accepted requests.
    """

    def get_queryset(self):
        return super(). \
            get_queryset(). \
            filter(expired_at__gt=timezone.now(),
                   is_accepted=False)


class PersonParticipationRequestAbstract(models.Model):
    """
    Abstract class to extend by all requests.
    """
    objects = models.Manager()
    valid = PersonParticipationRequestAbstractValidManager()

    key = models.CharField(verbose_name=_('Registration key'),
                           db_index=True,
                           editable=False,
                           max_length=128)

    is_email_sent = models.BooleanField(verbose_name=_('Registration mail was successfully sent'),
                                        default=False)

    is_accepted = models.BooleanField(verbose_name=_('Was collaboration request approved?'),
                                      default=False)

    created_at = models.DateTimeField(verbose_name=_('Created at'),
                                      auto_now_add=True)

    expired_at = models.DateTimeField(verbose_name=_('Expired at'),
                                      db_index=True,
                                      default=day_later)

    class Meta:
        abstract = True
        ordering = ['-expired_at']

        indexes = (
            models.Index(fields=['key']),
            models.Index(fields=['key', '-expired_at'])
        )

    def __str__(self):
        return str(self.pk)

    __repr__ = __str__


class PersonRegistrationRequest(PersonParticipationRequestAbstract):
    """
    Normal registration when user try to get workspace url and input
    email.
    These persons are not registered yet in PmDragon.
    """

    email = models.EmailField(verbose_name=_('Email'),
                              max_length=128)

    prefix_url = models.SlugField(verbose_name=_('Prefix URL'),
                                  help_text=_('String should contain from 3 to 20 small english letters '
                                              'without special chars'),
                                  validators=[url_validator],
                                  max_length=20)

    class Meta:
        db_table = 'core_person_registration_request'
        verbose_name = _('Person Registration Request')
        verbose_name_plural = _('Person Registration Requests')

    def __str__(self):
        return f'{self.prefix_url} - {self.email}'

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.key = hashing.get_hash(self.expired_at, self.email, self.prefix_url)

        super().save(*args, **kwargs)


class PersonInvitationRequest(PersonParticipationRequestAbstract):
    """
    Request for invitation of person that are not registered in PmDragon yet, with given email.
    These users don't want to create their own workspace.
    """

    email = models.EmailField(verbose_name=_('Email'),
                              max_length=128)

    workspace = models.ForeignKey(Workspace,
                                  verbose_name=_('Workspace'),
                                  on_delete=models.CASCADE)

    class Meta:
        db_table = 'core_person_invitation_request'
        verbose_name = _('Person Invitation Request')
        verbose_name_plural = _('Person Invitation Requests')

    def __str__(self):
        return f'{self.workspace.prefix_url} - {self.email}'

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.key = hashing.get_hash(self.expired_at, self.email, self.workspace.prefix_url)

        super().save(*args, **kwargs)


class Project(models.Model):
    """
    Project is a easiest way to isolate Tasks
    """
    workspace = models.ForeignKey(Workspace,
                                  verbose_name=_('Workspace'),
                                  db_index=True,
                                  on_delete=models.CASCADE,
                                  related_name='projects')

    title = models.CharField(verbose_name=_('Title'),
                             max_length=255)

    key = models.SlugField(verbose_name=_('Project key'),
                           help_text=_('Short word (must not exceed 10 characters) to mark project'),
                           max_length=10)

    created_at = models.DateTimeField(verbose_name=_('Created at'),
                                      auto_now_add=True)

    class Meta:
        db_table = 'core_project'
        ordering = ['-created_at']
        unique_together = [
            ['workspace', 'title'],
            ['workspace', 'key']
        ]
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    def __str__(self):
        return f'[ {self.workspace.prefix_url} - {self.title} ]'

    __repr__ = __str__


class IssueTypeCategoryIcons(models.Model):
    prefix = models.CharField(verbose_name=_('Icon prefix'),
                              max_length=50,
                              unique=True,
                              db_index=True)

    color = models.CharField(verbose_name=_('Icon color'),
                             max_length=50,
                             null=True,
                             blank=True)

    ordering = models.PositiveSmallIntegerField(verbose_name=_('Ordering'),
                                                blank=True,
                                                null=True,
                                                default=0)

    class Meta:
        db_table = 'core_issue_type_icon'
        ordering = ['ordering']
        verbose_name = _('Issue Type Icon')
        verbose_name_plural = _('Issue Type Icons')

    def __str__(self):
        return self.prefix

    __repr__ = __str__


class IssueTypeCategory(models.Model):
    workspace = models.ForeignKey(Workspace,
                                  verbose_name=_('Workspace'),
                                  db_index=True,
                                  on_delete=models.CASCADE,
                                  related_name='issue_categories')

    project = models.ForeignKey(Project,
                                db_index=True,
                                verbose_name=_('Project'),
                                on_delete=models.CASCADE)

    title = models.CharField(verbose_name=_('Title'),
                             max_length=255)

    icon = models.ForeignKey(IssueTypeCategoryIcons,
                             verbose_name=_('Icon'),
                             on_delete=models.SET_NULL,
                             null=True)

    is_subtask = models.BooleanField(verbose_name=_('Is sub-task issue type?'),
                                     default=False)

    is_default = models.BooleanField(verbose_name=_('Is type set by default?'),
                                     default=False)

    ordering = models.PositiveSmallIntegerField(verbose_name=_('Ordering'),
                                                blank=True,
                                                null=True,
                                                default=0)

    class Meta:
        db_table = 'core_issue_type'
        ordering = ['ordering']
        unique_together = [
            ['project', 'title']
        ]
        verbose_name = _('Issue Type Category')
        verbose_name_plural = _('Issue Type Categories')

    def __str__(self):
        return f'{self.project} - {self.title}'

    __repr__ = __str__

    def clean(self):
        try:
            self.workspace = self.project.workspace
        except Project.DoesNotExist:
            pass

        super(IssueTypeCategory, self).clean()

    def save(self, *args, **kwargs):
        if self.is_default:
            try:
                temp = IssueTypeCategory.objects \
                    .filter(workspace=self.workspace,
                            project=self.project,
                            is_default=True) \
                    .get()

                if self != temp:
                    temp.is_default = False
                    temp.save()
            except IssueTypeCategory.DoesNotExist:
                pass

        super(IssueTypeCategory, self).save(*args, **kwargs)


class IssueStateCategory(models.Model):
    workspace = models.ForeignKey(Workspace,
                                  verbose_name=_('Workspace'),
                                  db_index=True,
                                  on_delete=models.CASCADE)

    project = models.ForeignKey(Project,
                                db_index=True,
                                verbose_name=_('Project'),
                                on_delete=models.CASCADE)

    title = models.CharField(verbose_name=_('Title'),
                             max_length=255)

    is_default = models.BooleanField(verbose_name=_('Is type set by default?'),
                                     default=False)

    is_done = models.BooleanField(verbose_name=_('Is done state?'),
                                  help_text=_('Is task completed when moved to this column?'),
                                  default=False)

    ordering = models.PositiveSmallIntegerField(verbose_name=_('Ordering'),
                                                blank=True,
                                                null=True,
                                                default=0)

    class Meta:
        db_table = 'core_issue_state'
        ordering = ['ordering']
        unique_together = [
            ['project', 'title']
        ]
        verbose_name = _('Issue State Category')
        verbose_name_plural = _('Issue State Categories')

    def __str__(self):
        return f'{self.project} - {self.title}'

    __repr__ = __str__

    def clean(self):
        try:
            self.workspace = self.project.workspace
        except Project.DoesNotExist:
            pass

        super(IssueStateCategory, self).clean()

    def save(self, *args, **kwargs):
        """
        There is only one task in a project with:
        1) Done
        2) Default as state
        So we have to control it carefully
        """
        if self.is_default:
            default_issue_states = IssueStateCategory.objects \
                .filter(workspace=self.workspace,
                        project=self.project,
                        is_default=True) \
                .all()

            for state in default_issue_states:
                if state == self:
                    continue

                state.is_default = False
                state.save()

        if self.is_done:
            done_issue_states = IssueStateCategory.objects \
                .filter(workspace=self.workspace,
                        project=self.project,
                        is_done=True) \
                .all()

            for state in done_issue_states:
                if state == self:
                    continue

                state.is_done = False
                state.save()

        super(IssueStateCategory, self).save(*args, **kwargs)


class IssueEstimationCategory(models.Model):
    workspace = models.ForeignKey(Workspace,
                                  verbose_name=_('Workspace'),
                                  db_index=True,
                                  on_delete=models.CASCADE)

    project = models.ForeignKey(Project,
                                db_index=True,
                                verbose_name=_('Project'),
                                on_delete=models.CASCADE)

    title = models.CharField(verbose_name=_('Title'),
                             max_length=255,
                             help_text=_('You can call it by T-shirt size or like banana'))

    value = models.IntegerField(verbose_name=_('Value'),
                                help_text=_('This value is for calculating team velocity'))

    created_at = models.DateTimeField(verbose_name=_('Created at'),
                                      auto_now_add=True)

    updated_at = models.DateTimeField(verbose_name=_('Updated at'),
                                      auto_now=True)

    class Meta:
        db_table = 'core_issue_estimation'
        ordering = ['value']
        unique_together = [
            ['workspace', 'project', 'title'],
            ['workspace', 'project', 'value']
        ]
        verbose_name = _('Issue Estimation')
        verbose_name_plural = _('Issue Estimations')

    def __str__(self):
        return f'{self.title} {self.value}'

    __repr__ = __str__


class Issue(models.Model):
    cleaned_data: dict

    workspace = models.ForeignKey(Workspace,
                                  verbose_name=_('Workspace'),
                                  db_index=True,
                                  on_delete=models.CASCADE)

    project = models.ForeignKey(Project,
                                db_index=True,
                                verbose_name=_('Project'),
                                on_delete=models.CASCADE)

    title = models.CharField(verbose_name=_('Title'),
                             max_length=255)

    description = models.TextField(verbose_name=_('Description'),
                                   blank=True)

    type_category = models.ForeignKey(IssueTypeCategory,
                                      verbose_name=_('Type Category'),
                                      db_index=True,
                                      blank=True,
                                      null=True,
                                      on_delete=models.CASCADE)

    state_category = models.ForeignKey(IssueStateCategory,
                                       verbose_name=_('State Category'),
                                       db_index=True,
                                       blank=True,
                                       null=True,
                                       on_delete=models.SET_NULL)

    estimation_category = models.ForeignKey(IssueEstimationCategory,
                                            verbose_name=_('Story Point Estimation'),
                                            db_index=True,
                                            blank=True,
                                            null=True,
                                            on_delete=models.SET_NULL)

    assignee = models.ForeignKey(Person,
                                 verbose_name=_('Assignee'),
                                 db_index=True,
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 related_name='assigned_issues')

    created_by = models.ForeignKey(Person,
                                   verbose_name=_('Created by'),
                                   on_delete=models.CASCADE,
                                   related_name='created_issues')

    created_at = models.DateTimeField(verbose_name=_('Created at'),
                                      auto_now_add=True)

    updated_at = models.DateTimeField(verbose_name=_('Updated at'),
                                      auto_now=True)

    ordering = models.PositiveSmallIntegerField(verbose_name=_('Ordering'),
                                                blank=True,
                                                null=True,
                                                default=0)

    class Meta:
        db_table = 'core_issue'
        ordering = ['ordering']
        unique_together = [
            ['workspace', 'title', 'project']
        ]
        verbose_name = _('Issue')
        verbose_name_plural = _('Issues')

    def __str__(self):
        return f'#{self.id} {self.workspace.prefix_url} - {self.project.title} - {self.title}'

    __repr__ = __str__

    def clean(self):
        try:
            self.workspace = self.project.workspace
        except Project.DoesNotExist:
            pass

        super(Issue, self).clean()

        self.description = clean_useless_newlines(clean_html(self.description))

        """
        We have to check that we use the state category and type category
        from issue project.
        Also Type category and state category can to be None,
        so we can skip it in this case.
        """

        try:
            is_type_category_correct = bool(self.type_category is None) or \
                                       bool(self.project == self.type_category.project)
        except (Project.DoesNotExist, IssueTypeCategory.DoesNotExist):
            is_type_category_correct = True

        try:
            is_state_category_correct = bool(self.state_category is None) or \
                                        bool(self.project == self.state_category.project)
        except (Project.DoesNotExist, IssueStateCategory.DoesNotExist):
            is_state_category_correct = True

        workspace_checklist = [
            is_type_category_correct,
            is_state_category_correct,
        ]

        if False in workspace_checklist:
            raise ValidationError(_('Issue type category, '
                                    'state category should belong to the same project'))

    def save(self, *args, **kwargs):
        if self.type_category is None or self.type_category == 0:
            """
            If default issue type was set for Workspace, we set it as a default
            """
            try:
                self.type_category = IssueTypeCategory.objects \
                    .filter(workspace=self.workspace,
                            project=self.project,
                            is_default=True).get()
            except IssueTypeCategory.DoesNotExist:
                pass

        if self.state_category is None or self.type_category == 0:
            """
            If default issue state was set for Workspace, we set it as a default
            """
            try:
                default_state = IssueStateCategory.objects \
                    .filter(workspace=self.workspace,
                            project=self.project,
                            is_default=True).get()

                self.state_category = default_state

            except IssueStateCategory.DoesNotExist:
                pass

        if self.ordering is None:
            """
            Set the biggest value for current workspace to order
            """
            try:
                max_ordering = Issue.objects \
                    .filter(workspace=self.workspace) \
                    .aggregate(Max('ordering')) \
                    .get('ordering__max')
            except Issue.DoesNotExist:
                pass

            else:
                self.ordering = max_ordering

        super(Issue, self).save(*args, **kwargs)


class IssueMessage(models.Model):
    cleaned_data: dict

    workspace = models.ForeignKey(Workspace,
                                  verbose_name=_('Workspace'),
                                  db_index=True,
                                  on_delete=models.CASCADE)

    project = models.ForeignKey(Project,
                                verbose_name=_('Project'),
                                on_delete=models.CASCADE)

    created_by = models.ForeignKey(Person,
                                   verbose_name=_('Sent by'),
                                   on_delete=models.CASCADE,
                                   related_name='sent_messages')

    issue = models.ForeignKey(Issue,
                              verbose_name=_('Issue'),
                              on_delete=models.CASCADE,
                              related_name='messages')

    description = models.TextField(verbose_name=_('Description'),
                                   blank=True)

    created_at = models.DateTimeField(verbose_name=_('Created at'),
                                      auto_now_add=True)

    updated_at = models.DateTimeField(verbose_name=_('Updated at'),
                                      auto_now=True)

    class Meta:
        db_table = 'core_issue_message'
        ordering = [
            'created_at'
        ]
        verbose_name = _('Issue Message')
        verbose_name_plural = _('Issue Messages')

    def __str__(self):
        return f'#{self.pk} - {self.created_by.first_name} {self.created_by.last_name} <{len(self.description)} chars>'

    __repr__ = __str__

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.workspace = self.issue.workspace
            self.project = self.issue.project

        self.description = clean_useless_newlines(clean_html(self.description))

        super().save(*args, **kwargs)


class ProjectBacklog(models.Model):
    workspace = models.ForeignKey(Workspace,
                                  verbose_name=_('Workspace'),
                                  db_index=True,
                                  on_delete=models.CASCADE)

    project = models.OneToOneField(Project,
                                   verbose_name=_('Project'),
                                   on_delete=models.CASCADE)

    issues = models.ManyToManyField(Issue,
                                    verbose_name=_('Issues'),
                                    blank=True)

    class Meta:
        db_table = 'core_project_backlog'
        unique_together = [
            ['workspace', 'project']
        ]
        verbose_name = _('Project Backlog')
        verbose_name_plural = _('Project Backlogs')

    def __str__(self):
        return f'{self.workspace.prefix_url} - {self.project.title} {_("Backlog")} ' \
               f'| ({self.issues.count()}) {_("issues")}'

    __repr__ = __str__

    def clean(self):
        for _issue in self.issues.all():
            if _issue.workspace != self.workspace or _issue.project != self.project:
                raise ValidationError(_('Issues must be assigned to the same Project and Workspace as Backlog'))

        try:
            self.workspace = self.project.workspace
        except Project.DoesNotExist:
            pass

        super(ProjectBacklog, self).clean()


class SprintDuration(models.Model):
    workspace = models.ForeignKey(Workspace,
                                  verbose_name=_('Workspace'),
                                  db_index=True,
                                  on_delete=models.CASCADE)

    title = models.CharField(verbose_name=_('Title'),
                             max_length=255)

    duration = models.DurationField(verbose_name=_('Duration'))

    class Meta:
        db_table = 'core_sprint_duration'
        unique_together = [
            ['workspace', 'title'],
        ]
        verbose_name = _('Sprint duration')
        verbose_name_plural = _('Sprints duration')

    def __str__(self):
        return f'{self.workspace.prefix_url} - {self.title}'

    __repr__ = __str__


class Sprint(models.Model):
    workspace = models.ForeignKey(Workspace,
                                  verbose_name=_('Workspace'),
                                  db_index=True,
                                  on_delete=models.CASCADE)

    project = models.ForeignKey(Project,
                                verbose_name=_('Project'),
                                db_index=True,
                                on_delete=models.CASCADE)

    title = models.CharField(verbose_name=_('Title'),
                             max_length=255,
                             blank=True,
                             default=_("New Sprint"))

    goal = models.TextField(verbose_name=_('Sprint Goal'),
                            max_length=255,
                            blank=True)

    issues = models.ManyToManyField(Issue,
                                    verbose_name=_('Issues'),
                                    blank=True)

    is_started = models.BooleanField(verbose_name=_('Is sprint started'),
                                     default=False)

    is_completed = models.BooleanField(verbose_name=_('Is sprint completed'),
                                       default=False)

    started_at = models.DateTimeField(verbose_name=_('Start date'),
                                      blank=True,
                                      null=True)

    finished_at = models.DateTimeField(verbose_name=_('End date'),
                                       blank=True,
                                       null=True)

    class Meta:
        db_table = 'core_sprint'
        unique_together = [
            ['workspace', 'project', 'started_at'],
            ['workspace', 'project', 'finished_at'],
        ]
        ordering = [
            F('finished_at').asc(nulls_last=True)
        ]
        verbose_name = _('Sprint')
        verbose_name_plural = _('Sprints')

    def __str__(self):
        return f'#{self.id} {self.workspace.prefix_url} - {self.title}'

    __repr__ = __str__

    def clean(self):

        for _issue in self.issues.all():
            if _issue.workspace != self.workspace or _issue.project != self.project:
                raise ValidationError(_('Issues must be assigned to the same Project and Workspace as Sprint'))

        try:
            self.workspace = self.project.workspace
        except Project.DoesNotExist:
            pass

        super(Sprint, self).clean()

        if None not in [self.started_at, self.finished_at] and self.started_at >= self.finished_at:
            raise ValidationError(_('Date of start should be earlier than date of end'))

        if self.is_started:
            try:
                """
                Checking if we have another one started sprint
                """
                started_sprints_amount = \
                    Sprint.objects \
                        .filter(workspace=self.workspace,
                                project=self.project,
                                is_started=True) \
                        .exclude(pk=self.pk) \
                        .count()

                if started_sprints_amount > 0:
                    raise ValidationError(_('Another sprint was already started. '
                                            'Complete it before start the new one'))

            except Sprint.DoesNotExist:
                pass

            if None in [self.started_at, self.finished_at]:
                """
                Started sprint should contain information about start and finish dates
                Its not necessary for draft of sprint (Not started yet) """
                raise ValidationError(_('Start date and End date are required for started sprint'))

    def delete(self, using=None, keep_parents=False):
        """
        After deleting sprint we have to send it to backlog
        in the same workspace and project. """

        backlog = ProjectBacklog.objects \
            .filter(workspace=self.workspace,
                    project=self.project) \
            .get()

        for _issue in self.issues.all():
            backlog.issues.add(_issue)

        super(Sprint, self).delete(using, keep_parents)
