from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.utils.html import escape
from social.models import User, Post, Vote
from social.forms import PostForm, EditForm, DeleteForm
from social.serializers import PostSerializer#, VoteSerializer
from rest_framework import generics
from rest_framework.response import Response

def post(request):
    if request.user.is_authenticated and request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('post_text')
            image = request.FILES.get('post_image')
            date = timezone.now()            
            post = Post(post_text=text, user=request.user, pub_date=date)
            if image:
                post = Post(post_text=text, user=request.user, pub_date=date, image=image)
            post.save()

            data = {}
            data['post_image'] = None
            if image:
                data['post_image'] = post.image.url
            data['post_text'] = escape(post.post_text)
            data['post_date'] = post.get_readable_date()
            data['post_id'] = post.pk
            data['user_id'] = request.user.pk
            data['username'] = request.user.username
            return JsonResponse(data)    
    return redirect('/')



def databasecheck(request, post_id):
    if request.user.is_authenticated:
        data={'currentId':Post.objects.last().pk, 'lastId':post_id}
        return JsonResponse(data)
    return redirect('/')

            
class GetPostInfo(generics.RetrieveAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    

class VoteOnPost(generics.GenericAPIView):
    queryset = Vote.objects.all()
        
    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        post = get_object_or_404(Post, pk=request.POST.get('post_id'))
        vote = request.POST.get('vote')
        already_voted = queryset.filter(voted_by=request.user, voted_post=post).first()
        if already_voted:
            if already_voted.vote == 'L' and vote != 'L':
                already_voted.vote = 'D'
                already_voted.save()
            elif already_voted.vote == 'D' and vote != 'D':
                already_voted.vote = 'L'
                already_voted.save()
            else:
                already_voted.delete()
        else:
            already_voted = Vote(voted_post=post, voted_by=request.user, vote=vote)
            already_voted.save()
        likes = Vote.objects.filter(vote='L', voted_post=post).count()
        dislikes = Vote.objects.filter(vote='D', voted_post=post).count()
        data = {'total_likes':likes, 'total_dislikes':dislikes}
        return Response(data)


def edit(request):
    if request.user.is_authenticated and request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('id')
            post = get_object_or_404(Post, pk=post_id)
            if request.user == post.user:
                new_text = form.cleaned_data.get('new_text')
                post.post_text = new_text
                post.save()
                data = { 'new_text': escape(new_text) }
                return JsonResponse(data)
    return redirect('/')



def delete(request):
    if request.user.is_authenticated:
        post_id = request.GET.get('id')
        post = get_object_or_404(Post, pk=post_id)
        if request.user == post.user:
            post.delete()
            data = { 'post_id': post_id }
            return JsonResponse(data)
    return redirect('/')


