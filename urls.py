from django.urls import path
from . import views as v
from . import adminviews as av
from . import clientviews as cv


urlpatterns = [

    path('', v.loginpage, name='login'),
    path('admin_home', av.admin_home, name='admin_home'),
    path('user_login', v.dologin, name='user_login'),
    path('dologin', v.dologin, name='dologin'),
    path('user_details', v.user_details, name='user_details'),
    path('user_logout', v.logout_user, name='user_logout'),
    path('admin_home', av.admin_home, name='admin_home'),
    path('addclient', av.addclient, name='addclient'),
    path('addclient_save', av.addclient_save, name='addclient_save'),
    path('manageclient', av.manageclient, name='manageclient'),
    path('editclient/<str:client_id>', av.editclient, name='editclient'),
    path('editclient_save', av.editclient_save, name='editclient_save'),
    
    path('addfield', av.addfield, name='addfield'),
    path('addfield_save', av.addfield_save, name='addfield_save'),
    path('managefield', av.managefield, name='managefield'),
    path('editfield/<str:field_id>', av.editfield, name='editfield'),
    path('editfield_save', av.editfield_save, name='editfield_save'),

    path('addlaserrep', av.addlaserrep, name='addlaserrep'),
    path('addlaserrep_save', av.addlaserrep_save, name='addlaserrep_save'),
    path('managereps', av.managelaserrep, name='managereps'),
    path('editreps/<str:rep_id>', av.editreps, name='editreps'),
    path('editlaserrep_save', av.editlaserrep_save, name='editlaserrep_save'),


    path('addjobstatus', av.addjobstatus, name='addjobstatus'),
    path('addjobstatus_save', av.addjobstatus_save, name='addjobstatus_save'),
    path('managejobstatus', av.managejobstatus, name='managejobstatus'),
    path('editjobstatus/<str:status_id>', av.editjobstatus, name='editjobstatus'),
    #path('getfield', av.getfield, name='getfield'),
    path('editjobstatus_save', av.editjobstatus_save, name='editjobstatus_save'),

    path('addjob', av.addjob, name='addjob'),
    path('addjob_save', av.addjob_save, name='addjob_save'),
    path('getfields', av.getfields, name='getfields'),
    path('managejob', av.managejob, name='managejob'),
    path('editjob/<str:job_id>', av.editjob, name='editjob'),
    path('getfieldsedit', av.getfieldsedit, name='getfieldsedit'),
    path('editjob_save', av.editjob_save, name='editjob_save'),
    path('viewjobinfo/<str:job_id>', av.viewjobinfo, name='viewjobinfo'),
    path('viewfeedback', av.viewfeedback, name='viewfeedback'),
    path('viewfeedbackdetail/<str:job_id>', av.viewfeedbackdetail, name='viewfeedbackdetail'),
    path('completedjobs', av.completedjobs, name='completedjobs'),
    path('ongoingjobs', av.ongoingjobs, name='ongoingjobs'),


    #CLIENT URLS
    path('client_home', cv.client_home, name='client_home'),

    path('viewjob', cv.viewjob, name='viewjob'),
    path('jobkey/<slug:job_id>', cv.jobkey, name='jobkey'),
    path('jobdownload', cv.jobdownload, name='jobdownload'),
    path('downloadjob/<slug:job_id>', cv.downloadjob, name='downloadjob'),
    path('viewjobinfoclient/<str:job_id>', cv.viewjobinfoclient, name='viewjobinfoclient'),
    path('payforjob/<slug:job_id>', cv.payforjob, name='payforjob'),
    path('transcation', cv.transcation, name='transcation'),
    path('makepayment/<slug:job_id>', cv.makepayment, name='makepayment'),
    path('verifypayment/<str:ref>', cv.verifypayment, name='verifypayment'),
    path('jobfeedback/<slug:job_id>', cv.jobfeedback, name='jobfeedback'),
    path('feedback_save', cv.feedback_save, name='feedback_save'),
    path('clientcompletedjobs', cv.completedjobs, name='clientcompletedjobs'),
    path('clientongoingjobs', cv.ongoingjobs, name='clientongoingjobs'),

]