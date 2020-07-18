from django import forms
from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Max
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from libs.cryptography import hashing
from libs.helpers.datetimepresets import day_later

url_validator = RegexValidator(r'^[a-z]{3,20}$',
                               _('From 3 to 20 english lowercase letters are allowed'))


class PersonRegistrationRequestValidManager(models.Manager):
    """
    Get not expired Person registration requests manager
    """
    def get_queryset(self):
        return super(PersonRegistrationRequestValidManager, self). \
            get_queryset(). \
            filter(expired_at__gt=timezone.now())


class PersonRegistrationRequest(models.Model):
    objects = models.Manager()
    valid = PersonRegistrationRequestValidManager()

    email = models.EmailField(verbose_name=_('Email'),
                              max_length=128)

    prefix_url = models.SlugField(verbose_name=_('Prefix URL'),
                                  help_text=_('String should contain from 3 to 20 small english letters '
                                              'without special chars'),
                                  validators=[url_validator],
                                  max_length=20)

    key = models.CharField(verbose_name=_('Registration key'),
                           db_index=True,
                           editable=False,
                           max_length=128)

    email_sent = models.BooleanField(verbose_name=_('Registration mail was successfully sent'),
                                     default=False)

    created_at = models.DateTimeField(verbose_name=_('Created at'),
                                      auto_now_add=True)

    expired_at = models.DateTimeField(verbose_name=_('Expired at'),
                                      db_index=True,
                                      default=day_later)

    class Meta:
        db_table = 'core_person_registration_request'
        ordering = ['-expired_at']

        indexes = (
            models.Index(fields=['key']),
            models.Index(fields=['key', '-expired_at'])
        )

        verbose_name = _('Person Registration Request')
        verbose_name_plural = _('Person Registration Requests')

    def __str__(self):
        return f'{self.email} - {self.prefix_url}'

    __repr__ = __str__

    def save(self, *args, **kwargs):
        if self.pk is None:
            raw_string = ''.join([str(self.expired_at), self.email, self.prefix_url])
            self.key = hashing.get_hash(raw_string)

        super(PersonRegistrationRequest, self).save(self, *args, **kwargs)


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
                                  help_text=_('String should contain from 3 to 20 small english letters '
                                              'without special chars'),
                                  validators=[url_validator],
                                  max_length=20)

    participants = models.ManyToManyField(Person,
                                          verbose_name=_('Participants of workplace'),
                                          related_name='workspaces',
                                          blank=True)

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
        return f'{self.workspace.prefix_url} - {self.title}'

    __repr__ = __str__


def is_project_in_workspace(workspace: Workspace, project: Project):
    if workspace != project.workspace:
        raise forms.ValidationError(_('Project should belong to given Workspace'))


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

    is_subtask = models.BooleanField(verbose_name=_('Is sub-task issue type?'),
                                     default=False)

    is_default = models.BooleanField(verbose_name=_('Is type set by default?'),
                                     default=False)

    ordering = models.PositiveSmallIntegerField(verbose_name=_('Ordering'),
                                                blank=True,
                                                null=True,
                                                default=0)

    class Meta:
        db_table = 'core_issue_category'
        ordering = ['ordering']
        unique_together = [
            ['workspace', 'title']
        ]
        verbose_name = _('Issue Type Category')
        verbose_name_plural = _('Issue Type Categories')

    def __str__(self):
        return f'{self.workspace.prefix_url} - {self.title}'

    __repr__ = __str__

    def clean(self):
        super(IssueTypeCategory, self).clean()
        is_project_in_workspace(self.workspace, self.project)

    def save(self, *args, **kwargs):
        if self.is_default:
            try:
                temp = IssueTypeCategory.objects \
                    .filter(workspace=self.workspace) \
                    .get(is_default=True)
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

    ordering = models.PositiveSmallIntegerField(verbose_name=_('Ordering'),
                                                blank=True,
                                                null=True,
                                                default=0)

    class Meta:
        db_table = 'core_issue_state'
        ordering = ['ordering']
        unique_together = [
            ['workspace', 'title']
        ]
        verbose_name = _('Issue State Category')
        verbose_name_plural = _('Issue State Categories')

    def __str__(self):
        return f'{self.workspace.prefix_url} - {self.title}'

    __repr__ = __str__

    def clean(self):
        super(IssueStateCategory, self).clean()
        is_project_in_workspace(self.workspace, self.project)

    def save(self, *args, **kwargs):
        if self.is_default:
            try:
                temp = IssueStateCategory.objects \
                    .filter(workspace=self.workspace) \
                    .get(is_default=True)
                if self != temp:
                    temp.is_default = False
                    temp.save()
            except IssueStateCategory.DoesNotExist:
                pass

        super(IssueStateCategory, self).save(*args, **kwargs)


class Issue(models.Model):
    workspace = models.ForeignKey(Workspace,
                                  verbose_name=_('Workspace'),
                                  db_index=True,
                                  on_delete=models.CASCADE)

    title = models.CharField(verbose_name=_('Title'),
                             max_length=255)

    project = models.ForeignKey(Project,
                                db_index=True,
                                verbose_name=_('Project'),
                                on_delete=models.CASCADE)

    type_category = models.ForeignKey(IssueTypeCategory,
                                      verbose_name=_('Issue Type Category'),
                                      db_index=True,
                                      blank=True,
                                      null=True,
                                      on_delete=models.CASCADE)

    state_category = models.ForeignKey(IssueStateCategory,
                                       verbose_name=_('Issue State Category'),
                                       db_index=True,
                                       blank=True,
                                       null=True,
                                       on_delete=models.SET_NULL)

    created_by = models.ForeignKey(Person,
                                   verbose_name=_('Created by'),
                                   on_delete=models.CASCADE)

    created_at = models.DateTimeField(verbose_name=_('Created at'),
                                      auto_now_add=True)

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
        return f'{self.workspace.prefix_url} - {self.project.title} - {self.title}'

    __repr__ = __str__

    def clean(self):
        super(Issue, self).clean()
        is_project_in_workspace(self.workspace, self.project)

    def save(self, *args, **kwargs):
        just_created = False

        if self.type_category is None or self.type_category == 0:
            """
            If default issue type was set for Workspace, we set it as a default
            """
            try:
                self.type_category = IssueTypeCategory.objects \
                    .filter(workspace=self.workspace,
                            is_default=True).get()
            except IssueTypeCategory.DoesNotExist:
                pass

        if self.state_category is None or self.type_category == 0:
            """
            If default issue state was set for Workspace, we set it as a default
            """
            try:
                self.state_category = IssueStateCategory.objects \
                    .filter(workspace=self.workspace,
                            is_default=True).get()
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

        if self.pk is None:
            """
            If we just created issue - we have to add it into 
            Workspace - Project Backlog
            Before object creation we put this flag.
            """
            just_created = True

        super(Issue, self).save(*args, **kwargs)

        if just_created:
            """
            If we created this issue in this session 
            we have to put it to Workspace - Project Backlog
            """
            backlog = ProjectBacklog.objects \
                .filter(workspace=self.workspace,
                        project=self.project) \
                .get()

            assert isinstance(backlog, ProjectBacklog)

            backlog.issues.add(self)


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
        super(ProjectBacklog, self).clean()
        is_project_in_workspace(self.workspace, self.project)


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
                                      null=True,
                                      default=None)

    finished_at = models.DateTimeField(verbose_name=_('End date'),
                                       null=True,
                                       default=None)

    class Meta:
        db_table = 'core_sprint'
        unique_together = [
            ['workspace', 'project', 'started_at'],
            ['workspace', 'project', 'finished_at'],
        ]
        verbose_name = _('Sprint')
        verbose_name_plural = _('Sprints')

    def __str__(self):
        return f'{self.workspace.prefix_url} - {self.title}'

    __repr__ = __str__

    def clean(self):
        super(Sprint, self).clean()

        is_project_in_workspace(self.workspace, self.project)

        if None not in [self.started_at, self.finished_at] and self.started_at >= self.finished_at:
            raise forms.ValidationError(_('Date of start should be earlier than date of end'))

        if self.is_started:
            try:
                """
                Checking if we have another one started sprint
                """
                temp = Sprint.objects \
                    .filter(workspace=self.workspace,
                            project=self.project,
                            is_started=True) \
                    .get()

                if self != temp:
                    raise forms.ValidationError(_('Another sprint was already started. '
                                                  'Complete it before start the new one'))

            except IssueTypeCategory.DoesNotExist:
                pass

            if None in [self.started_at, self.finished_at]:
                """
                Started sprint should contain information about start and finish dates
                Its not necessary for draft of sprint (Not started yet)
                """
                raise forms.ValidationError(_('Start date and End date are required for started sprint'))
