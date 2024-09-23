from django.urls import path
from . import views
from .views import PipelineView,ExtractiveQAView,DocumentOutlineView,upload_file


urlpatterns = [
     path('home/', views.home, name='home'),
     #path('query/', views.query, name='query'),
     path('pipeline/', PipelineView.as_view(), name='pipeline'),
     #path('query/', QueryView.as_view(), name='query'),
     #path('index/', IndexingView.as_view(), name='index'),
     path('extractiveqa/', ExtractiveQAView.as_view(), name='extractiveqa'),
     path('documentoutline/', DocumentOutlineView.as_view(), name='documentoutline'),
     path('upload/',views.upload_file,name='upload_file'),
     path('success/', views.success_view, name='success'),
]





