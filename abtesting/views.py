from django.shortcuts import render, redirect
from abtesting.models import Filter


def test(request):
    if not request.user.is_authenticated():
        return redirect('/login')

    filters = Filter.objects.filter()
    return render(request, 'abtesting/test.html', {"filters": filters})


def save_test(request):
    if not request.user.is_authenticated():
        return redirect('/login')

    if request.method != "POST":
        return redirect('/test')

    configs = request.FILES

    result = ""
    if not "configs" in configs.keys() and not "levels" in configs.keys():
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

    if not result:
        result = "Good!!!"

    return render(request, 'abtesting/test.html', {"filters": filters, 'result': result})
