from django.shortcuts import render, redirect
from abtesting.models import Filter
from abtesting.consts import prod_server, dev_server

from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.files.uploadedfile import UploadedFile
from django.template import RequestContext

import json
import requests
import time
import uuid

import os.path


def test(request):
    if not request.user.is_authenticated():
        return redirect('/login')

    server = request.GET["server"]
    if not server:
        return redirect('/')

    filters = Filter.objects.filter()

    session_key = uuid.uuid4()

    return render(request, 'abtesting/test2.html',
                  {"filters": filters, "server": server, "session_key": session_key})


def ab_tests(request):
    if not request.user.is_authenticated():
        return redirect('/login')

    server = request.GET["server"]
    if not server:
        return redirect('/')

    if server == "prod":
        current_server = prod_server
    else:
        current_server = dev_server

    r = requests.get(current_server + "get_ab_tests?key=6b7b1a88b2aa45eb9f861d9c86e67696")
    tests = json.loads(r.text)
    return render(request, 'abtesting/tests_info.html', {"tests": tests, "server": server})


def set_ab_status(request):
    if not request.user.is_authenticated():
        return redirect('/login')

    server = request.GET["server"]
    if not server:
        return redirect('/')
    if server == "prod":
        current_server = prod_server
    else:
        current_server = dev_server

    ab_key = request.GET["ab_key"]
    ab_status = request.GET["ab_status"]
    r = requests.get(current_server + "set_ab_test_status?ab_status=" + ab_status +
                     "&key=6b7b1a88b2aa45eb9f861d9c86e67696&ab_id=" + ab_key)
    time.sleep(1)
    return redirect('/ab_tests?server=' + server)


def save_test(request):
    if not request.user.is_authenticated():
        return redirect('/login')

    if request.method != "POST":
        return redirect('/test')

    configs = request.FILES.getlist("configs")
    levels = request.FILES.getlist("levels")

    result = ""
    if not configs and not levels:
        result += "files can't be null"

    testing_name = request.POST['testing_name']
    if not testing_name:
        result += "testing_name can't be null "

    testing_probability = request.POST['testing_probability']
    if not testing_probability:
        result += "testing_probability can't be null "

    testing_user_count = request.POST['testing_user_count']
    if not testing_user_count:
        result += "testing_user_count can't be null "

    server = request.POST['server']
    if not testing_user_count:
        result += "server can't be null"

    filters = Filter.objects.filter()
    for filter in filters:
        filter_data = request.POST[filter.name]

        if not filter_data and filter.name + "_is_on" in request.POST.keys():
            result += filter.name + " can't be null;\n"

    if result:
        return render(request, 'abtesting/test2.html', {"filters": filters, 'result': result})

    filters_dict = dict()
    for filter in filters:
        filter_value = request.POST[filter.name]
        filter_type = request.POST[filter.name + "_type"]
        filter_data_type = request.POST[filter.name + "_data_type"]

        if filter.name + "_is_on" in request.POST.keys():
            filters_dict[filter.name] = {"filter_value": filter_value, "filter_type": filter_type,
                                         "filter_data_type": filter_data_type}

    filters_json = json.dumps(filters_dict)
    data = {"name": testing_name, "probability": testing_probability,
            "user_count": testing_user_count, "filters": filters_json}

    files = list()
    load_levels = list()
    if "loadLevelsFiles" in request.POST.keys():
        load_levels = json.loads(request.POST["loadLevelsFiles"])

    for level in levels:
        if level.name in load_levels:
            files.append(("levels", level))

    load_configs = list()
    if "loadConfigsFiles" in request.POST.keys():
        load_configs = json.loads(request.POST["loadConfigsFiles"])

    for config in configs:
        if config.name in load_configs:
            files.append(("configs", config))

    print(files)

    if server == "prod":
        pass
        r = requests.post(prod_server + "save_test?key=6b7b1a88b2aa45eb9f861d9c86e67696", files=files, data=data)
        result = r.text
    elif server == "dev":
        pass
        r = requests.post(dev_server + "save_test?key=6b7b1a88b2aa45eb9f861d9c86e67696", files=files, data=data)
        result = r.text

    return render(request, 'abtesting/test2.html', {"filters": filters, 'result': result, "server": server})
