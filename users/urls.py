from django.urls import path
from . import views
urlpatterns = [
    path('cutoff',views.finalcutoff),
    path('displaycutoff',views.finaldisplaycutoff),
    path('predcollege',views.finalpredcollege),
    path('dispredcollege',views.disfinalpredcollege),
    path('predcourse',views.finalpredcourse),
    path('dispredcourse',views.disfinalpredcourse),
    path('kct',views.kct),
    path('diskct',views.diskct),
    path('rank',views.rank_form),
    path('disrank',views.disrank),
    path('',views.home),


]