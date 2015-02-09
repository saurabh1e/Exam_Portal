from django.contrib.auth.decorators import login_required
from user.models import UserProfile, ProjectDetails
from django.template import RequestContext
from django.shortcuts import render_to_response, HttpResponseRedirect, redirect
from django.contrib.auth.models import User, AnonymousUser
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import logout, login, authenticate

@login_required()
def user_profile(request, p_id):
    context = RequestContext(request)

    print(p_id)
    user_prof = UserProfile.objects.get(roll_number=p_id)
    user = User.objects.get(profile=user_prof.user)
    projects = ProjectDetails.objects.filter(user=user_prof)
    print(projects)
    context_dict = {'user': user, 'userprofile': user_prof, 'projects': projects}
    return render_to_response('userprofile.html', context_dict, context)

@login_required()
def curr_profile(request):
    context = RequestContext(request)
    print(request.user)
    if request.user == AnonymousUser():
        return HttpResponse('No profile for anonymous user')
    user = request.user
    user_prof = UserProfile.objects.get(user=user.id)
    projects = ProjectDetails.objects.filter(user=user_prof)
    print(projects)
    context_dict = {'user': user, 'userprofile': user_prof, 'projects': projects}
    return render_to_response('curr_userprofile.html', context_dict, context)


def register_user(request):
    context = RequestContext(request)
    print("registration started")

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        roll_no = request.POST['roll_no']
        email = request.POST['email']
        if str(password) == str(cpassword):
            try:
                print("creating user")
                user = User.objects.create_user(username, email, password)
                print("creating userprofile")
                userprof = UserProfile(user.id, roll_no)
                print("created userprofile")
            except TypeError:
                return HttpResponse("Error Processing Request")
            else:
                print("saving user")
                user.save()
                print("saving profile")
                userprof.save()
            return render_to_response('login.html')
        elif str(password) != str(cpassword):
            return HttpResponse("password mismatch")
    return render_to_response('register.html', context)

@login_required
def user_logout(request):
    context = RequestContext(request)
    logout(request)
    return HttpResponseRedirect('/')


def user_login(request):
    context = RequestContext(request)
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/', )
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render_to_response('login.html', {}, context)

@login_required()
def All_User(request):
    context = RequestContext(request)
    return render_to_response('all_user.html', context)


@login_required()
def user_data(request):
    context = RequestContext(request)
    users = UserProfile.objects.order_by('roll_number').all()
    result = []
    for user in users:
        data = []
        data.append('<a href="/user/profile/'+str(user.roll_number)+'">'+user.user.first_name+'</a>')
        data.append(user.user.last_name)
        data.append(user.roll_number)
        result.append(data)
    return JsonResponse({"results": result})