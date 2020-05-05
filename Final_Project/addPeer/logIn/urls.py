from django.urls import path
from . import views


urlpatterns = [
          path('', views.home, name='home'), 
          path('logIn', views.logIn, name= 'logIn'),    
          path('backToInsert', views.backToInsert, name= 'backToInsert'),   
          path('addPeer', views.addPeer, name= 'addPeer'),
          path('logOut', views.logOut, name= 'logOut'),
          path('returnData', views.returnActivityData, name= 'returnData'),
		]