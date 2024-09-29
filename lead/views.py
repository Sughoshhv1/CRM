from django.shortcuts import render
from .models import Lead
from rest_framework.views import APIView
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from authuser.models import AuthUser
from ticket.models import Ticket
from django.db.models import Count

# def leading(request):
#     customers = AuthUser.objects.all()

#     # Group tickets by city and count how many are from each city
#     ticket_counts_by_city = Ticket.objects.values('address').annotate(ticket_count=Count('t_id'))

#     context = {
#         "currentuser": request.session["user_data"],
#         'customer': customers,
#         'ticket_counts_by_city': ticket_counts_by_city
#     }
#     return render(request, 'lead/lead.html', context)


# Create your views here.
def leading(request):
    customers = AuthUser.objects.all()
    ticket1=Ticket.objects.all()
    context = {"currentuser" :request.session["user_data"], 'customer':customers,'ticket1':ticket1}
    return render(request, 'lead/lead.html',context)



class Createtkassign(APIView):
    def post(self, request):
        tech_id = request.POST['tech']
        ticket_id= request.POST['ticket']
        ass_date = request.POST['ass_date']
        ld_name = request.POST['ld_name']

        tech = AuthUser.objects.get(cid=tech_id)  # Fetching AuthUser instance
        ticket = Ticket.objects.get(t_id=ticket_id)  # Fetching Ticket instance
        usr = Lead()
        usr.tech = tech
        usr.ticket = ticket
        usr.lead_date  = ass_date
        usr.tk_name = ld_name
        usr.save()
        return JsonResponse({"status":"pass"})
    
class deletetkassign(APIView):
    def post(self, request):
        id = request.POST["id"]
        Lead.objects.filter(id=id).delete()
        return JsonResponse({"status":"pass"})
    
class Viewtkassignall(TemplateView):
    template_name = 'lead/alllead.html'
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        userdata = Lead.objects.all()
        customers = AuthUser.objects.all()
        ticket1=Ticket.objects.all()
        context={'userdata':userdata,'customer':customers,'ticket1':ticket1}
        return context

class Viewtkassign(TemplateView):
    template_name = 'lead/leadtable.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the current user from the session
        current_user_name = self.request.session.get("user_data")
        customers = AuthUser.objects.all()

        # Filter tickets with "Ticket Raised" or "Technician assigned" status
        ticket1 = Ticket.objects.filter(status__in=["Ticket Raised", "Technician Assigned"])

        # Filter userdata based on the current tech lead and filtered tickets
        userdata = Lead.objects.filter(tk_name=current_user_name, ticket__in=ticket1)

        # Update context with filtered userdata
        context.update({
            'userdata': userdata,
            'customer': customers,
            'ticket1': ticket1,
            'currentuser': current_user_name,
        })
        
        return context


class edit_user(APIView):
    def post(self, request):
        uid = request.POST['id']
        fullname1 = request.POST['fullname']
        password1 = request.POST['password']
        userdata = Lead.objects.filter(id=uid).update(tech=fullname1,lead_date=password1)
        return JsonResponse({"status":"pass"})
    
