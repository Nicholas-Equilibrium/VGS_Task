import json
import os
import requests
from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.conf import settings

from .models import PiiData

vgs_outbound_route = getattr(settings, "OUTBOUND_ROUTE", None)

def index(request):
    pii_data_list = PiiData.objects.order_by('-pub_date')[:5]
    host = getattr(settings, "INBOUND_ROUTE", "")
    context = {
        'pii_data_list': pii_data_list,
        'host': host
    }
    return render(request, 'app/index.html', context)


def add(request):
    cc_number = request.POST['cc_number']
    cc_exp = request.POST['cc_exp']
    cc_cvv = request.POST['cc_cvv']
    pii_data = PiiData(cc_number=cc_number, cc_exp=cc_exp, cc_cvv=cc_cvv, pub_date=datetime.now())
    pii_data.save()
    return HttpResponseRedirect("/app/" + str(pii_data.id) + "/")


def detail(request, data_id):
    pii_data = get_object_or_404(PiiData, pk=data_id)
    host = getattr(settings, "INBOUND_ROUTE", "")
    context = {
        'pii_data': pii_data,
        'host': host
    }
    return render(request, 'app/detail.html', context)


def turn_on_outbound():
    if vgs_outbound_route is not None:
        os.environ["HTTPS_PROXY"] = vgs_outbound_route
        os.environ["REQUESTS_CA_BUNDLE"] = os.getcwd() + '/app/cert.pem'


def turn_off_outbound():
    if vgs_outbound_route is not None:
        del os.environ["HTTPS_PROXY"]
        del os.environ["REQUESTS_CA_BUNDLE"]


def check(request, data_id):
    pii_data = get_object_or_404(PiiData, pk=data_id)
    try:
        turn_on_outbound()
        context = {
         'cc_number': pii_data.cc_number,
         'cc_exp': pii_data.cc_exp,
         'cc_cvv': pii_data.cc_cvv,
        }
        r = requests.post(
            "https://echo.apps.verygood.systems/post",
            json=context,
            verify=os.getcwd() + '/app/cert.pem'
        )

        turn_off_outbound()

    except CheckerServiceException as e:
        return HttpResponse(json.dumps({"status_code": e.status_code, "error:": e.error}),
                            content_type="application/json")

    return HttpResponse(r.text, content_type="application/json")


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))

def get_data(request, data_id):
    pii_data = get_object_or_404(PiiData, pk=data_id)
    return HttpResponse(json.dumps({
        'id': pii_data.id,
        'cc_number': pii_data.cc_number,
        'cc_exp': pii_data.cc_exp,
        'cc_cvv': pii_data.cc_cvv,
        'pub_date': pii_data.pub_date,
    }, default=json_serial), content_type="application/json")
