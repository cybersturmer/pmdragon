from django.db.models import Q
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from .models import Project, \
    ProjectBacklog, \
    IssueTypeCategory, \
    IssueStateCategory, Sprint


@receiver(post_save, sender=Project)
def create_backlog_for_project(sender, **kwargs):
    instance: Project = kwargs.get('instance')
    created: bool = kwargs.get('created')

    project_backlog = ProjectBacklog.objects.filter(workspace=instance.workspace,
                                                    project=instance)

    if created and not project_backlog.exists():
        backlog = ProjectBacklog(workspace=instance.workspace,
                                 project=instance)
        backlog.save()


@receiver(post_save, sender=Project)
def create_default_issue_type_category_for_project(sender, **kwargs):
    instance: Project = kwargs.get('instance')
    created: bool = kwargs.get('created')

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
def create_default_issue_state_category_for_project(sender, **kwargs):
    instance: Project = kwargs.get('instance')
    created: bool = kwargs.get('created')

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


@receiver(m2m_changed, sender=Sprint.issues.through)
@receiver(m2m_changed, sender=ProjectBacklog.issues.through)
def arrange_issue_in_sprints(sender, **kwargs):
    """
    1) find any sprints that have the same issues.
    2) Iterate all over sprints to remove issues that
    bind to sprint or Backlog from sprints.
    """
    instance: [Sprint, ProjectBacklog] = kwargs.get('instance')
    action = kwargs.get('action')

    if action != 'post_add':
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
def arrange_issue_in_backlog(sender, **kwargs):
    """
    1) Find Backlog that have same issues as sender Sprint.
    2) Remove that issues from Backlog.
    """
    instance: Sprint = kwargs['instance']
    action = kwargs.get('action')

    if action != 'post_add':
        return True

    base_query = Q(workspace=instance.workspace) & Q(project=instance.project) & Q(issues__in=instance.issues.all())

    to_remove = instance.issues.values_list('id', flat=True)

    try:
        backlog = ProjectBacklog.objects.filter(base_query).get()
        backlog.issues.remove(*to_remove)

    except ProjectBacklog.DoesNotExist:
        pass
