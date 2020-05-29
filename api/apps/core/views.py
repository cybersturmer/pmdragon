from django.views.generic import TemplateView


class SwaggerView(TemplateView):
    template_name = 'core/swagger.html'
    extra_context = {'schema_url': 'openapi-schema'}

