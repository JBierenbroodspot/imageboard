from django.contrib.auth import forms as auth_forms, login, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.views import View

from novachan.forms import *
from novachan.models import *


# Create your views here.
class MainView(View):

    def get(self, request):
        template = 'novachan/index.html'
        topics = Topic.objects.all()
        render_args = {
            'topics': topics,
        }
        return render(request, template, render_args)


class TopicView(View):
    # TODO Maybe ad *args and **kwargs so that url can be turned into an attribute
    # TODO Maybe find a way to merge TopicView and ThreadView and base them of a single ParentView
    def get(self, request, url):
        topic = Topic.objects.get(url=url)
        threads = Thread.objects.filter(topic_id=topic)
        replies = Reply.objects.filter(thread_id__in=threads)

        form = SubmitPostForm()  # Generate empty form
        return render(request, 'novachan/topic.html', {
            'threads': threads,
            'topic': topic,
            'replies': replies,
            'form': form
        })

    def post(self, request, url):
        form = SubmitPostForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name'] if form.cleaned_data['name'] else _('Anonymous')
            text = form.cleaned_data['text']
            image = form.cleaned_data['image']
            topic = Topic.objects.get(url=url)

            Thread.objects.create(name=name, text=text, image=image, topic_id=topic.id)
            return HttpResponseRedirect(request.path_info)  # Prevent from resubmitting same form by redirecting

        else:
            return HttpResponseRedirect(request.path_info)


class ThreadView(View):
    def get(self, request, url, id):
        topic = Topic.objects.get(url=url)
        thread = Thread.objects.get(id=id)
        replies = Reply.objects.filter(thread_id=thread.pk)
        form = SubmitPostForm()
        return render(request, 'novachan/thread.html', {
            'topic': topic,
            'thread': thread,
            'replies': replies,
            'form': form
        })

    def post(self, request, url, id):
        form = SubmitPostForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name'] if form.cleaned_data['name'] else 'Anonymous'
            text = form.cleaned_data['text']
            image = form.cleaned_data['image']

            Reply.objects.create(name=name, text=text, image=image, thread_id_id=id)
            return HttpResponseRedirect(request.path_info)  # Prevent from resubmitting same form by redirecting

        else:
            return HttpResponseRedirect(request.path_info)
