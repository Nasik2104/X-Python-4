from django.urls import path

from . import views

app_name = 'analysis'

urlpatterns = [
    path('index/', views.Index.as_view(), name='index'),
    path('csv_analysis/', views.CSVAnalysis.as_view(), name='csv-analysis')
]
