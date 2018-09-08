from django.shortcuts import render, redirect
from abtesting.models import Filter
from abtesting.consts import current_server

import json
import requests
import time



def test(request):
    if not request.user.is_authenticated():
        return redirect('/login')

    filters = Filter.objects.filter()
    return render(request, 'abtesting/test.html', {"filters": filters})


def ab_tests(request):
    if not request.user.is_authenticated():
        return redirect('/login')

    r = requests.get(current_server + "get_ab_tests?key=6b7b1a88b2aa45eb9f861d9c86e67696")
    tests = json.loads(r.text)
    return render(request, 'abtesting/tests_info.html', {"tests": tests})


def off_ab_test(request):
    if not request.user.is_authenticated():
        return redirect('/login')

    ab_key = request.GET["ab_key"]
    requests.get(current_server + "off_ab_test?key=6b7b1a88b2aa45eb9f861d9c86e67696&ab_id=" + ab_key)
    time.sleep(1)
    return redirect('ab_tests')


def on_ab_test(request):
    if not request.user.is_authenticated():
        return redirect('/login')

    ab_key = request.GET["ab_key"]
    requests.get(current_server + "on_ab_test?key=6b7b1a88b2aa45eb9f861d9c86e67696&ab_id=" + ab_key)
    time.sleep(1)
    return redirect('ab_tests')


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

    filters = Filter.objects.filter()
    for filter in filters:
        filter_data = request.POST[filter.name]
        if not filter_data:
            result += filter.name + " can't be null "

    if result:
        return render(request, 'abtesting/test.html', {"filters": filters, 'result': result})

    filters_dict = dict()
    for filter in filters:
        filter_value = request.POST[filter.name]
        filter_type = request.POST[filter.name + "_type"]
        filters_dict[filter.name] = {"filter_value": filter_value, "filter_type": filter_type}

    filters_json = json.dumps(filters_dict)
    data = {"name": testing_name, "probability": testing_probability,
            "user_count": testing_user_count, "filters": filters_json}

    files = list()
    for level in levels:
        files.append(("levels", level))

    for config in configs:
        files.append(("configs", config))

    r = requests.post(current_server + "save_test?key=6b7b1a88b2aa45eb9f861d9c86e67696", files=files, data=data)
    if not result:
        result = r.text

    return render(request, 'abtesting/test.html', {"filters": filters, 'result': result})
