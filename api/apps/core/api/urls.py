from rest_framework import routers

from . import views

app_name = 'core_api'

router = routers.SimpleRouter()

router.register('projects', views.ProjectViewSet, basename='projects')
router.register('issues', views.IssueViewSet, basename='issues')
router.register('issue/types', views.IssueTypeCategoryViewSet, basename='issue-types')
router.register('issue/states', views.IssueStateCategoryViewSet, basename='issue-states')
router.register('backlogs', views.ProjectBacklogViewSet, basename='backlogs')
router.register('issues/ordering', views.ProjectBacklogIssueOrder, basename='issues-ordering')
router.register('sprints', views.SprintViewSet, basename='sprints')
router.register('sprint/durations', views.SprintDurationViewSet, basename='sprint-durations')

urlpatterns = router.urls
