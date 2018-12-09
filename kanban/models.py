from django.db import models

# Create your models here.


class TrelloUser(models.Model):
    UserID = models.IntegerField(unique = True)
    IsPremium = models.BooleanField(default = False)
    BoardCount = models.IntegerField(default = 0)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    UpdatedDate = models.DateTimeField(auto_now=True)
    Active = models.BooleanField(default=True)
    Archived = models.BooleanField(default=False)

    class Meta:
        ordering = ('CreatedDate',)

    
class Board(models.Model):
    Name = models.CharField(max_length=30)
    CreatedBy = models.IntegerField()
    CreatedDate = models.DateTimeField(auto_now_add=True)
    UpdatedDate = models.DateTimeField(auto_now=True)
    Active = models.BooleanField(default=True)
    Archived = models.BooleanField(default=False)

    class Meta:
        ordering = ('CreatedDate',)


class BoardMember(models.Model):

    BoardID = models.IntegerField()
    UserID = models.IntegerField()
    CreatedDate = models.DateTimeField(auto_now_add=True)
    UpdatedDate = models.DateTimeField(auto_now=True)
    Active = models.BooleanField(default=True)
    Archived = models.BooleanField(default=False)

    class Meta:
        ordering = ('CreatedDate',)

class List(models.Model):
    BoardID = models.IntegerField()
    Name = models.CharField(max_length=30)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    UpdatedDate = models.DateTimeField(auto_now=True)
    Active = models.BooleanField(default=True)
    Archived = models.BooleanField(default=False)


class Card(models.Model):
    ListID = models.IntegerField()
    Name = models.CharField(max_length=30)
    Description = models.CharField(max_length=1000)
    DueDate = models.DateTimeField(null = True)
    pos = models.IntegerField()
    CreatedDate = models.DateTimeField(auto_now_add=True)
    UpdatedDate = models.DateTimeField(auto_now=True)
    Active = models.BooleanField(default=True)
    Archived = models.BooleanField(default=False)

class Attachment(models.Model):
    CardID = models.IntegerField()
    Url = models.URLField()
    UploadedBy = models.IntegerField()
    CreatedDate = models.DateTimeField(auto_now_add=True)
    UpdatedDate = models.DateTimeField(auto_now=True)
    Active = models.BooleanField(default=True)
    Archived = models.BooleanField(default=False)
