from django.contrib.auth.models import AbstractUser
from django.db import models
import secrets
from .paystack import *
from .utils import *


# Create your models here.
from django.db.models.signals import post_save,pre_save ###presave for slug url function
from django.dispatch import receiver

class CustomUser(AbstractUser):
    user_type_data = ((1, "admin"), (2, "client"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)

class AdminLaser(models.Model):
    id=  models.AutoField(primary_key=True)
    admin= models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects= models.Manager()
    def __str__(self):
        return self.id

class Client(models.Model):
    id=  models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    client_name= models.CharField(max_length=500)
    address = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects= models.Manager()
    def __str__(self):
        return self.client_name

class Fields(models.Model):
    id=models.AutoField(primary_key=True)
    client_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    field_name= models.CharField(max_length=255)
    objects= models.Manager()
    def __str__(self):
        return self.field_name

class LaserRep(models.Model):
    id=models.AutoField(primary_key=True)
    laserrep_name= models.CharField(max_length=255, null=True)
    position= models.CharField(max_length=255)
    objects= models.Manager()
    def __str__(self):
        return self.laserrep_name

class JobStatus(models.Model):
    id=models.AutoField(primary_key=True)
    jobstatus= models.CharField(max_length=255)
    objects= models.Manager()
    def __str__(self):
        return self.jobstatus

class Dataset(models.Model):
    choices = (("complete", "complete"), ("ongoing", "ongoing"))
    id=  models.AutoField(primary_key=True)
    slug= models.SlugField(max_length=255,null=True,blank=True)
    client_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    field_id= models.ForeignKey(Fields,on_delete=models.CASCADE,default=1)
    pvt_number = models.CharField(max_length=255)
    clientrep= models.CharField(max_length=255)
    clientrep_email= models.EmailField()
    jobstatus = models.ForeignKey(JobStatus,on_delete=models.CASCADE,default=1)
    laserrep_id = models.ForeignKey(LaserRep,on_delete=models.CASCADE,default=1)
    jobkey= models.CharField(max_length=255)
    cover =models.ImageField(upload_to='img',blank=True,null=True)
    pdf = models.FileField(upload_to='pdf')
    completed = models.CharField(choices=choices, max_length=8, default="ongoing")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    # class Meta:
    #     ordering = ('-created_at')
    def __str__(self):
        return self.pvt_number

def slug_generator(sender, instance, *args, **kwargs):
        if not instance.slug:
            instance.slug = unique_slug_generator(instance)
pre_save.connect(slug_generator, sender=Dataset)

class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.PositiveIntegerField()
    ref = models.CharField(max_length=200)
    job_id =  models.ForeignKey(Dataset,on_delete=models.CASCADE,default=1)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    email =  models.EmailField()
    verified = models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    class Meta:
        ordering = ('-created_at',)
    def __str__(self):
        return self.job_id

    def save(self,*args,**kwargs) -> None:
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_same_ref = Payment.objects.filter(ref=ref)
            if not object_with_same_ref:
                self.ref = ref
        super().save(*args, **kwargs)
    def amount_value(self) -> int:
        return self.amount
    def verifypayment(self):
        paystack = Paystack()
        status, result = paystack.verifypayment(self.ref,self.amount)
        if status:
            if result["amount"] / 100 == self.amount:
                self.verified = True
            self.save()
        if self.verified:
            return True
        return False





class FeedBackClient(models.Model):

    id = models.AutoField(primary_key=True)
    pvt_number = models.CharField(max_length=255)
    job_id = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    client = models.CharField(max_length=255)
    address = models.TextField()
    descrition_of_service = models.TextField()
    analysis_and_report = models.IntegerField()
    job_schedule = models.IntegerField()
    staff_performance = models.IntegerField()
    job_price = models.IntegerField()
    recommend_us = models.IntegerField()
    complaint_response = models.IntegerField()
    rejected_services = models.CharField(max_length=3)
    rejected_services_comment = models.TextField()
    comment = models.TextField()
    laser_rep = models.CharField(max_length=255)
    client_rep = models.CharField(max_length=255)

    score=models.IntegerField()
    client_rep_designation = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    def __str__(self):
        return self.job_id

class NotificationClient(models.Model):
    id=  models.AutoField(primary_key=True)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    def __str__(self):
        return self.message




@receiver(post_save, sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            AdminLaser.objects.create(admin=instance)
        if instance.user_type==2:
            Client.objects.create(admin=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.adminlaser.save()
    if instance.user_type==2:
        instance.client.save()


