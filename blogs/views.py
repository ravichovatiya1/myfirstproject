from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from blogs import forms
from blogs import models
import random # for otp sending to mail
from django.core.mail import send_mail  # this is for sending the plain email purpose.
from django.core.mail import EmailMultiAlternatives # this is to send the male with html templates
from django.template.loader import render_to_string # we we do an render operation it is used to return
from django.utils.html import strip_tags
from django.conf import settings # this is to import the setting in views file.
from django.contrib.auth import login,authenticate,logout # this is for login and logout
from django.contrib.auth.decorators import login_required # we have use this when we have to login in before add profile.  
from django.contrib.auth.mixins import LoginRequiredMixin # we used this when we we write the class instead of functions.

# Create your views here.

def index_page(request):
    return render(request,'base.html')


user = 0 # this is global variable for all the functions

def otp_varify(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        cotp = request.POST.get('conf_otp')

        if int(otp) == int(cotp):
            global user
            user.save()
            return HttpResponse('<h1>sucessfully registration done... </h1>')
    # return render(request,'registration/otp.html')


# this is used to send the template in email.
def register(request):
    form = forms.UserModelForm()
    if request.method == 'POST':
        form = forms.UserModelForm(request.POST)
        if form.is_valid():
            global user
            user = form.save(commit=False)
            mail = request.POST.get('email')
            password = request.POST.get('password')
            user.set_password(password)
            otp = random.randint(1111,9999)

            dct ={'otp':otp,'email': mail}
            html_content = render_to_string('registration/otp_verification_page.html',dct)
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(
                'Otp Verification',
                text_content,
                settings.EMAIL_HOST_USER,
                [mail,],
            )

            email.attach_alternative(html_content,'text/html')
            email.send()
            return render(request,'registration/otp.html', dct)
        return HttpResponse('regestration sucessful')        
    return render(request, 'registration/register.html', {'form':form})



# this is for the plain message sending

# def register(request):
#     form = forms.UserModelForm()
#     if request.method == 'POST':
#         form = forms.UserModelForm(request.POST)
#         if form.is_valid():
#             global user
#             user = form.save(commit=False)
#             mail = request.POST.get('email')
#             password = request.POST.get('password')
#             user.set_password(password)
#             otp = random.randint(1111,9999)
#             send_mail(
#                         'Otp Verification',
#                         f"your one time verification for registration is {otp}",
#                         settings.EMAIL_HOST_USER,
#                         [mail,],
#                         fail_silently=False,
#                     )
#             dct ={'otp':otp}
#             return render(request,'registration/otp.html', dct)
#         return HttpResponse('regestration sucessful')        
#     return render(request, 'registration/register.html', {'form':form})


 
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)
        if user :
            if user.is_active:
                login(request,user)
            # here we have create the sessions 
            # 1. ['user_login'] is set when user will login it will be true or else false in base.html 
            # 2. ['username'] is used to used to get the unique sessions of user using username
                request.session['user_login'] = True
                request.session['username'] = username
                print(request.session['username'])
                print('Sucessfully user login')
                return HttpResponseRedirect(reverse('app:index'))  
        else:
            return HttpResponse('<h1>Invalid Credentials</h1>')
    return render(request,'registration/web_login.html')


def user_logout(request):
    del request.session['user_login']
    del request.session['username']

    logout(request)
    return HttpResponseRedirect(reverse('app:index')) 


@login_required
def user_profile(request):
    form = forms.UserProfileModelForm()

    if request.method =='POST':
        form = forms.UserProfileModelForm(request.POST,request.FILES)

        if form.is_valid():

            profile = form.save(commit = False)
            username = request.session['username']
            user = models.User.objects.get(username = username)
            profile.user = user

            if 'Img_pic' in  request.FILES:
                profile.Img_pic = request.FILES['Img_pic']

            profile.save()

        else:
            print(form.errors)
            return HttpResponse('<h1>invalid forms</h1>')
    return render(request,'registration/profile.html',{'form':form})



###########################################################################
# creating using class based

from django.views.generic import (CreateView,ListView,DetailView,DeleteView,UpdateView)

class PostCreateView(LoginRequiredMixin,CreateView):
    model= models.Post
    login_url='/blogs/login/'
    # fields = ('author','Title','Text')
    # redirect_field_name = ''
    form_class = forms.PostModelForm

    def form_valid(self,form):
        if form.is_valid():
            obj = form.save(commit = False)
            username = self.request.session['username']
            user = models.User.objects.get(username = username)

            if obj.author == user :
                form = forms.PostModelForm(self.request.POST)
                return super().form_valid(form)
            else:
                return HttpResponse('<h1>Invalid user</h1>')
        else:
            return HttpResponse('<h1>Invalid Form</h1>')
                  





class PostDetailView(DetailView):
    model = models.Post




from django.utils import timezone
# this imported statement is for pagination query
# https://stackoverflow.com/questions/5907575/how-do-i-use-pagination-with-django-class-based-generic-listviews
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger


class PostListView(ListView):
    model = models.Post   
    paginate_by = 2 
    def get_queryset(self):
        return models.Post.objects.filter(Published_date__lte = timezone.now()).order_by('-Published_date')

# we have imported statement is for pagination query and useded hear.
    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs) 
        list_exam = self.model.objects.all()
        paginator = Paginator(list_exam, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
            
        context['list_exams'] = file_exams
        return context




class DraftListView(LoginRequiredMixin,ListView):
    model = models.Post
    login_url='/blogs/login/'

    def get_queryset(self):
        username = self.request.session['username']
        user = models.User.objects.get(username = username)
        return models.Post.objects.filter(author=user,Published_date__isnull= True).order_by('Created_date')

    

@login_required
def post_publish(request,pk):
    post = get_object_or_404(models.Post,pk=pk)
    post.published()
    return HttpResponse('<h1> Post Published </h1>')

@login_required
def post_drafts(request,pk):

    post = get_object_or_404(models.Post,pk=pk)
    post.drafted()
    return HttpResponse('<h1> Post drafted </h1>')

class PostUpdateView(LoginRequiredMixin,UpdateView):
    model = models.Post
    login_url='/blogs/login/'
    fields = ('Title','Text')


# this is used when we have to delete the post.
from django.urls import reverse_lazy
class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = models.Post
    login_url='/blogs/login/'
    success_url = reverse_lazy('app:post_draft')



def add_comment(request,pk):

    if request.method=='POST':
        form = forms.CommentModelForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            post = get_object_or_404(models.Post,pk=pk)
            obj.post = post
            obj.save()
            return HttpResponseRedirect(reverse('app:post_detail',kwargs={'pk':pk}))

    else:
        form = forms.CommentModelForm()
        return render(request,'blogs/comment.html',{'form': form,'pk':pk})



