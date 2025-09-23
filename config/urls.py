"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
#from utils.errors import graphql_format_error
import config.schema as schema_module
#from utils.errors import as_json_error
from django.http import JsonResponse
from django.contrib import admin
from django.urls import path



def health(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema_module.schema))),
    #path("graphql/", GraphQLView.as_view(graphiql=True, format_error=graphql_format_error)),
    path("health/", health),
]
