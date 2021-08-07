from django.shortcuts import render
from profiles.models import Profile
from django.http import JsonResponse, HttpResponse
from .utils import get_report_image
from .models import Report
from django.views.generic import ListView, DetailView, TemplateView
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa


# Class for views


class ReportListView(ListView):
    model = Report
    template_name = 'reports/main.html'


class ReportDetailView(DetailView):
    model = Report
    template_name = 'reports/detail.html'


class UploadTemplateView(TemplateView):
    template_name = 'reports/from_file.html'


# Create your views here.


def create_report_view(request):
    if request.is_ajax():
        name = request.POST.get('name')
        remarks = request.POST.get('remarks')
        image = request.POST.get('image')
        img = get_report_image(image)
        author = Profile.objects.get(user=request.user)
        Report.objects.create(name=name, remarks=remarks,
                              image=img, author=author)
        return JsonResponse({
            'msg': "Sent"
        })
    return JsonResponse({})


def render_pdf_view(request, pk):
    template_path = 'reports/pdf.html'
    obj = Report.objects.get(pk=pk)
    context = {'obj': obj}
    # Create a Django response object and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # If download
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # If display
    response['Content-Disposition'] = 'filename="report.pdf"'
    # Find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # Create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # If error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def csv_upload_view(request):
    return HttpResponse()
