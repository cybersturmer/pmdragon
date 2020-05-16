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
            _('Person registration request create'):
                request.build_absolute_uri('person-registration-requests'),

            _('Person list'):
                request.build_absolute_uri('persons')
        }

        return Response(docs)


urlpatterns = [
    path('', DocsView.as_view()),
    path('person-registration-requests/',
         views.PersonRegistrationRequestCreateView.as_view(),
         name='person-registration-requests')
]

router = routers.DefaultRouter()
router.register('persons', views.PersonViewSet)

urlpatterns += router.urls
