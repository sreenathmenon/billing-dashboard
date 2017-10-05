from django.conf.urls import patterns
from django.conf.urls import url

from billingdashboard.dashboards.project.plans import views

urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
)
