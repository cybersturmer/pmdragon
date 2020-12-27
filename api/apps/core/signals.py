from django.db.models import Q
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from .api.tasks import send_mentioned_in_message_email, \
    send_mentioned_in_description_email

from enum import Enum

from .models import Project, \
    ProjectBacklog, \
    IssueTypeCategory, \
    IssueStateCategory, \
    Sprint, \
    Issue, \
    IssueMessage, IssueEstimationCategory


class ActionM2M(Enum):
    PRE_ADD = 'pre_add'
    POST_ADD = 'post_add'
    PRE_REMOVE = 'pre_remove'
    POST_REMOVE = 'post_remove'
    PRE_CLEAR = 'pre_clear'
    POST_CLEAR = 'post_clear'


@receiver(post_save, sender=Issue)
def put_created_issue_to_backlog(instance: Issue, created: bool, **kwargs):
    """
    Lets put just created issue to Backlog.
    """
    if not created:
        return True

    backlog_with_same_workspace_and_project = ProjectBacklog.objects \
        .filter(workspace=instance.workspace,
                project=instance.project)

    if backlog_with_same_workspace_and_project.exists():
        backlog = backlog_with_same_workspace_and_project.get()
        backlog.issues.add(instance)


@receiver(post_save, sender=Project)
def create_backlog_for_project(instance: Project, created: bool, **kwargs):
    """
    Every project should contain only one Backlog.
    So we provide it.
    """
    project_backlog = ProjectBacklog.objects.filter(workspace=instance.workspace,
                                                    project=instance)

    if created and not project_backlog.exists():
        backlog = ProjectBacklog(workspace=instance.workspace,
                                 project=instance)
        backlog.save()


@receiver(post_save, sender=Project)
def create_default_issue_type_category_for_project(instance: Project, created: bool, **kwargs):
    """
    Every project should contain defaults Issue Types
    So we provide it.
    @todo Better to add default issue types based on current language of project
    """
    issue_types = IssueTypeCategory.objects.filter(workspace=instance.workspace,
                                                   project=instance)

    if created and not issue_types.exists():
        epic = IssueTypeCategory(workspace=instance.workspace,
                                 project=instance,
                                 title=_('Epic'),
                                 is_subtask=False,
                                 is_default=False,
                                 ordering=0)

        epic.save()

        user_story = IssueTypeCategory(workspace=instance.workspace,
                                       project=instance,
                                       title=_('User Story'),
                                       is_subtask=True,
                                       is_default=True,
                                       ordering=1)

        user_story.save()

        task = IssueTypeCategory(workspace=instance.workspace,
                                 project=instance,
                                 title=_('Task'),
                                 is_subtask=True,
                                 is_default=False,
                                 ordering=2)

        task.save()

        bug = IssueTypeCategory(workspace=instance.workspace,
                                project=instance,
                                title=_('Bug'),
                                is_subtask=False,
                                is_default=False,
                                ordering=3)

        bug.save()


@receiver(post_save, sender=Project)
def create_default_issue_state_category_for_project(instance: Project, created: bool, **kwargs):
    """
    Every project should contain issue states.
    So we provide it.
    @todo Better to add states based on current language of project
    """
    issue_states = IssueStateCategory.objects.filter(workspace=instance.workspace,
                                                     project=instance)

    if created and not issue_states.exists():
        todo = IssueStateCategory(workspace=instance.workspace,
                                  project=instance,
                                  title=_('Todo'),
                                  is_default=True,
                                  is_done=False)

        todo.save()

        in_progress = IssueStateCategory(workspace=instance.workspace,
                                         project=instance,
                                         title=_('In Progress'),
                                         is_default=False,
                                         is_done=False)

        in_progress.save()

        verify = IssueStateCategory(workspace=instance.workspace,
                                    project=instance,
                                    title=_('Verify'),
                                    is_default=False,
                                    is_done=False)

        verify.save()

        done = IssueStateCategory(workspace=instance.workspace,
                                  project=instance,
                                  title=_('Done'),
                                  is_default=False,
                                  is_done=True)

        done.save()


@receiver(post_save, sender=Project)
def create_default_issue_estimation_for_project(instance: Project, created: bool, **kwargs):
    issue_estimations = IssueEstimationCategory.objects.filter(workspace=instance.workspace,
                                                               project=instance)

    if created and not issue_estimations.exists():
        xs = IssueEstimationCategory(workspace=instance.workspace,
                                     project=instance,
                                     title=_('XS'),
                                     value=1)
        xs.save()

        sm = IssueEstimationCategory(workspace=instance.workspace,
                                     project=instance,
                                     title=_('SM'),
                                     value=2)
        sm.save()

        m = IssueEstimationCategory(workspace=instance.workspace,
                                    project=instance,
                                    title=_('M'),
                                    value=3)
        m.save()

        l_ = IssueEstimationCategory(workspace=instance.workspace,
                                     project=instance,
                                     title=_('L'),
                                     value=5)
        l_.save()

        xl = IssueEstimationCategory(workspace=instance.workspace,
                                     project=instance,
                                     title=_('XL'),
                                     value=8)
        xl.save()

        xxl = IssueEstimationCategory(workspace=instance.workspace,
                                      project=instance,
                                      title=_('XXL'),
                                      value=13)
        xxl.save()


@receiver(m2m_changed, sender=Sprint.issues.through)
@receiver(m2m_changed, sender=ProjectBacklog.issues.through)
def arrange_issue_in_sprints(sender, action, instance, **kwargs):
    """
    1) Find any sprints that have the same issues.
    2) Iterate all over sprints to remove issues that
    bind to sprint or Backlog from sprints.
    """
    if action != ActionM2M.POST_ADD.value:
        return True

    base_query = Q(issues__in=instance.issues.all())
    additional_query = {
        sender is Sprint.issues.through: ~Q(id=instance.pk),
        sender is ProjectBacklog.issues.through: Q()
    }[True]

    sprint_with_intersection_of_issues = Sprint.objects \
        .filter(base_query, additional_query)

    if not sprint_with_intersection_of_issues.exists():
        return True

    to_remove = instance.issues.values_list('id', flat=True)
    for _sprint in sprint_with_intersection_of_issues.all():
        _sprint.issues.remove(*to_remove)


@receiver(m2m_changed, sender=Sprint.issues.through)
def arrange_issue_in_backlog(action, instance, **kwargs):
    """
    1) Find Backlog that have same issues as sender Sprint.
    2) Remove that issues from Backlog.
    """

    """
    We need to track only post add action """
    if action != ActionM2M.POST_ADD.value:
        return True

    base_query = Q(workspace=instance.workspace) & Q(project=instance.project) & Q(issues__in=instance.issues.all())
    to_remove = instance.issues.values_list('id', flat=True)

    try:
        backlog = ProjectBacklog.objects.filter(base_query).get()
        backlog.issues.remove(*to_remove)

    except ProjectBacklog.DoesNotExist:
        pass


@receiver(post_save, sender=IssueMessage)
def signal_mentioned_in_message_emails(instance: IssueMessage, created: bool, **kwargs):
    """
    1) Check if someone was mentioned
    2) Send an email if someone was mentioned
    """

    if not created:
        return False

    send_mentioned_in_message_email.delay(instance.pk)


@receiver(post_save, sender=Issue)
def signal_mentioned_in_description_emails(instance: Issue, created: bool, **kwargs):
    """
    Send an email if someone was mentioned in issue description
    """
    if not created:
        return False

    send_mentioned_in_description_email.delay(instance.pk)
