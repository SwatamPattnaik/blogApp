from django.db import models

# Create your models here.

class Transaction(models.Model):
    lender = models.ForeignKey('User', models.DO_NOTHING, db_column='lender', blank=True, null=True, related_name='lender')
    borrower = models.ForeignKey('User', models.DO_NOTHING, db_column='borrower', blank=True, null=True, related_name='borrower')
    amount = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transaction'


class User(models.Model):
    name = models.CharField(unique=True, max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'