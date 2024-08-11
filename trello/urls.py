from django.urls import path
from .views import loginuser, registration, logoutuser, my_trello, trello_board, create_board, my_boards, add_member_to_board, staff_page, create_list, edit_list_card

urlpatterns = [
    path('login/', loginuser, name='login'),
    path('signup/', registration, name='signup'),
    path('logout/', logoutuser, name='logout'),
    # path('', admin_page, name='admin_page'),
    path('team_member_page/', staff_page, name='team_member_page'),
    path('my_trello/', my_trello, name='my_trello'),
    path('trello_board/<str:pk>/', trello_board, name='trello_board'),
    path('edit_list_card/', edit_list_card, name='edit_list_card'),
    path('trello_board/<str:pk>/create_list/<str:id>',
         create_list, name='create_list'),
    path('create_board/', create_board, name='create_board'),
    path('', my_boards, name='all_boards'),
    path('add_member/<str:pk>/', add_member_to_board, name='add_member'),

]
