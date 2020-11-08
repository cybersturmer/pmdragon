from django.urls import path
from rest_framework import routers

from . import views

app_name = 'core_api'

router = routers.SimpleRouter()
router.register('projects', views.ProjectViewSet, basename='projects')
router.register('persons', views.CollaboratorsViewSet, basename='collaborators')
router.register('issues', views.IssueViewSet, basename='issues')
router.register('issue-types', views.IssueTypeCategoryViewSet, basename='issue-types')
router.register('issue-states', views.IssueStateCategoryViewSet, basename='issue-states')
router.register('backlogs', views.ProjectBacklogViewSet, basename='backlogs')
router.register('sprints', views.SprintViewSet, basename='sprints')
router.register('sprint-durations', views.SprintDurationViewSet, basename='sprint-durations')


urlpatterns = router.urls
urlpatterns += [path('issue/ordering/',
                     views.IssueListUpdateApiView.as_view(),
                     name='issue-ordering'),
                path('persons-invitations-requests/',
                     views.PersonInvitationRequestListCreateView.as_view(),
                     name='person-invitations-requests-list-create'),
                path('persons-invitations-requests/<key>/',
                     views.PersonInvitationRequestRetrieveUpdateView.as_view(),
                     name='person-invitations-requests-retrieve-update')]
