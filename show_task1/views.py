from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from . import forms
from . import models
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.utils.decorators import method_decorator
from add_category.models import Category
from django.contrib.auth.models import User


@login_required
def add_post(request):
    if request.method == 'POST':
        post_form = forms.PostForm(request.POST)
        if post_form.is_valid():
            post_form.instance.author = request.user
            post_form.save()
            return redirect('homepage')  # Redirect to homepage or the list of posts
    else:
        post_form = forms.PostForm()

    return render(request, 'add_post.html', {'form': post_form})

@login_required
def edit_post(request, id):
    post = models.Post.objects.get(pk=id) 
    post_form = forms.PostForm(instance=post)
    # print(post.title)
    if request.method == 'POST': # user post request koreche
        post_form = forms.PostForm(request.POST, instance=post) # user er post request data ekhane capture korlam
        if post_form.is_valid(): # post kora data gula amra valid kina check kortechi
            post_form.save() # jodi data valid hoy taile database e save korbo
            return redirect('homepage') # sob thik thakle take add author ei url e pathiye dibo
    
    return render(request, 'add_post.html', {'form' : post_form})

@login_required
def delete_post(request, id):
    post = models.Post.objects.get(pk=id) 
    post.delete()
    return redirect('homepage')  # Redirect to homepage or the list of posts

# Class-based views
@method_decorator(login_required, name='dispatch')
class AddPostCreateView(CreateView):
    model = models.Post
    form_class = forms.PostForm
    template_name = 'add_post.html'
    success_url = reverse_lazy('homepage')  # Redirect to homepage or the list of posts

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class EditPostView(UpdateView):
    model = models.Post
    form_class = forms.PostForm
    template_name = 'add_post.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('profile')  # Redirect to profile or the list of posts

@method_decorator(login_required, name='dispatch')
class DeletePostView(DeleteView):
    model = models.Post
    template_name = 'delete.html'
    success_url = reverse_lazy('profile')  # Redirect to profile or the list of posts
    pk_url_kwarg = 'id'

class DetailPostView(DetailView):
    model = models.Post
    template_name = "post_detail.html"
    
    def post(self,request,*args,**kwargs):
     comment_form=forms.CommentForm(data=self.request.POST)
     post=self.get_object()
     if comment_form.is_valid():
                 new_comment=comment_form.save(commit=False)
                 new_comment.post=post
                 new_comment.save()
                 return self.get(request,*args,**kwargs)
     else:
                   comment_form=forms.CommentForm()
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post=self.object
        comments=post.comments.all()
        if self.request.method=='POST':
             comment_form=forms.CommentForm(data=self.request.POST)
            
             context['comments']=comments
             context['comment_form']=comment_form
             return context                 