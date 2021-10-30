from django.urls import path, include
from django.conf.urls import url

from rest_framework.authtoken.views import obtain_auth_token

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from myapi.core import views

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('user/', views.UserList.as_view(), name='show users'),
    path('user/api-token-auth/', obtain_auth_token, name='api_token_auth'),

    path('task/', views.TaskAPIView.as_view(), name='show tasks'),
    path('task/<int:pk>', views.TaskAPIViewDetailed.as_view(), name='show/edit task'),
    path('task/delete/<int:pk>', views.DeleteTaskAPIView.as_view(), name='show/edit task'),



]
