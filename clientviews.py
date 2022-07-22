#import datetime
#import json
from django.contrib import messages
#from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404, HttpRequest
from django.shortcuts import render, redirect
#from django.urls import reverse
#from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from datetime import datetime as dt, timedelta as td
#from  pypaystack import Transaction,Customer,Plan
import pytz
from .models import *
#from .forms import PaymentFORM
from django.conf import settings
#from .encryption_util import *
from django.core.mail import EmailMessage,send_mail
from django.template.loader import render_to_string

def client_home(request):
    return render (request,"client_templates/client_home.html")

def viewjob(request):
    jobs = Dataset.objects.filter(client_id=request.user.id).order_by("-id")
    Active = Dataset.objects.filter(client_id=request.user.id, completed="Active").order_by("-id")
    Complete = Dataset.objects.filter(client_id=request.user.id, completed="Complete").order_by("-id")
    jc = jobs.count()
    oc = Active.count()
    cc = Complete.count()
    return render (request,"client_templates/viewjob.html",{"jc":jc,"oc": oc,"cc":cc,"jobs":jobs})

def viewjobinfoclient(request, job_id):
    jobs = Dataset.objects.get(id=job_id)
    return render(request, "client_templates/viewjobinfoclient.html",{"jobs": jobs, "id": job_id})

def jobkey(request,job_id):
    jobs = Dataset.objects.get(slug=job_id)
    return render(request, "client_templates/jobkey.html", {"jobs": jobs, "slug": job_id})

def jobdownload(request):

    if request.method != "POST":
        return HttpResponse("method not allowed")

    else:
        job_id = request.POST.get("job_id")
        slug = request.POST.get("slug")
        userkey = request.POST.get("key")

        try:
            # job = Dataset.objects.get(slug=job_id)
            test = Dataset.objects.get(slug=slug).jobkey  ### collected the value of jobkey
            ##print(test)
            datecreated = Dataset.objects.get(slug=slug).created_at
            x = dt.now()
            #print(x)
            utc = pytz.UTC
            xcon = utc.localize(x)
            #0.000694
            expiredate = datecreated + td(days=0.00347)
            ##print(datecreated)
            ##print(expiredate)
            ##print(xcon)

            if test == userkey:
                if xcon < expiredate:
                      return HttpResponseRedirect(reverse("downloadjob", kwargs={"job_id": slug}))
                else:
                    return HttpResponseRedirect(reverse("payforjob", kwargs={"job_id": slug}))
            else:
                messages.error(request, "Job Key is wrong, type in correct Job Key and try again")
                return HttpResponseRedirect(reverse("jobkey", kwargs={"job_id": slug}))
        except:
            return render(request, "client_templates/client_home.html")

def downloadjob(request,job_id):
    jobs = Dataset.objects.get(slug=job_id)
    #cover = Dataset.objects.get(id=job_id).cover to get specific parameter in dataset class model
    return render(request, "client_templates/downloadjob.html",{"jobs": jobs, "slug": job_id})



def payforjob(request, job_id):
    jobs = Dataset.objects.get(slug=job_id)
    return render(request, "client_templates/payforjob.html",{"jobs": jobs, "slug": job_id})

def transcation(request):
    if request.method != "POST":
        return HttpResponse("method not allowed")
    else:
        job_id=request.POST.get("job_id")
        slug = request.POST.get("slug")
        email = request.POST.get("email")
        amount = request.POST.get("amount")
        job = Dataset.objects.get(id=job_id)
        #####mail part
        pvt_number = Dataset.objects.get(id=job_id).pvt_number
        clientrep = Dataset.objects.get(id=job_id).clientrep
        jobstatus_id = Dataset.objects.get(id=job_id).jobstatus_id
        clientrepmail = Dataset.objects.get(id=job_id).clientrep_email
        copiedemails = Dataset.objects.get(id=job_id).copiedemails
        copiedemails1 = Dataset.objects.get(id=job_id).copiedemail1
        copiedemails2 = Dataset.objects.get(id=job_id).copiedemails2
        copiedemails3 = Dataset.objects.get(id=job_id).copiedemails3

        try:
            paymentset = Payment(job_id=job, email=email,amount=amount, slug=slug)
            paymentset.save()
            try:
                ### payment confirm client mail
                context = {"pvt_number": pvt_number, "amount": amount, "clientrep": clientrep, }
                mail_temp = "client_templates/payjobemail_template.html"
                mail_msg = render_to_string(mail_temp, context=context)
                mail_from = "labinfo@laser-ng.com"
                subject = "Laser Engineering to recieve your Payment"
                recipient = [clientrepmail,]
                mail = EmailMessage(subject, mail_msg, mail_from, recipient)
                mail.content_subtype = 'html'
                mail.send()
            except:
                messages.error(request, "Make sure your internet is connected")
                return HttpResponseRedirect(reverse("error"))
            try:
                ### payment confirm client mail
                context = {"pvt_number": pvt_number, "amount": amount, "clientrep": clientrep, }
                mail_temp = "client_templates/recievepaymentmail.html"
                mail_msg = render_to_string(mail_temp, context=context)
                mail_from = "labinfo@laser-ng.com"
                subject = "Laser Engineering to receive Payment"
                recipient = [copiedemails,copiedemails1,copiedemails2,copiedemails3]
                mail = EmailMessage(subject, mail_msg, mail_from, recipient)
                mail.content_subtype = 'html'
                mail.send()
            except:
                messages.error(request, "Make sure your internet is connected")
                return HttpResponseRedirect(reverse("error"))
            #return HttpResponseRedirect(reverse("downloadjob", kwargs={"job_id": job_id}))
            return render(request, "client_templates/makepayment.html", {"job":job,"paymentset":paymentset,"paystack_public_key":settings.PAYSTACK_PUBLIC_KEY,})
            #return (request,"makepayment.html",{"paymentset":paymentset,"paystack_public_key":settings.PAYSTACK_PUBLIC_KEY})

        except:
           return HttpResponseRedirect(reverse("payforjob",kwargs={"job_id":slug}))

def makepayment(request,job_id):
    jobs = Dataset.objects.filter(id=job_id)

    return render (request,"client_templates/makepayment.html",{"jobs": jobs, "id": job_id})

def verifypayment(request: HttpRequest, ref,job_id):
    job =Dataset.objects.get(id=job_id)
    payment = Payment.objects.get(id=ref)
    verified = payment.verifypayment()
    if verified:
        pass
    else:
        pass
       #return HttpResponseRedirect(reverse("jobkey", kwargs= {"id": job_id}))

def jobfeedback(request,job_id):
    jobs=Dataset.objects.get(slug=job_id)
    return render(request, "client_templates/jobfeedback.html",{"jobs":jobs,"slug": job_id})

def feedback_save(request):
    if request.method != "POST":
        return HttpResponse("method not allowed")
    else:
        job = request.POST.get("job")
        slug = request.POST.get("slug")
        service=request.POST.get("service")
        analysis_and_report = request.POST.get("analysis_and_report")
        job_schedule =request.POST.get("job_schedule")
        staff_performance =request.POST.get("staff_performance")
        job_price =request.POST.get("job_price")
        recommend_us =request.POST.get("recommend_us")
        complaint_response =request.POST.get("complaint_response")
        rejected_services =request.POST.get("rejected_services")
        rejected_services_comment =request.POST.get("rejected_services_comment")
        address =request.POST.get("address")
        client_id =request.POST.get("client_id")
        job_id =request.POST.get("job_id")
        laser_rep =request.POST.get("laserrep")
        client_rep =request.POST.get("clientrep")
        comment =request.POST.get("comment")
        client_rep_designation =""
        date=request.POST.get("date")
        n1= int(analysis_and_report)
        n2=int(job_price)
        n3=int(job_schedule)
        n4= int(recommend_us)
        n5= int(staff_performance)
        n6= int(complaint_response)
        score = n1+n2+n3+n4+n5+n6
        copiedemails = Dataset.objects.get(id=job_id).copiedemails
        copiedemails1 = Dataset.objects.get(id=job_id).copiedemail1
        copiedemails2 = Dataset.objects.get(id=job_id).copiedemails2
        copiedemails3 = Dataset.objects.get(id=job_id).copiedemails3
        #print(score)
        try:
            job_id=Dataset.objects.get(id=job_id)
            feedback_model = FeedBackClient(job_id=job_id,client=client_id,address=address,descrition_of_service=service,
                                       analysis_and_report=analysis_and_report,job_schedule=job_schedule,staff_performance=staff_performance,
                                       job_price=job_price,recommend_us=recommend_us,complaint_response=complaint_response,score=score,
                                       rejected_services=rejected_services,rejected_services_comment=rejected_services_comment,pvt_number=job,
                                       comment=comment,laser_rep=laser_rep,client_rep=client_rep,client_rep_designation=client_rep_designation,created_at=date ,slug=slug)
            feedback_model.save()
            try:
                ### payment confirm client mail
                context = {"pvt_number": job_id, "clientrep": client_rep, }
                mail_temp = "client_templates/feedbackemail_template.html"
                mail_msg = render_to_string(mail_temp, context=context)
                mail_from = "labinfo@laser-ng.com"
                subject = "Laser Engineering Recieved Feedback"
                recipient = [copiedemails,copiedemails1,copiedemails2,copiedemails3]
                mail = EmailMessage(subject, mail_msg, mail_from, recipient)
                mail.content_subtype = 'html'
                mail.send()
            except:
                messages.error(request, "Make sure your internet is connected")
                return HttpResponseRedirect(reverse("error"))
            return HttpResponseRedirect(reverse("viewjob"))
        except:
            messages.error(request, "Failed to send  Feedback")
            return HttpResponseRedirect(reverse( "jobfeedback",kwargs={"job_id": slug}))

def completedjobs(request):
    jobs = Dataset.objects.filter(client_id=request.user.id).order_by("-id")
    Active = Dataset.objects.filter(client_id=request.user.id, completed="Active").order_by("-id")
    Complete = Dataset.objects.filter(client_id=request.user.id, completed="Complete").order_by("-id")
    jc = jobs.count()
    oc = Active.count()
    cc = Complete.count()
    return render(request, "client_templates/clientcompletedjobs.html",{"jc":jc,"oc": oc,"cc":cc,"completedjobs":Complete})

def ongoingjobs(request):
    jobs = Dataset.objects.filter(client_id=request.user.id).order_by("-id")
    Active = Dataset.objects.filter(client_id=request.user.id, completed="Active").order_by("-id")
    Complete = Dataset.objects.filter(client_id=request.user.id, completed="Complete").order_by("-id")
    jc = jobs.count()
    oc = Active.count()
    cc = Complete.count()
    return render(request, "client_templates/clientongoingjobs.html",{"jc":jc,"oc": oc,"cc":cc,"ongoingjobs":Active})

def error(request,job_id):
    return render(request, "client_templates/error.html")

