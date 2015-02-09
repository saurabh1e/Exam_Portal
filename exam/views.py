import random
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.http import JsonResponse
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from exam.models import *
from user.models import UserProfile
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required

def index(request):
    context = RequestContext(request)
    return render_to_response('base.html', context)

@login_required(login_url='/user/login')
def test_name(request, t_id):
    context = RequestContext(request)
    test_id = Test.objects.get(s_id=t_id)
    print(request.user)
    if request.user is None:
        return render_to_response('/')
    user1 = UserProfile.objects.get(user=request.user)
    try:
        score_card = Score_Card.objects.get(user=user1, test=test_id)
        if score_card is not None and score_card.disables == True:
            return redirect('/exam/tests/')
    except ObjectDoesNotExist as e:
        print("got exception")
    request.session['user'] = request.user.username
    q_id = []
    count = Question.objects.filter(test=test_id).order_by('?')
    for i in count:
        q_id.append(i.ss_id)
    random.shuffle(q_id)
    request.session['count'] = q_id
    request.session['time'] = str(datetime.now() + timedelta(minutes=330))
    request.session['minutes'] = str(test_id.time)
    context_dict = {'t_id': t_id}
    print(request.session['count'])
    request.session['start'] = 1
    return render_to_response('test_name.html', context_dict, context)


@login_required(login_url='/user/login')
def test(request, t_id):
    if request.session['start'] == 1:
        request.session['time'] = str(datetime.now() + timedelta(minutes=330))
        request.session['start'] = 2
        print("inside time")

    print('started')
    context = RequestContext(request)
    length = len(request.session['count'])
    test_id = Test.objects.get(s_id=t_id)
    user1 = UserProfile.objects.get(user=request.user)
    try:
        score_card = Score_Card.objects.get(user=user1, test=test_id)
        if score_card is not None and score_card.disables == True:
            return redirect('/exam/results')
    except ObjectDoesNotExist as e:
        print("got exception")
    print('getting in post')
    if request.method == 'POST':
        if 'ans' in request.POST and 'ques' in request.POST:
            print("ans and ques in post")
            ans_id = request.POST['ans']
            ans1 = Answer.objects.get(id=ans_id)
            ques_id = request.POST['ques']
            print(ans1)
            print(ques_id)
            ques = Question.objects.get(test=test_id, ss_id=ques_id)
            try:
                Choice.objects.create(
                    test=test_id,
                    ques=ques,
                    user=user1,
                    ans=ans1,
                )

            except IntegrityError:
                print('error')
                if len(request.session['count']) < 1:
                    return redirect('/exam/results')
                else:
                    ques_id = request.session['last_ques']
                    ques = Question.objects.get(ss_id=ques_id)
                    ans = Answer.objects.filter(ques=ques)
                    context_dict = {'ques': ques, 'ans': ans, 'test': test_id, 'length': length}
                    return render_to_response("questions.html", context_dict, context)

            print("saving")
            marks = Score_Card.objects.get_or_create(user=user1, test=test_id)
            marks = Score_Card.objects.get(user=user1, test=test_id)
            if marks.disables == True:
                return redirect('/exam/results')
            if ans1.ans == ques.correct_answer:
                marks.score += test_id.postive
                print(marks.score)
            else:
                marks.score -= test_id.negative
                print(marks.score)
            marks.save()

            if len(request.session['count']) < 1:
                random_index = 0
                return redirect('/exam/results')
            else:
                request.session['last_ques'] = request.session['count'][-1]
                random_index = request.session['count'].pop()
                request.session.modified = True
                print(random_index)
                print(request.session['count'])
            ques = Question.objects.get(ss_id=random_index)
            ans = Answer.objects.filter(ques=ques)
            print(ques.id)
            context_dict = {'ques': ques, 'ans': ans, 'test': test_id, 'next_ques': random_index, 'length': length}
            return render_to_response("questions.html", context_dict, context)

        else:
            print("else")
            if len(request.session['count']) <= 0:
                    random_index = 0
                    return redirect('/exam/results')
            else:
                request.session['last_ques'] = request.session['count'][-1]
                random_index = request.session['count'].pop()
                request.session.modified = True
                print(random_index)
                print(request.session['count'])
                ques = Question.objects.get(ss_id=random_index)
                ans = Answer.objects.filter(ques=ques)
                print(ques.id)
                context_dict = {'ques': ques, 'ans': ans, 'test': test_id, 'length': length}
                return render_to_response("questions.html", context_dict, context)

    print('last')
    random_index = request.session['last_ques']
    ques = Question.objects.get(ss_id=random_index)
    ans = Answer.objects.filter(ques=ques)
    context_dict = {'ques': ques, 'ans': ans, 'test': test_id, 'length': length}
    return render_to_response("questions.html", context_dict, context)


@login_required(login_url='/user/login')
def results(request):

    context = RequestContext(request)
    users = UserProfile.objects.get(user=request.user.id)
    score_card = Score_Card.objects.filter(user=users)
    for scorecard in score_card:
        scorecard.disables = True
        print(scorecard.disables)
        scorecard.save()
    context_dict = {'score_card': score_card}
    return render_to_response('result.html', context_dict, context)


@login_required(login_url='/user/login')
def test_results(request, t_id):

    context = RequestContext(request)
    user = UserProfile.objects.get(user=request.user.id)
    test1 = Test.objects.get(s_id=t_id)
    question = Question.objects.filter(test=test1)
    choice = Choice.objects.filter(user=user, test=test1)
    context_dict = {'user': user, 'test': test1, 'question': question, 'choice': choice}

    return render_to_response('test_results.html', context_dict, context)

@login_required(login_url='/user/login')
def test_select(request):
    context = RequestContext(request)
    user = request.user
    userprof = UserProfile.objects.get(user=user.id)
    test = Test.objects.filter(branch_code__in=[userprof.branch_code, 0])
    context_dict = {'test': test}
    return render_to_response('test.html', context_dict, context)


def savetime(request):
    x = request.session['time']
    print(x)
    y = request.session['minutes']
    x = datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f")
    print(x)
    return JsonResponse({"result": x, "ti": int(y)})