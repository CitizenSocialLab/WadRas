from django.conf.urls import patterns, url

import views
import views_game
import views_user
import views_admin
import views_ws

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

     url(r'^((?P<lang>[\w-]+)/)?$', views.index, name='index'),

     url(r'^((?P<lang>[\w-]+)/)?user$', views_user.index),
     url(r'^((?P<lang>[\w-]+)/)?user/logout$', views_user.logout, name="user.logout"),

     url(r'^((?P<lang>[\w-]+)/)?user/nickname$', views_user.nickname, name="user.nickname"),
     url(r'^((?P<lang>[\w-]+)/)?user/avis$', views_user.avis, name="user.avis"),
     url(r'^((?P<lang>[\w-]+)/)?user/enquesta1$', views_user.enquesta1, name="user.enquesta1"),

     url(r'^((?P<lang>[\w-]+)/)?user/inici', views_user.inici, name="user.inici"),
     url(r'^((?P<lang>[\w-]+)/)?user/registre', views_user.registre, name="user.registre"),

     url(r'^((?P<lang>[\w-]+)/)?user/final_joc', views_user.final_joc, name="user.final_joc"),

     url(r'^((?P<lang>[\w-]+)/)?game$', views_game.index, name='game.index'),
     url(r'^((?P<lang>[\w-]+)/)?game/presentacio$', views_game.presentacio, name='game.presentacio'),

     #############
     ### Admin
     url(r'^((?P<lang>[\w-]+)/)?admin$', views_admin.registre, name='admin.admin'),
     url(r'^((?P<lang>[\w-]+)/)?admin/users$', views_admin.users, name='admin.users'),
     url(r'^((?P<lang>[\w-]+)/)?admin/users_list$', views_admin.users_list, name='admin.users_list'),
     url(r'^((?P<lang>[\w-]+)/)?admin/users_results$', views_admin.users_results, name='admin.users_results'),
     url(r'^((?P<lang>[\w-]+)/)?admin/partida$', views_admin.partida, name='admin.partida'),
     url(r'^((?P<lang>[\w-]+)/)?admin/partida_list$', views_admin.partida_list, name='admin.partida_list'),
     url(r'^((?P<lang>[\w-]+)/)?ws/stats_partida_detail/(?P<num_partida>\d+)/', views_ws.stats_partida_detail, name='ws.stats_partida_detail'),
     url(r'^((?P<lang>[\w-]+)/)?ws/tancar_partida/(?P<num_partida>\d+)/', views_ws.tancar_partida, name='ws.tancar_partida'),

     #############


     url(r'^((?P<lang>[\w-]+)/)?admin/registre$', views_admin.registre, name='admin.registre'),
     url(r'^((?P<lang>[\w-]+)/)?admin/partida$', views_admin.partida, name='admin.partida'),
     url(r'^((?P<lang>[\w-]+)/)?admin/stats$', views_admin.stats, name='admin.stats'),
     url(r'^((?P<lang>[\w-]+)/)?admin/results$', views_admin.results, name='admin.results'),
     url(r'^((?P<lang>[\w-]+)/)?admin/users/reset/(?P<user_id>\d+)$', views_admin.users_reset, name='admin.users_reset'),
     url(r'^((?P<lang>[\w-]+)/)?admin/partida_detail/(?P<num_partida>\d+)/$', views_admin.partida_detail, name='admin.partida_detail'),

     url(r'^((?P<lang>[\w-]+)/)?ws/enviar_joc/(?P<id_joc>\d+)/', views_ws.enviar_joc, name='ws.enviar_joc'),
     url(r'^((?P<lang>[\w-]+)/)?ws/estat_partida/', views_ws.estat_partida, name='ws.estat_partida'),
     url(r'^((?P<lang>[\w-]+)/)?ws/estat_users/', views_ws.estat_users, name='ws.estat_users'),

     url(r'^((?P<lang>[\w-]+)/)?ws/llistat_partides/', views_ws.llistat_partides, name='ws.llistat_partides'),
     url(r'^((?P<lang>[\w-]+)/)?ws/stats_partida/', views_ws.stats_partida, name='ws.stats_partida'),
     url(r'^((?P<lang>[\w-]+)/)?ws/demanar_resultat_partida/', views_ws.demanar_resultat_partida, name='ws.demanar_resultat_partida'),

     url(r'^((?P<lang>[\w-]+)/)?ws/demanar_dades/(?P<user_id>\d+)/', views_ws.demanar_dades, name='ws.demanar_dades'),

    ######## Prisoner 1 ########
    url(r'^((?P<lang>[\w-]+)/)?user/joc_prisoner1_1', views_user.joc_prisoner1_1, name="user.joc_prisoner1_1"),
    url(r'^((?P<lang>[\w-]+)/)?user/joc_prisoner1_2', views_user.joc_prisoner1_2, name="user.joc_prisoner1_2"),
    url(r'^((?P<lang>[\w-]+)/)?user/joc_prisoner1_3', views_user.joc_prisoner1_3, name="user.joc_prisoner1_3"),

    url(r'^((?P<lang>[\w-]+)/)?ws/enviar_accio_prisoner1/(?P<user_id>\d+)/(?P<result>[\w-]+)',views_ws.enviar_accio_prisoner1, name='ws.enviar_accio_prisoner1'),
    url(r'^((?P<lang>[\w-]+)/)?ws/enviar_accio_guess1/(?P<user_id>\d+)/(?P<result>[\w-]+)',views_ws.enviar_accio_guess1, name='ws.enviar_accio_guess1'),
    url(r'^((?P<lang>[\w-]+)/)?ws/demanar_resultat_prisoner1/(?P<user_id>\d+)',views_ws.demanar_resultat_prisoner1, name='ws.demanar_resultat_prisoner1'),

    #########  Analysis  #########
     url(r'^((?P<lang>[\w-]+)/)?ws/basic_analysis/',views_ws.basic_analysis, name='ws.basic_analysis'),


)
