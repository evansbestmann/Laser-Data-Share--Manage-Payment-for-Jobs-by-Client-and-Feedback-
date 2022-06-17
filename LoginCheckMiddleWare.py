#the goal of this is to restrict on type of user acessing other user type pages
#after all the restriction code here you pass the  middleware class in the maddleware.py  in settings.py
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
import django.contrib.admin.sites

import django.contrib.admin.sites




class LoginCheckMiddleWare(MiddlewareMixin):
    def process_view(self,request,view_func,view_args, view_kwargs):
        modulename=view_func.__module__
        #print(modulename)
        user=request.user
        if user.is_authenticated:
            #so only user 1 type can access hodviews
          if user.user_type == "1":
            if modulename == "client.adminviews":
                pass
            elif (modulename == django.contrib.admin.sites):
                pass
            elif modulename == "client.views" or modulename == "django.views.static":# or modulename == "django.views.static" will let middleware allow static files
                pass
            else:
                return HttpResponseRedirect(reverse("admin_home"))
            # so only user 2 type can access staffviews
          elif user.user_type == "2":
            if modulename == "client.clientviews":
                pass
            elif modulename == "client.views" or modulename == "django.views.static":
                pass
            else:
                return HttpResponseRedirect(reverse("client_home"))
          elif request.path == reverse("#baseadmin"):
                  return HttpResponseRedirect(reverse("#baseadmin"))
          else:
              #else return to login page
              return HttpResponseRedirect(reverse("login"))
        else:
            #if user not authenticated but try to access login and user_details views(trmplates)
            #the middleware with do nothing asin "pass" and return user to login view(template)
            if request.path == reverse("login") or request.path == reverse("dologin"):
                pass
            else:
                return HttpResponseRedirect(reverse("login"))


