from django.urls import path
from django.utils.translation import ugettext_lazy
from rest_framework import routers, permissions
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from . import views

app_name = 'core_api'


def _(string: str) -> str:
    return str(ugettext_lazy(string))


@permission_classes((permissions.AllowAny,))
class DocsView(APIView):

    @staticmethod
    def get(request, *args, **kwargs):
        docs = {
            _('Registration requests'):
                request.build_absolute_uri('registration-requests'),

            _('Person create'):
                request.build_absolute_uri('persons/1dc4039fefa37e387d9ca0b88681b7ba8ad8cbdce'
                                           '297a8e33ed12b253cb5c6ae'),
        }

        return Response(docs)


urlpatterns = [
    path('', DocsView.as_view()),
    path('registration-requests/',
         views.PersonRegistrationRequestCreateView.as_view(),
         name='registration-requests_create'),

    path('persons/<key>/',
         views.PersonVerifyView.as_view(),
         name='registration-requests_approve'),
]

router = routers.DefaultRouter()

urlpatterns += router.urls
