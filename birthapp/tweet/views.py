from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm, UserRegistrationForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
import datetime
from django.core.mail import send_mail
from django.conf import settings
import logging 

logger = logging. getLogger(__name__)

def update_mail_status(tweets):
    """ update mail status """
    currentday = datetime.date.today() 
    for email_info in tweets:
        if currentday.month == email_info.date_of_birth.month and currentday.day == email_info.date_of_birth.day:
            if email_info.email and email_info.text and email_info.email_status != 'Email sent successfully':
                try:
                    send_mail('Best wishes for your special day', email_info.text, settings.EMAIL_HOST_USER, [email_info.email])
                    email_info.email_status = 'Email sent successfully'
                except Exception as e:
                    email_info.email_status = f'Error sending email: {e}'
            ### save email status
            email_info.save()
    return

def remind_birth_day(birthdays):
    """ remind birth day condition check"""
    currentday = datetime.date.today() 
    maxdays = 7
    try:
        replace_year_bday = birthdays.replace(year=currentday.year)
    except ValueError: # 29 Feb can't be map to non-leap year
        replace_year_bday = birthdays.replace(year=currentday.year, day=28) # Choose 28 Feb here
    if abs((replace_year_bday - currentday).days) <= maxdays:
        return True

def index(request):
    return render(request,'index.html')

def tweet_list(request):
    if request.user.is_authenticated:
        tweets = Tweet.objects.filter(user = request.user ) 
        if tweets:
            update_mail_status(tweets)
            username = tweets[0].user.username
            remind_tweets = [] 
            for tweet in tweets:
                if tweet.date_of_birth and remind_birth_day(tweet.date_of_birth):
                    remind_tweets.append(tweet)
            return render(request, 'tweet_list.html', {'tweets': tweets, 'remind_tweets' : remind_tweets, 'username':username})
        else:
            return render(request, 'tweet_list.html', {'tweets': tweets, 'remind_tweets' : '', 'username':request.user})
    else:
        # Redirect anonymous users to login
        return redirect('login')

@login_required
def tweet_create(request):
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request,'tweet_form.html',{'form': form})

@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id , user =   request.user)
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')

    else:
        form = TweetForm(instance=tweet)
    return render(request,'tweet_form.html',{'form': form})

@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id , user =   request.user)
    if request.method == "POST":
        tweet.delete()
        return redirect('tweet_list')
    return render(request,'tweet_confirm_delete.html',{'tweet': tweet})


def register(request):
    if request.method=="POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request,user)
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()
    return render(request,'registration/register.html',{'form': form})
