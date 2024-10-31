from django.db import models

# Create your models here.


class Users(models.Model):
    username = models.CharField(max_length=20)
    email = models.EmailField()
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.email


class Income(models.Model):
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE, related_name='user_income')
    month = models.CharField(max_length=20)
    amount = models.PositiveBigIntegerField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} has income {self.amount}"


class Expnese(models.Model):
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE, related_name='user_expense')
    month = models.CharField(max_length=20)
    amount = models.BigIntegerField()
    note = models.TextField()

    def __str__(self):
        return f"{self.user.username} spend {self.amount}"
