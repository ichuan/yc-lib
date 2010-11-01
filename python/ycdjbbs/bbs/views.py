# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django.views.generic.list_detail import object_list
from django.http import HttpResponseRedirect, HttpResponse, Http404
from ycdjbbs.bbs.forms import PostForm, ReplyForm
from ycdjbbs.bbs.models import *

def register(request):
    context = {}
    if request.POST:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect('/accounts/login')
        else:
            context['errors'] = form.errors
    context['form'] = UserCreationForm()
    return render_to_response('registration/register.html', RequestContext(request, context))

def post_list(request):
    '''
    '''
    params = {'extra_context': {}}
    tag = request.GET.get('tag', None)

    if tag is None:
        params['queryset'] = Post.objects.filter(parent=None).select_related()
    else:
        t = get_object_or_404(Tag, tag_name=tag)
        params['extra_context']['tag'] = tag
        params['queryset'] = t.post_set.filter(parent=None).select_related()

    params['paginate_by'] = int(request.GET.get('pagesize', 20)) # todo
    params['page'] = int(request.GET.get('page', 1)) # todo

    return object_list(request, **params)


@login_required
def new_post(request):
    '''
    '''
    if request.POST:
        form = PostForm(request.POST)
        tags = request.POST.get('tags', '').split(',')
        if form.is_valid():
            tag_list = []
            for i in tags:
                try:
                    j, created = Tag.objects.get_or_create(tag_name=i)
                except AssertionError:  # more than 1 items returned
                    continue
                tag_list.append(j)
            if len(tag_list):
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                post.tags.add(*tag_list);
            else:
                post = form.save()

            if request.GET.get('ajax', '') == 'true':
                obj = {'id': post.id, 'subject': post.subject, 'author': post.author.username, 'tags': tags}
                import json
                return HttpResponse(json.dumps(obj))
            return HttpResponseRedirect('/bbs/post/%d' % post.id)

    form = PostForm()

    return render_to_response('bbs/new_post.html', RequestContext(request, {'form': form}))

@login_required
def new_reply(request, post_id):
    parent = get_object_or_404(Post, pk=post_id)
    if request.POST:
        form = ReplyForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.parent = parent
            post.save()
            return HttpResponseRedirect('/bbs/post/%d' % parent.id)
    form = ReplyForm()
    return render_to_response('bbs/new_reply.html', RequestContext(request, {'form': form}))

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.id != int(post_id):
        raise Http404('Post not exists')
    if request.POST:
        form = PostForm(request.POST)
        if form.is_valid():
            tag_list = []
#tags = set(map(lambda x:x.tag_name, post.tags.all())) | set(request.POST.get('tags', '').split(','))
            tags = set(request.POST.get('tags', '').split(','))
            post.tags.clear()
            for i in tags:
                try:
                    j, created = Tag.objects.get_or_create(tag_name=i)
                except AssertionError:  # more than 1 items returned
                    continue
                tag_list.append(j)
            if len(tag_list):
                post.tags.add(*tag_list);
            post.subject = request.POST.get('subject', '')
            post.content = request.POST.get('content', '')
            post.save()
            return HttpResponseRedirect('/bbs/post/%d' % post.id)
    return render_to_response('bbs/edit_post.html', RequestContext(request, {'post': post}))

@login_required
def del_post(request, post_id):
    if not request.user.is_superuser:
        raise Http404('Post not exists')
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return HttpResponseRedirect('/bbs')

def view_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    replies = Post.objects.filter(parent=post).order_by('-created').select_related()
    return render_to_response('bbs/view_post.html', locals())
