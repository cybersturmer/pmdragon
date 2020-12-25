from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONOpenAPIRenderer
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import TokenRefreshView

from apps.core.api.views import PersonRegistrationRequestVerifyView, \
    PersonSetPasswordView, \
    UserUpdateView, \
    PersonAvatarUpload, \
    PersonRegistrationRequestView, \
    PersonInvitationRequestListView, \
    PersonInvitationRequestRetrieveUpdateView
from apps.core.api.views import TokenObtainPairExtendedView
from apps.core.views import SwaggerView

API_TITLE = 'PmDragon API'
API_DESCRIPTION = 'Web API for PmDragon service'
schema_url_patterns = [
    url(r'^api/', include('apps.core.api.urls'))
]

schema_view = get_schema_view(version=1,
                              title=API_TITLE,
                              description=API_DESCRIPTION,
                              renderer_classes=[JSONOpenAPIRenderer],
                              permission_classes=(AllowAny,))

urlpatterns = [
    path('admin/', admin.site.urls),

    path('schema/', schema_view, name='openapi-schema'),

    path('swagger/', SwaggerView.as_view()),

    path('api/auth/obtain/',
         TokenObtainPairExtendedView.as_view(),
         name='token_obtain_pair'),

    path('api/auth/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),

    path('api/auth/password/',
         PersonSetPasswordView.as_view(),
         name='person_update_password'),

    path('api/auth/persons/',
         PersonRegistrationRequestVerifyView.as_view(),
         name='person_create'),

    path('api/auth/person-registration-requests/',
         PersonRegistrationRequestView.as_view({'post': 'create'}),
         name='request-register'),

    path('api/auth/person-registration-requests/<key>/',
         PersonRegistrationRequestView.as_view({'get': 'retrieve'}),
         name='request-register'),

    path('api/auth/person-invitation-requests/',
         PersonInvitationRequestListView.as_view(),
         name='person-invitations-requests-list'),

    path('api/auth/person-invitation-requests/<key>/',
         PersonInvitationRequestRetrieveUpdateView.as_view(),
         name='person-invitations-requests-retrieve-update'),

    path('api/auth/me/',
         UserUpdateView.as_view(),
         name='me'),

    path('api/auth/password/',
         PersonSetPasswordView.as_view(),
         name='password'),

    path('api/auth/avatar/',
         PersonAvatarUpload.as_view(),
         name='avatar'),

    path('api/core/', include('apps.core.api.urls', namespace='core_api'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
