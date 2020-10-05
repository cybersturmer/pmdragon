from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONOpenAPIRenderer
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import TokenRefreshView

from apps.core.api.views import PersonRegistrationRequestCreateView, \
    PersonVerifyView, \
    PersonSetPasswordView, \
    WorkspaceReadOnlyViewSet, \
    PersonUpdateView
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
                              permission_classes=(AllowAny, ))

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

    path('api/auth/requests/',
         PersonRegistrationRequestCreateView.as_view(),
         name='request_create'),

    path('api/auth/password/',
         PersonSetPasswordView.as_view(),
         name='person_update_password'),

    path('api/auth/registrations/',
         PersonVerifyView.as_view(),
         name='request_update'),

    path('api/auth/workspaces/',
         WorkspaceReadOnlyViewSet.as_view({'get': 'list'}),
         name='workspaces'),

    path('api/auth/person/<int:pk>/',
         PersonUpdateView.as_view(),
         name='persons'),

    path('api/core/', include('apps.core.api.urls', namespace='core_api'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
