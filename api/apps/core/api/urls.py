from rest_framework import routers

from . import views

app_name = 'core_api'

router = routers.SimpleRouter()

router.register('projects', views.ProjectViewSet, basename='project')
router.register('issues', views.IssueViewSet, basename='issue')
router.register('issue/types', views.IssueTypeCategoryViewSet, basename='issue-type')
router.register('issue/states', views.IssueStateCategoryViewSet, basename='issue-state')
router.register('backlogs', views.ProjectBacklogViewSet,basename='backlog')
router.register('sprints', views.SprintViewSet, basename='sprint')
router.register('sprint/durations', views.SprintDurationViewSet, basename='sprint-duration')

urlpatterns = router.urls
