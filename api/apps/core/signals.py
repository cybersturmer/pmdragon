from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Project, \
    ProjectBacklog, \
    IssueTypeCategory, \
    IssueStateCategory


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
                                 title='Epic',
                                 is_subtask=False,
                                 is_default=False,
                                 ordering=0)

        epic.save()

        user_story = IssueTypeCategory(workspace=instance.workspace,
                                       project=instance,
                                       title='User Story',
                                       is_subtask=True,
                                       is_default=True,
                                       ordering=1)

        user_story.save()

        task = IssueTypeCategory(workspace=instance.workspace,
                                 project=instance,
                                 title='Task',
                                 is_subtask=True,
                                 is_default=False,
                                 ordering=2)

        task.save()

        bug = IssueTypeCategory(workspace=instance.workspace,
                                project=instance,
                                title='Bug',
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
                                  title='Todo',
                                  is_default=True,
                                  is_done=False)

        todo.save()

        in_progress = IssueStateCategory(workspace=instance.workspace,
                                         project=instance,
                                         title='In Progress',
                                         is_default=False,
                                         is_done=False)

        in_progress.save()

        verify = IssueStateCategory(workspace=instance.workspace,
                                    project=instance,
                                    title='Verify',
                                    is_default=False,
                                    is_done=False)

        verify.save()

        done = IssueStateCategory(workspace=instance.workspace,
                                  project=instance,
                                  title='Done',
                                  is_default=False,
                                  is_done=True)

        done.save()
