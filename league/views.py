from django.utils import timezone
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth.models import User

from .forms import SignUpForm, FollowerForm, LeagueForm, NotificationForm
from .models import Leagues, Follower, Notification
from json import dumps, loads, JSONEncoder, JSONDecoder

from django.core import serializers

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/leagues')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
@login_required
def league(request):    
    template = loader.get_template('league/index.html')
    users = User.objects.all()
    content = {
        'leagueForm': LeagueForm(),
        'followerForm': FollowerForm(),
        'users': users
    }
    return HttpResponse(template.render(content, request))
@login_required
def save_league(request):        
    if request.method == 'POST':
        form = LeagueForm(request.POST)
        form.created_data = timezone.now
        user = request.user
        if form.is_valid():
            leagues = form.save(commit=False)
            leagues.manager = user
            leagues.save()           
            data = {
                'response_code': 1,
                'data': '',
                'message':'Create Leagues Successfully!'
            }
            return JsonResponse(data)
        else:
            data = {
                'response_code': 0,
                'data': form.errors,
                'message': 'Submit Invalidate!'
            }
            return JsonResponse(data)
    return JsonResponse({'response_code': 0, 'meassage': 'Not Posted data'})

@login_required
def get_leagues_table(request):
    send_data = []
    try:            
        leagues = Leagues.objects.all()
        for league in leagues:
            action = ''
            league_id = str (league.id)
            if league.manager.id == request.user.id:
                action = '<a class="btn-floating waves-effect waves-light blue" onclick="viewLeague('+league_id+')"><i class="material-icons dp48">visibility</i></a>'
                action = action + '<a class="btn-floating waves-effect waves-light deep-orange" onclick="removeLeague('+league_id+')"><i class="material-icons dp48">delete</i></a>'
                action = action + '<a class="btn-floating waves-effect waves-light cyan lighten-1" onclick="sendInvitation('+league_id+')"><i class="material-icons dp48">contacts</i></a>'
            else:            
                action = '<a class="btn-floating waves-effect waves-light blue" onclick="viewLeague('+league_id+')"><i class="material-icons dp48">visibility</i></a>'            
                action = action + '<a class="btn-floating waves-effect waves-light deep-orange" onclick="joinLeague('+league_id+')"><i class="material-icons dp48">share</i></a>'
            send_data.append({
                'name':league.name,
                'terms': league.terms,
                'manager': league.manager.username,
                'created_date': league.created_date.strftime('%m/%d/%Y'),
                'action': action
            })
    except Leagues.DoesNotExist:
        send_data = []
    data = {'data': send_data}
    return JsonResponse(data)   

@login_required
def get_league_userlist(request):
    send_data = []
    followers = [] 
    try:
        if request.GET.get('league'):
            league_id = request.GET.get('league')
            league = Leagues.objects.get(id=league_id)
            followers = Follower.objects.filter(league=league)      
        else:
            followers = Follower.objects.all()
    except Follower.DoesNotExist:
        followers = []
    if len(followers) == 0:
            return JsonResponse({'data':[]})
    else:
        for follower in followers:
            send_data.append({
                'user':follower.user.username,
                'league':follower.league.name,
                'manager': follower.league.manager.username,
                'date':follower.created_date.strftime('%m/%d/%Y')
            })
    return JsonResponse({'data':send_data})

@login_required
def delete_league(request):
    message = ''
    response_code = 0
    try:
        if request.POST.get('league'):
            Leagues.objects.filter(id=request.POST.get('league')).delete()   
            response_code= 1   
            message = 'Delete successfully!'
        else:
            message = 'Delete error!'
    except Leagues.DoesNotExist:
        message = 'Delete error!'
    return JsonResponse({'message':message, 'response_code': response_code})
@login_required
def join_league(request):
    message = ''
    response_code = 0
    follower = {}
    try:
        if request.POST.get('league'):
            league = Leagues.objects.filter(id=request.POST.get('league')).get()   
            user = User.objects.filter(id=request.POST.get('user_id')).get()  
            already = Follower.objects.filter(user=user).filter(league=league)
            if already:
                message = 'Already Joined!'
            else:
                follower = Follower.objects.create(
                    league = league,
                    user = user,
                    status = 0
                )
                response_code= 1   
                message = 'Join successfully!'
        else:
            message = 'Join error!'
    except Leagues.DoesNotExist:
        message = 'Join error!'
    return JsonResponse({'message':message, 'response_code': response_code, 'data': '' })
@login_required
def send_invitation(request):
    message = ''
    response_code = 0
    try:
        if request.POST.get('league'):
            league = Leagues.objects.filter(id=request.POST.get('league')).get()
            users = request.POST.getlist('user[]')
            content = request.POST.get('content')
            print(users)
            if len(users) == 0:
                message = 'There is no Invited Users'                                
            else:
                for user_id in users:
                    if int(user_id) == request.user.id:
                        continue
                    user = User.objects.filter(id=user_id).get()
                    already = Notification.objects.filter(user=user).filter(league=league)
                    if already:
                        continue
                    Notification.objects.create(
                        league = league,
                        user = user,
                        content = content,
                        status = 0
                    )
                response_code= 1   
                message = 'Invite successfully!'
        else:
            message = 'Invite error!'
    except User.DoesNotExist:
        message = 'Join error!'
    return JsonResponse({'message':message, 'response_code': response_code, 'data':  users})

@login_required
def notification(request):
    template = loader.get_template('league/notification.html')
    users = User.objects.all()
    content = {
        'leagueForm': LeagueForm(),
        'followerForm': FollowerForm(),
        'users': users
    }
    return HttpResponse(template.render(content, request))
@login_required
 
def get_incoming_table(request):
    send_data = []
    try:
        notifications = Notification.objects.all()
        print(notifications)
        action = ''
        for notification in notifications:
            if notification.user != request.user:
                continue
            if notification.status == 0:
                status = '<a class="btn-small  blue lighten-4">stand by..</a>'       
                action = '<button type="button" class="btn-floating btn-small waves-effect waves-light  blue" onclick="update_notification('+str(notification.id)+', 1' + ')"><i class="material-icons dp48">done</i></button>'         
                action += '<button type="button" class="btn-floating btn-small waves-effect waves-light pink" onclick="update_notification('+str(notification.id)+', 2' + ')"><i class="material-icons dp48">replay</i></button>'                 
            elif notification.status == 1:
                status = '<a class="btn-small purple">accepted</a>'                
            else:
                status = '<a class="btn-small red lighten-1">rejected</a>'                    
            send_data.append({
                'league': notification.league.name,
                'manager': notification.league.manager.username,
                'user': notification.user.username,
                'status':status,
                'action': action
            })
    except Notification.DoesNotExist:
        send_data = []
    return JsonResponse({'data':send_data})
def get_outcoming_table(request):
    send_data = []
    try:
        notifications = Notification.objects.all()
        print(notifications)
        action = ''
        for notification in notifications:
            if notification.league.manager != request.user:
                continue
            if notification.status == 0:
                status = '<a class="btn-small  blue lighten-4">stand by..</a>'       
                action = '<a class="btn-floating btn-small waves-effect waves-light onclick ="update_notification('+str(notification.id)+', 1' + ')" blue"><i class="material-icons dp48">done</i></a>'         
                action += '<a class="btn-floating btn-small waves-effect waves-light pink" onclick ="update_notification('+str(notification.id)+', 2' + ')"><i class="material-icons dp48">replay</i></a>'         
            elif notification.status == 1:
                status = '<a class="btn-small purple">accepted</a>'                
            else:
                status = '<a class="btn-small red lighten-1">rejected</a>'                    
            send_data.append({
                'league': notification.league.name,
                'manager': notification.league.manager.username,
                'user': notification.user.username,
                'status':status,
                'content': notification.content,
                'date': notification.created_date.strftime('%m/%d/%Y')                
            })
    except Notification.DoesNotExist:
        send_data = []
    return JsonResponse({'data':send_data})
@login_required

def update_notification(request):
    message = ''
    response_code = 0
    try:
        if request.POST.get('notification_id'):
            notification = Notification.objects.filter(id=int(request.POST.get('notification_id')))  
            notification.update(status=int(request.POST.get('status')))
            print(int(request.POST.get('notification_id')))
            if int(request.POST.get('status')) == 1:
                user =  Notification.objects.get(id=int(request.POST.get('notification_id'))).user
                league =  Notification.objects.get(id=int(request.POST.get('notification_id'))).league    
                already = Follower.objects.filter(user=user).filter(league=league)
                if already:
                    message = 'Already Joined!'
                else:
                    Follower.objects.create(
                        league = league,
                        user = user,
                        status = 0
                    )
                message = 'Accepted successfully!'            
            else:
                message = 'Rejected successfully!'            
            response_code= 1 
        else:
            message = 'Join error!'
    except Notification.DoesNotExist:
        message = 'Update error!'
    return JsonResponse({'message':message, 'response_code': response_code, 'data': '' })
@login_required

def profile(request):
    template = loader.get_template('league/profile.html')
    users = request.user
    content = {
        'users': users
    }
    return HttpResponse(template.render(content, request))
        
