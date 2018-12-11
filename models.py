# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from __future__ import unicode_literals

from django.db import models

class Clients(models.Model):
    id = models.ForeignKey('Users', on_delete = models.CASCADE, db_column='Id', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'clients'

class Contracts(models.Model):
    cid = models.ForeignKey(Clients, on_delete = models.CASCADE, db_column='Cid')  # Field name made lowercase.
    fid = models.ForeignKey('Freelancers', on_delete = models.CASCADE, db_column='Fid')  # Field name made lowercase.
    rid = models.ForeignKey('Request', on_delete =models.CASCADE, db_column='Rid')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'contracts'
        unique_together = (('cid', 'fid', 'rid'),)

class FProficiency(models.Model):
    language = models.CharField(db_column='Language', primary_key=True, max_length=20)  # Field name made lowercase.
    star_rating = models.DecimalField(db_column='Star_rating', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    fid = models.ForeignKey('Freelancers', on_delete = models.CASCADE, db_column='Fid', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'f_proficiency'


class Freelancers(models.Model):
    id = models.ForeignKey('Users', on_delete = models.CASCADE, db_column='Id', primary_key=True)  # Field name made lowercase.
    age = models.IntegerField(db_column='Age', blank=True, null=True)  # Field name made lowercase.
    exp = models.IntegerField(db_column='Exp', blank=True, null=True)  # Field name made lowercase.
    major = models.CharField(db_column='Major', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'freelancers'


class Message(models.Model):
    rid = models.ForeignKey('Request', on_delete = models.CASCADE, db_column='Rid')  # Field name made lowercase.
    cid = models.ForeignKey(Clients, on_delete = models.CASCADE, db_column='Cid')  # Field name made lowercase.
    message = models.CharField(db_column='Message', max_length=1000)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'message'
        unique_together = (('rid', 'cid'),)


class ParticipateIn(models.Model):
    tname = models.ForeignKey('Teams', on_delete = models.CASCADE, db_column='Tname')  # Field name made lowercase.
    fid = models.ForeignKey(Freelancers, on_delete = models.CASCADE, db_column='Fid')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'participate_in'
        unique_together = (('tname', 'fid'),)


class Portfolio(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    fid = models.ForeignKey(Freelancers, on_delete = models.CASCADE, db_column='Fid', blank=True, null=True)  # Field name made lowercase.
    class_field = models.CharField(db_column='Class', max_length=1, blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    file = models.FileField(db_column='Filepath')
    req = models.ForeignKey('Request', on_delete = models.CASCADE, db_column='Req_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'portfolio'


class RProficiency(models.Model):
    language = models.CharField(db_column='Language', primary_key=True, max_length=20)  # Field name made lowercase.
    star_rating = models.DecimalField(db_column='Star_rating', max_digits=3, decimal_places=2, blank=True, null=True, default = 0.00)  # Field name made lowercase.
    req = models.ForeignKey('Request', on_delete = models.CASCADE, db_column='Req_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'r_proficiency'


class Request(models.Model):
    req_id = models.IntegerField(db_column='Req_id', primary_key=True)  # Field name made lowercase.
    req_title = models.CharField(db_column='Req_title', max_length=30, null = True)
    fund = models.IntegerField(db_column='Fund', blank=True, null=True)  # Field name made lowercase.
    start_date = models.DateField(db_column='Start_date', default = '1980-01-01')  # Field name made lowercase.
    end_date = models.DateField(db_column='End_date', default = '1980-01-01')  # Field name made lowercase.
    min_exp = models.IntegerField(db_column='Min_exp', blank=True, null=True, default = 0)  # Field name made lowercase.
    min_fre = models.IntegerField(db_column='Min_fre', blank=True, null=True, default = 1)  # Field name made lowercase.
    max_fre = models.IntegerField(db_column='Max_fre', blank=True, null=True, default = 1)  # Field name made lowercase.
    team_only = models.BooleanField(db_column='Team_only', blank=True, default = False)  # Field name made lowercase.
    state = models.IntegerField(db_column='State', blank=False, null=False, default = 0)  # Field name made lowercase.
    frating = models.DecimalField(db_column='Frating', max_digits=3, decimal_places=2, blank=True, null=True, default = None)  # Field name made lowercase.
    crating = models.DecimalField(db_column='Crating', max_digits=3, decimal_places=2, blank=True, null=True, default = None)  # Field name made lowercase.
    cid = models.ForeignKey(Clients, on_delete = models.SET_NULL, db_column='Cid', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'request'


class RequestAsk(models.Model):
    rid = models.ForeignKey(Request, on_delete = models.CASCADE, db_column='Rid')  # Field name made lowercase.
    fid = models.ForeignKey(Freelancers, on_delete = models.CASCADE, db_column='Fid')  # Field name made lowercase.
    askdate = models.DateField(db_column='Askdate', blank=True, null=True)  # Field name made lowercase.
    asktime = models.TimeField(db_column='Asktime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'request_ask'
        unique_together = (('rid', 'fid'),)


class RequestDoc(models.Model):
    doc_id = models.IntegerField(db_column='Doc_id', primary_key=True)  # Field name made lowercase.
    doc = models.FileField(db_column='Docpath')
    req = models.ForeignKey(Request, on_delete = models.CASCADE, db_column='Req_id')  # Field name made lowercase.SS
    class Meta:
        managed = False
        db_table = 'request_doc'


class RequestTeamAsk(models.Model):
    rid = models.ForeignKey(Request, on_delete = models.CASCADE, db_column='Rid')  # Field name made lowercase.
    tname = models.ForeignKey('Teams', on_delete = models.CASCADE, db_column='Tname')  # Field name made lowercase.
    askdate = models.DateField(db_column='Askdate', blank=True, null=True)  # Field name made lowercase.
    asktime = models.TimeField(db_column='Asktime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'request_team_ask'
        unique_together = (('rid', 'tname'),)


class ResultDoc(models.Model):
    doc_id = models.IntegerField(db_column='Doc_id', primary_key=True)  # Field name made lowercase.
    doc = models.FileField(db_column='Docpath')
    req = models.ForeignKey(Request, on_delete = models.CASCADE, db_column='Req_id')  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'result_doc'

class TContracts(models.Model):
    cid = models.ForeignKey(Clients, on_delete = models.CASCADE, db_column='Cid')  # Field name made lowercase.
    tname = models.ForeignKey('Teams', on_delete = models.CASCADE, db_column='Tname')  # Field name made lowercase.
    rid = models.ForeignKey(Request, on_delete = models.CASCADE, db_column='Rid')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 't_contracts'
        unique_together = (('cid', 'tname', 'rid'),)


class Teams(models.Model):
    tname = models.CharField(db_column='Tname', primary_key=True, max_length=20)  # Field name made lowercase.
    leader = models.ForeignKey(Freelancers, on_delete = models.CASCADE, db_column='Id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'teams'


class Users(models.Model):
    id = models.CharField(db_column='Id', primary_key=True, max_length=14)  # Field name made lowercase.
    pw = models.CharField(db_column='Pw', max_length=50)  # Field name made lowercase.
    uname = models.CharField(db_column='UName', max_length=20)  # Field name made lowercase.
    phone_num = models.CharField(db_column='Phone_num', max_length=11, blank=True, null=True)  # Field name made lowercase.
    rating = models.DecimalField(db_column='Rating', max_digits=3, decimal_places=2, blank=True, null=True, default=None)  # Field name made lowercase.
    user_type = models.CharField(db_column='User_type', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'users'