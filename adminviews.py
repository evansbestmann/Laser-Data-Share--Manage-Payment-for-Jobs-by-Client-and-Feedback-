#import datetime
import json
from django.contrib import messages
#from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
#from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import EmailMessage,send_mail
from django.template.loader import render_to_string
from mailjet_rest import Client
from .models import *
def admin_home(request):
    return render (request,"admin_templates/home_content.html")

def addclient(request):
    return render (request,"admin_templates/addclient.html")

def addclient_save(request):
    if request.method != "POST":
        return HttpResponse("method not allowed")
    else:
        username= request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        sentpassword = password
        # print(sentpassword)
        address = request.POST.get("address")
        client_name = username


        try:
            user=CustomUser.objects.create_user(username=username, password=password,email=email,sentpassword=sentpassword,user_type=2)
            user.client.address=address
            user.client.sentpassword=sentpassword
            user.client.client_name = client_name
            user.save()
            # print(user.client.sentpassword)
            messages.success(request,"client added successfully")
            return HttpResponseRedirect(reverse("addclient"))
        except:
            messages.error(request, "Failed to add client")
            return HttpResponseRedirect(reverse("addclient"))

def manageclient(request):
    clients=Client.objects.all().order_by("-id")
    return render(request, "admin_templates/manageclient.html",{"clients":clients})

def editclient(request, client_id):#as passed in url
    clients=Client.objects.get(admin=client_id)
    #return HttpResponse("client id :" +client_id) to test if its returning correct user id
    return render(request, "admin_templates/editclient.html", {"clients": clients, "id":client_id})

def editclient_save(request):
    if request.method != "POST":
        return HttpResponse("method not allowed")
    else:
        client_id= request.POST.get("client_id")
        if client_id==None:
            return HttpResponseRedirect(reverse("manageclient"))
        username = request.POST.get("username")
        email = request.POST.get("email")
        address = request.POST.get("address")
        password = request.POST.get("password")
        client_name = username
        print(username,client_name,password)
        try:
            user = CustomUser.objects.get(id=client_id)
            user.username = username
            user.password = password
            user.email = email
            user.save()

            client = Client.objects.get(admin=client_id)
            client.address = address
            user.client.client_name = client_name
            client.save()
            # print(user.password)
            #messages.success(request, "client Edited successfully")
            return HttpResponseRedirect(reverse("manageclient"))
        except:
            messages.error(request, "Failed to edit client")
            return HttpResponseRedirect(reverse("editclient",kwargs={"client_id":client_id}))


def addfield(request):
    clients= CustomUser.objects.filter(user_type=2)
    return render(request, "admin_templates/addfield.html",{"clients":clients})

def addfield_save(request):
    if request.method != "POST":
        return HttpResponse("method not allowed")
    else:
        client_id=request.POST.get("client")
        field_name=request.POST.get("field_name")
        client = CustomUser.objects.get(id=client_id)
        try:
            field_model = Fields(client_id=client, field_name=field_name)
            field_model.save()
            messages.success(request, "Field added successfully")
            return HttpResponseRedirect(reverse("addfield"))
        except:
            messages.error(request, "Failed to edit client")
            return HttpResponseRedirect(reverse("addfield"))

def managefield(request):
    fields=Fields.objects.all().order_by("-id")
    return render(request, "admin_templates/managefield.html",{"fields":fields})

def editfield(request, field_id):#as passed in url
    fields=Fields.objects.get(id=field_id)
    clients = CustomUser.objects.filter(user_type=2)
    #return HttpResponse("client id :" +client_id) to test if its returning correct user id
    return render(request, "admin_templates/editfield.html", {"fields": fields,"clients":clients, "id":field_id})

def editfield_save(request):
    if request.method != "POST":
        return HttpResponse("method not allowed")
    else:
        field_id=request.POST.get("field_id")
        if field_id==None:
            return HttpResponseRedirect(reverse("managefield"))
        client_id=request.POST.get("client")
        field_name=request.POST.get("field_name")

        try:
                client = CustomUser.objects.get(id=client_id)
                field_model = Fields(id=field_id)
                field_model.field_name = field_name
                field_model.client_id = client
                field_model.save()
                messages.success(request, "Field edited successfully")
                return HttpResponseRedirect(reverse("managefield"))
        except:
                messages.error(request, "Failed to edit client")
                return HttpResponseRedirect(reverse("editfield",kwargs={"field_id":field_id}))

def addlaserrep(request):
    return render(request, "admin_templates/addlaserrep.html")

def addlaserrep_save(request):
    if request.method != "POST":
        return HttpResponse("method not allowed")
    else:
        repname = request.POST.get("laserrep_name")
        repposition = request.POST.get("laserrep_position")

        try:
           rep_model = LaserRep(laserrep_name=repname, position=repposition)
           rep_model.save()
           messages.success(request, "Representative added successfully")
           return HttpResponseRedirect(reverse("addlaserrep"))
        except:
           messages.error(request, "Failed to add  Representative")
           return HttpResponseRedirect(reverse("addlaserrep"))


def managelaserrep(request):
    reps = LaserRep.objects.all().order_by("-id")
    return render(request, "admin_templates/managereps.html", {"reps": reps})

def editreps(request, rep_id):#as passed in url
    reps=LaserRep.objects.get(id=rep_id)
    #return HttpResponse("client id :" +client_id) to test if its returning correct user id
    return render(request, "admin_templates/editreps.html", {"reps": reps, "id":rep_id})


def editlaserrep_save(request):
    if request.method != "POST":
        return HttpResponse("method not allowed")
    else:
        rep_id=request.POST.get("rep_id")
        repname = request.POST.get("laserrep_name")
        repposition = request.POST.get("laserrep_position")

        try:
           rep_model = LaserRep.objects.get(id=rep_id)
           rep_model.laserrep_name=repname
           rep_model.position=repposition
           rep_model.save()
           messages.success(request, "Representative edited successfully")
           return HttpResponseRedirect(reverse("managereps"))
        except:
           messages.error(request, "Failed to edit  Representative")
           return HttpResponseRedirect(reverse("editreps",kwargs={"rep_id":rep_id}))

def addjobstatus(request):
    fields = Fields.objects.all()
    clients = Client.objects.all()
    jobstatuses=JobStatus.objects.all()
    laserreps=LaserRep.objects.all()
    return render(request, "admin_templates/addjobstatus.html",{"fields":fields,"clients":clients,"jobstatuses":jobstatuses,"laserreps":laserreps})

def addjobstatus_save(request):
    if request.method != "POST":
        return HttpResponse("method not allowed")
    else:
        status= request.POST.get("status_name")
        try:
            status_model=JobStatus(jobstatus=status)
            status_model.save()
            messages.success(request, "Status added successfully")
            return HttpResponseRedirect(reverse("addjobstatus"))
        except:
            messages.error(request, "Failed to add  Status")
            return HttpResponseRedirect(reverse("addjobstatus"))

def managejobstatus(request):
    statuses=JobStatus.objects.all().order_by("-id")
    return render(request, "admin_templates/managejobstatus.html", {"statuses": statuses})

def editjobstatus(request, status_id):#as passed in url
    statuses=JobStatus.objects.get(id=status_id)
    #return HttpResponse("client id :" +client_id) to test if its returning correct user id
    return render(request, "admin_templates/editjobstatus.html", {"statuses": statuses, "id":status_id})

def editjobstatus_save(request):
    if request.method != "POST":
        return HttpResponse("method not allowed")
    else:
        status_id=request.POST.get("status_id")
        status = request.POST.get("status_name")
        try:
            status_model = JobStatus(id=status_id,jobstatus=status)
            status_model.save()
            messages.success(request, "Status edited successfully")
            return HttpResponseRedirect(reverse("managejobstatus"))
        except:
            messages.error(request, "Failed to edit  Status")
            return HttpResponseRedirect(reverse("editjobstatus",kwargs={"status_id":status_id}))

def addjob(request):
    clients=CustomUser.objects.filter(user_type=2)
    statuses=JobStatus.objects.all()
    laserreps=LaserRep.objects.all()
    fields=Fields.objects.all()
    passwordsent=Client.objects.all()

    return render(request, "admin_templates/addjob.html", {"fields":fields,"clients":clients,"statuses":statuses,"laserreps":laserreps,"passwordsent":passwordsent})

def getfields(request):
    client = json.loads(request.body)#here we get the body from our fetch api that was already converted to string  with json.stringify
    client_id=client["id"]#'id' key of data passed to backend from id:clientval in our fetch api
    fields=Fields.objects.filter(client_id__id=client_id)#now filtering fields related to client id gotten from fetch api
    return JsonResponse(list(fields.values("id", "field_name")),safe=False)

def addjob_save(request):
    if request.method != "POST":
        return HttpResponse("method not allowed")
    else:
        client = request.POST.get("client")
        field = request.POST.get("field_id")
        pvt_number = request.POST.get("pvt_number")
        clientrep = request.POST.get("clientrep")
        clientrepmail = request.POST.get("clientrepmail")
        jobstatus = request.POST.get("status")
        laser_rep = request.POST.get("laser_rep")
        jobkey = request.POST.get("jobkey")
        copiedemails = request.POST.get("copiedemails")
        copiedemails1 = request.POST.get("copiedemails1")
        copiedemails2 = request.POST.get("copiedemails2")
        copiedemails3 = request.POST.get("copiedemails3")
        # if request.FILES.get('jobfile', False):
        jobfile = request.FILES['jobfile']
        complete = request.POST.get("complete")
        client_id = CustomUser.objects.get(id=client)
        field_id = Fields.objects.get(id=field)
        jobstatus_id = JobStatus.objects.get(id=jobstatus)
        laser_rep_id = LaserRep.objects.get(id=laser_rep)
        clientemail = CustomUser.objects.get(id=client).email
        clientpassword = CustomUser.objects.get(id=client).password
        passwordsent = CustomUser.objects.get(id=client).sentpassword
        # print(passwordsent)
        #mail for client rep

        try:
            job_model = Dataset(pvt_number=pvt_number, clientrep=clientrep, clientrep_email=clientrepmail, jobkey=jobkey,
                                pdf=jobfile, copiedemails=copiedemails,client_id=client_id, field_id=field_id, jobstatus=jobstatus_id, laserrep_id=laser_rep_id,
                                completed=complete, copiedemail1=copiedemails1,copiedemails2=copiedemails2, copiedemails3=copiedemails3)
            job_model.save()
            try:

                context = {"pvt_number": pvt_number, "jobkey": jobkey, "clientrep": clientrep,
                           "jobstatus_id": jobstatus_id, "clientemail": clientemail,"passwordsent":passwordsent}
                mail_temp = "admin_templates/email_template.html"
                mail_msg = render_to_string(mail_temp, context=context)
                mail_from = "labinfo@laser-ng.com"
                subject = "Laser Engineering posted a Report to you"
                recipient = [clientrepmail]
                mail = EmailMessage(subject, mail_msg, mail_from, recipient)
                mail.content_subtype = 'html'
                mail.send()
            except:
                messages.error(request, "Make sure your internet is connected")
                return HttpResponseRedirect(reverse("addjob"))

            # mail for copied mails
            try:
                context = {"pvt_number": pvt_number, "jobkey": jobkey, "clientrep": clientrep,
                           "jobstatus_id": jobstatus_id,
                           "clientemail": clientemail, "clientpassword": clientpassword, }
                mail_temp = "admin_templates/emailcopied_template.html"
                mail_msg = render_to_string(mail_temp, context=context)
                mail_from = "labinfo@laser-ng.com"
                subject = "Laser Engineering Notice for Report sent to Client representative"
                recipient = [copiedemails, copiedemails1, copiedemails2, copiedemails3]
                mail = EmailMessage(subject, mail_msg, mail_from, recipient)
                mail.content_subtype = 'html'
                mail.send()
            except:
                messages.error(request, "Make sure your internet is connected")
                return HttpResponseRedirect(reverse("addjob"))
            messages.success(request, "Job added successfully")
            return HttpResponseRedirect(reverse("addjob"))
        except:
            messages.error(request, "Job add Failed")
            return HttpResponseRedirect(reverse("addjob"))

def managejob(request):
    Active = Dataset.objects.filter(completed="Active").order_by("-id")
    Complete = Dataset.objects.filter(completed="Complete").order_by("-id")
    jobs = Dataset.objects.all().order_by("-id")
    jc = jobs.count()
    oc = Active.count()
    cc = Complete.count()

    return render(request, "admin_templates/managejob.html", {"jc":jc,"oc": oc,"cc":cc,"jobs": jobs,})

def editjob(request, job_id):
    clients = CustomUser.objects.filter(user_type=2)
    statuses = JobStatus.objects.all()
    laserreps = LaserRep.objects.all()
    jobs= Dataset.objects.get(id=job_id)
    fields = Fields.objects.get(id=jobs.field_id.id)
    return render(request, "admin_templates/editjob.html", {"fields": fields,"jobs": jobs, "id":job_id,"clients":clients,"statuses":statuses,"laserreps":laserreps})

def getfieldsedit(request):
    client = json.loads(request.body)#here we get the body from our fetch api that was already converted to string  with json.stringify
    client_id=client["id"]#'id' key of data passed to backend from id:clientval in our fetch api
    fields=Fields.objects.filter(client_id__id=client_id)#now filtering fields related to client id gotten from fetch api
    return JsonResponse(list(fields.values("id", "field_name")),safe=False)


def editjob_save(request):
    if request.method != "POST":
        return HttpResponse("method not allowed")
    else:
        job_id = request.POST.get("job_id")
        slug= request.POST.get("slug")
        if job_id == None:
            return HttpResponseRedirect(reverse("managejob"))
        client = request.POST.get("client")
        if request.POST.get('field_id', False):
            field = request.POST.get("field_id")
        else:
            field = None
        pvt_number = request.POST.get("pvt_number")
        clientrep = request.POST.get("clientrep")
        clientrepmail = request.POST.get("clientrepmail")
        jobstatus = request.POST.get("status")
        laser_rep = request.POST.get("laser_rep")
        jobkey = request.POST.get("jobkey")
        if request.POST.get('complete',False):
            complete = request.POST.get("complete")
        else:
            complete = Dataset.objects.get(id=job_id).completed
        copiedemails= request.POST.get("copiedemails")
        if request.FILES.get('jobfile', False):
           jobfile = request.FILES['jobfile']
        else:
            jobfile = Dataset.objects.get(id=job_id).pdf  # AND IF NO NEW FILE IS SELECTED DO NONE
        client_id = CustomUser.objects.get(id=client)
        field_id = Fields.objects.get(id=field)
        jobstatus_id = JobStatus.objects.get(id=jobstatus)
        laser_rep_id = LaserRep.objects.get(id=laser_rep)
        clientemail = CustomUser.objects.get(id=client).email
        clientpassword = CustomUser.objects.get(id=client).password
        copiedemails = request.POST.get("copiedemails")
        copiedemails1 = request.POST.get("copiedemails1")
        copiedemails2 = request.POST.get("copiedemails2")
        copiedemails3 = request.POST.get("copiedemails3")
        ####mail part

        ##mail for client rep
        try:
            context = {"pvt_number": pvt_number, "jobkey": jobkey, "clientrep": clientrep, "jobstatus_id": jobstatus_id,"clientemail":clientemail,"clientpassword":clientpassword, }
            mail_temp = "admin_templates/editjobemail_template.html"
            mail_msg = render_to_string(mail_temp, context=context)
            mail_from = "labinfo@laser-ng.com"
            subject = "Laser Engineering posted a Report to you was updated"
            recipient = [clientrepmail]
            mail = EmailMessage(subject, mail_msg, mail_from, recipient)
            mail.content_subtype = 'html'
            mail.send()
        except:
            messages.error(request, "Make sure your internet is connected")
            return HttpResponseRedirect(reverse("editjob", kwargs={"job_id": job_id}))
        # mail for copied mails
        try:
            context = {"pvt_number": pvt_number, "jobkey": jobkey, "clientrep": clientrep, "jobstatus_id": jobstatus_id,
                       "clientemail": clientemail, "clientpassword": clientpassword, }
            mail_temp = "admin_templates/emaileditcopied_template.html"
            mail_msg = render_to_string(mail_temp, context=context)
            mail_from = "labinfo@laser-ng.com"
            subject = "Laser Engineering Notice for Report Update sent to Client representative"
            recipient = [copiedemails, copiedemails1, copiedemails2, copiedemails3]
            mail = EmailMessage(subject, mail_msg, mail_from, recipient)
            mail.content_subtype = 'html'
            mail.send()
        except:
            messages.error(request, "Make sure your internet is connected")
            return HttpResponseRedirect(reverse("editjob", kwargs={"job_id": job_id}))
        try:
            job_model = Dataset.objects.get(id=job_id)
            job_model.pvt_number = pvt_number
            job_model.slug=slug
            job_model.clientrep = clientrep
            job_model.clientrep_email = clientrepmail
            job_model.jobkey = jobkey
            job_model.copiedemails = copiedemails
            job_model.pdf = jobfile
            job_model.client_id = client_id
            job_model.field_id = field_id
            job_model.jobstatus = jobstatus_id
            job_model.laserrep_id = laser_rep_id
            job_model.completed = complete
            jobfile.copiedemails = copiedemails
            job_model.copiedemail1=copiedemails1
            job_model.copiedemails2=copiedemails2
            job_model.copiedemails3=copiedemails3
            job_model.save()
            messages.success(request, "Job edited successfully")
            return HttpResponseRedirect(reverse("managejob"))
        except:
            messages.error(request, "Job edit Failed")
            return HttpResponseRedirect(reverse("editjob", kwargs={"job_id": job_id}))

def viewjobinfo(request, job_id):
    jobs = Dataset.objects.get(id=job_id)
    return render(request, "admin_templates/viewjobinfo.html",{"jobs": jobs, "id": job_id})


def viewfeedback(request):
    feedback = FeedBackClient.objects.all().order_by("-id")
    return render(request, "admin_templates/viewfeedback.html",{"fb": feedback})

def viewfeedbackdetail(request,job_id):
    feedback = FeedBackClient.objects.get(id = job_id)
    return render(request, "admin_templates/viewfeedbackdetail.html", {"fb": feedback, "id": job_id})

def completedjobs(request):
    Active = Dataset.objects.filter(completed="Active").order_by("-id")
    Complete = Dataset.objects.filter(completed="Complete").order_by("-id")
    jobs = Dataset.objects.all().order_by("-id")
    jc=jobs.count()
    oc=Active.count()
    cc=Complete.count()
    return render(request, "admin_templates/completedjobs.html",{"jc":jc,"oc": oc,"cc":cc,"Complete":Complete})

def ongoingjobs(request):
    Active = Dataset.objects.filter(completed="Active").order_by("-id")
    Complete = Dataset.objects.filter(completed="Complete").order_by("-id")
    jobs = Dataset.objects.all().order_by("-id")
    jc=jobs.count()
    oc=Active.count()
    cc=Complete.count()
    return render(request, "admin_templates/ongoingjobs.html",{"jc":jc,"oc": oc,"cc":cc,"Active":Active})
