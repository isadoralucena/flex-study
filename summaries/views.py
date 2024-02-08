from django.shortcuts import render, redirect
from . models import Summary, SummaryViews
from django.contrib.messages import constants
from django.contrib import messages

def create_summary(request):
    if request.method == 'GET':
        summaries = Summary.objects.filter(user=request.user)
        total_views = SummaryViews.objects.filter(summary__user = request.user).count()

        return render(request, 'create_summary.html', {'summaries': summaries, 'total_views': total_views})
    elif request.method == 'POST':
        title = request.POST.get('title')
        file = request.FILES['file']

        summary = Summary(user=request.user, title=title, file=file)
        summary.save()
        messages.add_message(request, constants.SUCCESS, 'Apostila adicionada com sucesso.')
        return redirect('/summaries/create_summary/')

def summary(request, id):
    summary = Summary.objects.get(id=id)

    unique_views = SummaryViews.objects.filter(summary = summary).values('ip').distinct().count()
    total_views = SummaryViews.objects.filter(summary = summary).count()

    view = SummaryViews(ip = request.META['REMOTE_ADDR'], summary = summary)
    view.save()

    return render(request, 'summary.html', {'summary': summary, 'unique_views': unique_views, 'total_views': total_views})