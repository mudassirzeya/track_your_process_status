from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Company(models.Model):
    super_user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    profile_pic = models.ImageField(
        default="profile1.jpg", null=True, blank=True)

    def __str__(self):
        return self.company_name


class UserProfile(models.Model):
    USERTYPE = (
        ('staff', 'staff'),
        ('admin', 'admin'),
    )
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE
    )
    company = models.ForeignKey(
        Company, null=True, blank=True, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        default="profile1.jpg", null=True, blank=True)
    user_type = models.CharField(max_length=100, blank=True, choices=USERTYPE)

    def __str__(self):
        return str(self.user)


class Board(models.Model):
    company = models.ForeignKey(
        Company, null=True, blank=True, on_delete=models.CASCADE
    )
    board_name = models.CharField(max_length=100, null=True, blank=True)
    created_date = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)


class Add_Staff(models.Model):
    user = models.ForeignKey(
        UserProfile, null=True, blank=True, on_delete=models.CASCADE
    )
    associated_board = models.ForeignKey(
        Board, null=True, blank=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.associated_board.board_name)


class Board_Card(models.Model):
    board = models.ForeignKey(
        Board, null=True, blank=True, on_delete=models.CASCADE
    )
    card_name = models.CharField(max_length=100, null=True, blank=True)
    created_date = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)


class Card_List(models.Model):
    card = models.ForeignKey(
        Board_Card, null=True, blank=True, on_delete=models.CASCADE
    )
    list_text = models.CharField(max_length=100, null=True, blank=True)
    created_date = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
