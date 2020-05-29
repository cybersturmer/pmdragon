from rest_framework import routers

from . import views

app_name = 'core_api'

router = routers.SimpleRouter()

router.register('projects',
                views.ProjectViewSet,
                basename='project')

router.register('issue-type-categories',
                views.IssueTypeCategoryViewSet,
                basename='issue-type-category')

router.register('issue-state-categories',
                views.IssueStateCategoryViewSet,
                basename='issue-state-category')

router.register('issues',
                views.IssueViewSet,
                basename='issue')

router.register('project-backlogs',
                views.ProjectBacklogViewSet,
                basename='project-backlog')

router.register('sprint-durations',
                views.SprintDurationViewSet,
                basename='sprint-duration')

router.register('sprints',
                views.SprintViewSet,
                basename='sprint')

urlpatterns = router.urls

