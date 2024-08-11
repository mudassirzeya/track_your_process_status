from django.shortcuts import render, redirect
from django.contrib.auth.models import User
# sending email
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
import json
from .models import Add_Staff, Board, Board_Card, Company, Card_List, UserProfile
from .forms import RegisterForm, CompanyForm
from .password import PasswordSet
# from .password import PasswordSet
from django.http import JsonResponse

# reset password
from django.http import HttpResponse
# from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
# from django.contrib.auth.models import User
# from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
# from django.core.mail import EmailMultiAlternatives
from django.core.mail import BadHeaderError
from django import template
import time
# Create your views here.

# Create your views here.


def registration(request):
    form1 = CompanyForm()
    form2 = RegisterForm()
    if request.method == 'POST':
        form2 = RegisterForm(request.POST)
        # print("form2: ", form2)
        form1 = CompanyForm(request.POST)
        # print("form1: ", form1)
        username = request.POST.get('email')
        print("username: ", username)
        if form2.is_valid():
            # print("form2 valid")
            newuser_obj = form2.save(commit=False)
            # print("form2: ", newuser_obj)
            newuser_obj.username = username
            newuser_obj.save()
            if form1.is_valid():
                # print("form1 valid")
                company_obj = form1.save(commit=False)
                company_obj.super_user = newuser_obj
                company_obj.save()
                UserProfile.objects.create(
                    user=newuser_obj,
                    company=company_obj,
                    user_type='admin'
                )
                return redirect('login')
        else:
            print("form2 not valid")

    context = {"form1": form1, "form2": form2}
    return render(request, 'signup.html', context)


def loginuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            userprofile = UserProfile.objects.get(user=request.user)
            if userprofile.user_type == 'admin':
                return redirect('all_boards')
            elif userprofile.user_type == 'staff':
                return redirect('team_member_page')
        else:
            messages.info(request, 'Username or Password is in correct')
    context = {}
    return render(request, 'login.html', context)


def logoutuser(request):
    logout(request)
    return redirect('login')


# @login_required(login_url='login')
# def admin_page(request):
#     userprofile = UserProfile.objects.get(user=request.user)
#     company = Company.objects.get(super_user=request.user)
#     my_board = Board.objects.filter(company=company)
#     context = {"my_board": my_board, 'userprofile': userprofile}
#     return render(request, 'admin_page.html', context)


@login_required(login_url='login')
def staff_page(request):
    userprofile = UserProfile.objects.get(user=request.user)
    my_boards = Add_Staff.objects.filter(user=userprofile)
    context = {'my_boards': my_boards, 'userprofile': userprofile}
    return render(request, 'staff_page.html', context)


@login_required(login_url='login')
def my_trello(request):
    context = {}
    return render(request, 'my_trello.html', context)


@login_required(login_url='login')
def trello_board(request, pk):
    userprofile = UserProfile.objects.get(user=request.user)
    board = Board.objects.get(id=pk)
    board_card = Board_Card.objects.filter(board=board)
    # card_list = Card_List.objects.all()
    card_list_queryset = []
    final_card_list = []
    for card in board_card:
        # temp = {}
        this_card_list = Card_List.objects.filter(card=card)
        for list in this_card_list:
            card_list_queryset.append(list)
        # temp['list'] = this_card_list
        # final_card_list.append(temp)
    # print('loop', card_list_queryset)
    # numb = 0
    # for list in card_list_queryset:
    #     numb+1
    #     temp = {}
    #     temp['card_id'] = list[numb].card.id
    #     temp['text'] = list[numb].list_text
    #     final_card_list.append(temp)

    # print('list', final_card_list)
    if request.method == "POST":
        card_name = request.POST.get("card_name")
        Board_Card.objects.create(
            board=board,
            card_name=card_name,
        )
        return redirect("trello_board", pk=pk)
    context = {'board': board, 'board_card': board_card,
               'final_card_list': final_card_list,
               'card_list_queryset': card_list_queryset,
               'userprofile': userprofile}
    return render(request, 'trello_board.html', context)


@login_required(login_url='login')
def edit_list_card(request):
    if request.method == "POST":
        data = json.loads(request.body)
        board_data = data["data_obj"][0]
        board_card = Board_Card.objects.get(id=int(board_data['card']))
        card_list = Card_List.objects.get(id=int(board_data['list']))
        card_list.card = board_card
        card_list.save()
        return JsonResponse({"msg": "success"})
    context = {}
    return render(request, 'trello_board.html', context)


@login_required(login_url='login')
def create_list(request, pk, id):
    userprofile = UserProfile.objects.get(user=request.user)
    board = Board.objects.get(id=pk)
    board_card = Board_Card.objects.get(id=id)
    if request.method == "POST":
        list_text = request.POST.get("text")
        Card_List.objects.create(
            card=board_card,
            list_text=list_text,
        )
        return redirect("trello_board", pk=pk)
    context = {'board': board, 'board_card': board_card,
               'userprofile': userprofile}
    return render(request, 'trello_board.html', context)


# admin all boards
@login_required(login_url='login')
def my_boards(request):
    userprofile = UserProfile.objects.get(user=request.user)
    if userprofile.user_type != 'admin':
        return JsonResponse({"msg": "You dont have the Access"})
    company = Company.objects.get(super_user=request.user)
    my_board = Board.objects.filter(company=company)
    context = {"my_board": my_board, 'userprofile': userprofile}
    return render(request, 'my_boards.html', context)


@login_required(login_url='login')
def create_board(request):
    userprofile = UserProfile.objects.get(user=request.user)
    loggedin_user = Company.objects.get(super_user=request.user)
    if request.method == "POST":
        board_name = request.POST.get("board_name")
        Board.objects.create(
            company=loggedin_user,
            board_name=board_name,
        )
        return redirect("all_boards")
    context = {"userprofile": userprofile}
    return render(request, 'my_boards.html', context)


@login_required(login_url='login')
def add_member_to_board(request, pk):
    userprofile = UserProfile.objects.get(user=request.user)
    company = userprofile.company
    company_name = company.company_name
    board = Board.objects.get(id=pk)
    print(company_name)
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        passcode = PasswordSet()
        user, created = User.objects.get_or_create(username=email)

        if created:
            user.email = email
            user.first_name = name
            user.set_password(passcode)
            user.save()

            new_userprofile = UserProfile.objects.create(
                user=user,
                company=company,
                user_type='staff',
            )

            Add_Staff.objects.create(
                user=new_userprofile,
                associated_board=board,
            )

            msg_html = render_to_string('add_staff_email.html', {
                'first_name': name,
                'company': company_name,
                'username': email,
                'password': passcode
            })
            text_content = strip_tags(msg_html)

            email = EmailMultiAlternatives(
                # title
                f'Mail From {company_name} admin',
                # context
                text_content,
                # from email
                settings.EMAIL_HOST_USER,
                # to email
                [email],
            )
            email.attach_alternative(msg_html, "text/html")
            email.send()

            messages.info(request, "User Added Successfully!!")
        else:
            new_userprofile = UserProfile.objects.filter(user=user).first()
            if new_userprofile:
                exist_board_assigned = Add_Staff.objects.filter(
                    user=new_userprofile, associated_board=board).exists()
                print(new_userprofile, exist_board_assigned, board.board_name)
                if not exist_board_assigned:
                    Add_Staff.objects.create(
                        user=new_userprofile,
                        associated_board=board,
                    )
                    messages.info(request, "Board Assigned Successfully!!")
                else:
                    messages.info(
                        request, "This User Was Already Assigned To this Board")
        return redirect('all_boards')
    context = {'userprofile': userprofile}
    return render(request, 'my_boards.html', context)
