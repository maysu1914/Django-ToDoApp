from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class List(models.Model):
    # FILTERING = (
    #     ('Completed', 'Completed'),
    #     ('Not Completed', 'Not Completed'),
    #     ('Expired', 'Expired')
    # )
    # SORTING = (
    #     ('Name', 'Name'),
    #     ('Status', 'Status'),
    #     ('Deadline', 'Deadline')
    # )
    user_id = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    # last_sorting = models.CharField(max_length=200, null=True, choices=SORTING)
    # last_filtering = models.CharField(max_length=200, null=True, choices=FILTERING)

    def __str__(self):
        return str(self.user_id) + ' ' + self.name


class Item(models.Model):
    STATUS = (
        ('Completed', 'Completed'),
        ('Not Completed', 'Not Completed'),
        ('Expired', 'Expired'),
    )
    list_id = models.ForeignKey(List, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    deadline = models.DateField(null=True)
    created = models.DateField(auto_now_add=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.list_id) + ' ' + self.name
