import json

from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.template import RequestContext
from django.core import serializers

from myapplication.models import Message, Report, PublicKey, ReportFile, ReportFolder
from django.contrib.auth.models import User, Group
from myapplication.forms import UserForm, GroupForm, SendMessage, ReportForm, ReportFolderForm
from Crypto.PublicKey import RSA
from datetime import datetime
from mysite import settings
from django.db.models import Q

# Create your views here.
from mysite.settings import MEDIA_URL


def index(request):
    report_list=Report.objects.all()
    Mlist = Message.objects.filter(recipient=request.user.username, viewed=False)
    if len(Mlist) != 0:
        NewM = True
    else:
        NewM= False
    context_dict = {'Reports' : report_list, 'NewM':NewM}

    return render(request, 'index.html', context_dict)


def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                if (user.is_staff):
                    login(request,user)
                    return HttpResponseRedirect('/myapplication/manager/')
                login(request, user)
                return HttpResponseRedirect('/myapplication/')
            else:
                return HttpResponse("Your account is disabled")

        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render_to_response('login.html', {}, context)


def register(request):
    context = RequestContext(request)

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render_to_response('register.html', {'user_form': user_form, 'registered': registered},
                              context)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/myapplication/')

def settings(request):
    if request.method == 'POST':
        if request.POST['change_password']:
            new_pass = request.POST['change_password']
            u = request.user
            u.set_password(new_pass)
            u.save()
            return HttpResponseRedirect('/myapplication/')
    return render(request, 'settings.html')


def manager(request):
    if request.user.is_staff:
        user_list = User.objects.all()
        group_list = Group.objects.all()
        group_form = GroupForm()
        create_manager = True

        manager_list = User.objects.filter(is_staff=True)
        num_managers = len(manager_list)
        if num_managers > 2:
            create_manager = False


        if request.method == 'POST':
            if request.POST.get('suspend-btn'):
                username  = request.POST.get('username')
                try:
                    user = User.objects.get(username=username)
                    if user.is_active:
                        user.is_active = False
                    else:
                        user.is_active = True
                    user.save()
                except User.DoesNotExist:
                    pass

            else:
                group_form = GroupForm(data=request.POST)
                if group_form.is_valid():
                    group = group_form.save()
                    group.save()

        context_dict = {'users': user_list, 'group_form': group_form, 'groups': group_list, 'create_manager': create_manager}

        return render(request, 'manager.html', context_dict)


    else:
        #Deploy SWAT if a non-admin tries to access the page
        return HttpResponse("A SWAT team is on the way")

def user_to_group(request):
    if request.method == 'POST':
            if request.POST.get('user-group-btn'):
                username  = request.POST.get('username')
                group_name = request.POST.get('group-name')
                try:
                    group = Group.objects.get(name=group_name)
                    group.user_set.add(User.objects.get(username=username))
                    group.save()
                except Group.DoesNotExist:
                    pass
    return HttpResponseRedirect('/myapplication/manager')

def group_to_report(request):
    if request.method == 'POST':
            if request.POST.get('report-group-btn'):
                group_name = request.POST.get('group-name')
                try:
                    r = Report.objects.get(id=request.POST.get('reportid'))
                    potentialgroup= Group.objects.get(name=group_name)
                    r.groups.add(potentialgroup)
                    r.save()
                except Group.DoesNotExist:
                    pass
    return HttpResponseRedirect('/myapplication/reports')

def user_to_report(request):
    if request.method == 'POST':
            if request.POST.get('report-user-btn'):
                user_name = request.POST.get('user-name')
                try:
                    r = Report.objects.get(id=request.POST.get('reportid'))
                    potentialuser = User.objects.get(username=user_name)
                    r.users.add(potentialuser)
                    r.save()
                except User.DoesNotExist:
                    pass
    return HttpResponseRedirect('/myapplication/reports')

def new_report(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            if request.POST.get('description'):
                report = Report(author=request.user)
                if request.POST.get('encrypted'):
                    report.encrypted = request.POST.get('encrypted')
                else:
                    report.encrypted = False
                if request.POST.get('security'):
                    report.security = request.POST.get('security')
                else:
                    report.security = False
                report.content = request.POST.get('content')
                report.description = request.POST.get('description')
                report.save()
                for count, x in enumerate(request.FILES.getlist("files")):
                    report_file = ReportFile(reporter=report, file=x)
                    report_file.save()
        return render(request, 'makereport.html')
    else:
        return HttpResponse("You must be logged in to submit a report")


def edit_report(request):
    if request.user.is_authenticated():
        if request.POST.get('reportID'):
            r = Report.objects.get(id=request.POST.get('reportID'))
            files = ReportFile.objects.filter(reporter=r)
            context_dict = {'report' : r, 'files' : files}
            return render(request, 'editreport.html', context_dict)
        if request.method == 'POST':
            if request.POST.get('idme'):
                rep = Report.objects.get(id=request.POST.get('idme'))
                rep.encrypted = False
                rep.security = False
                if request.POST.get('encrypted'):
                    rep.encrypted = request.POST.get('encrypted')
                if request.POST.get('security'):
                    rep.security = request.POST.get('security')
                rep.content = request.POST.get('content')
                rep.description = request.POST.get('description')
                rep.save()
                for count, x in enumerate(request.FILES.getlist("files")):
                    report_file = ReportFile(reporter=rep, file=x)
                    report_file.save()
                    with open(settings.MEDIA_ROOT + x.name, 'wb+') as destination:
                        for chunk in x.chunks():
                            destination.write(chunk)
            return render(request, 'editreport.html')

    else:
       return HttpResponse("You should not be here")

def view_report(request):
    if request.user.is_authenticated():
        if request.POST.get('reportID'):
            if request.POST.get('report-user-btn'):
                user_name = request.POST.get('user-name')
                try:
                    r = Report.objects.get(id=request.POST.get('reportID'))
                    potentialuser = User.objects.get(username=user_name)
                    r.users.add(potentialuser)
                    r.save()
                except User.DoesNotExist:
                    pass
            if request.POST.get('report-group-btn'):
                group_name = request.POST.get('group-name')
                try:
                    r = Report.objects.get(id=request.POST.get('reportID'))
                    potentialgroup= Group.objects.get(name=group_name)
                    r.groups.add(potentialgroup)
                    r.save()
                except Group.DoesNotExist:
                    pass
            if request.POST.get('deletefile-btn'):
                try:
                    rf =ReportFile.objects.get(id=request.POST.get('fileID')).delete()
                except ReportFile.DoesNotExist:
                    pass
            r = Report.objects.get(id=request.POST.get('reportID'))
            files = ReportFile.objects.filter(reporter=r)
            viewer = request.user
            x= r.views
            r.views= x + 1
            r.save()
            context_dict = {'report' : r, 'files' : files, 'viewer' : viewer}
            return render(request, 'viewreport.html', context_dict)
        return render(request, 'viewreport.html')
    else:
        return HttpResponse("You should not be here")


def new_folder(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            folder_form = ReportFolderForm(data=request.POST)
            if folder_form.is_valid():
                f = folder_form.save()
                f.owner = request.user
                f.save()
            context_dict = {'folder_form' : folder_form}
            return render(request, 'makefolder.html', context_dict)
        return render(request, 'makefolder.html')
    else:
        return HttpResponse("You should not be here")

def edit_folder(request):
    if request.POST.get('folderID'):
        userreports = Report.objects.filter(author_id=request.user.id)
        folder = ReportFolder.objects.get(id=request.POST.get('folderID'))
        context_dict = {'reports' : userreports, 'folder' : folder}
        if request.POST.get('reportID'):
            folder.reports.add(Report.objects.get(id=request.POST.get('reportID')))
        return render(request, 'addtofolder.html', context_dict)
    else:
        return HttpResponse("You should not be here")

def delete_folder(request):
    if request.POST.get('folderID'):
        try:
            ReportFolder.objects.get(id=request.POST.get('folderID')).delete()
        except: ReportFolder.DoesNotExist
        return render(request, 'reports.html')
    else:
        return HttpResponse("You should not be here")


def view_folder(request):
    if request.POST.get('folderID'):
        folder = ReportFolder.objects.get(id=request.POST.get('folderID'))
        folderreports = folder.reports.all()
        context_dict = {'reports' : folderreports, 'folder' : folder}
        return render(request, 'viewfolder.html', context_dict)
    else:
        return HttpResponse("You should not be here")

def make_manager(request):
    if request.method == 'POST':
        manager_list = User.objects.filter(is_staff=True)
        num_managers = len(manager_list)

        if request.POST.get('manager-btn'):
            username  = request.POST.get('username')
            try:
               user = User.objects.get(username=username)
               if user.is_staff:
                   user.is_staff = False
               elif num_managers < 3:
                   user.is_staff = True
               user.save()

            except User.DoesNotExist:
                pass
    return HttpResponseRedirect('/myapplication/manager')


def messaging(request):

    try:
        Messages = Message.objects.filter(recipient=request.user.username)
    except:
         Messages = []
    Users = User.objects.all()
    for m in Messages:
        m.viewed=True
        m.save()
    context_dict = {'messages' : Messages, 'users' :Users, 'NError': False, 'SError':False}




    if request.method == 'POST':
        if request.POST.get('submit'):

            form = SendMessage(data=request.POST)

            if form.is_valid():
                send_message = form.save(commit=False)
                send_message.sender = request.user.username
                if len(User.objects.filter(username=send_message.recipient)) == 0:
                    context_dict['NError'] =True
                    print("invalid recipient")
                    pass
                else:
                    if send_message.encrypted:
                        #print("fetching " + send_message.recipient + "'s public key")
                        keys = PublicKey.objects.filter(user=send_message.recipient)
                        if len(keys) ==0:
                            context_dict['SError']=True
                            print("Recipient's public key not set")
                            send_message.encrypted=False
                        else:
                            pubkey = keys[0]
                            #print("constructing key")
                            public = RSA.construct((int(pubkey.Nval),int(pubkey.Eval)))
                            #print("encrypting message")
                            result = public.encrypt(str.encode(send_message.message),32)
                            send_message.message="this is encrypted"
                            send_message.bites=result[0]
                            send_message.save()
                            #print("message encrypted")
                    else:
                        send_message.save()



            else:
                print(form.errors)
        if request.POST.get('delete-message'):


            id = request.POST.get('id')

            try:
                dump = Message.objects.get(id=id)
                dump.delete()
            except:
                print("delete failed")

        if request.POST.get('decrypt-message'):


            Dval = int(request.POST.get('Dval'))
            id = request.POST.get('id')
            message = Message.objects.get(id=id)
            Pubkey = PublicKey.objects.filter(user=request.user.username)[0]
            Nval = int(Pubkey.Nval)
            Eval = int(Pubkey.Eval)
            print("constructing Key")
            private = RSA.construct((Nval,Eval,Dval))
            print("key constructed, decrypting")
            bites = message.bites
            message.message = private.decrypt(bites)
            print("message decrypted")
            message.encrypted= False
            message.bites=None
            message.save()




        if request.POST.get('SetKey'):
            nValue = request.POST.get('Nval')
            eValue = request.POST.get('Eval')
            nValueI = int(nValue)
            eValueI = int(eValue)
            try:
                RSA.construct((nValueI,eValueI))
                print("RSA checked, making form")


                if len(list(PublicKey.objects.filter(user = request.user.username).all())) ==0:
                    public2 = PublicKey(user=request.user.username, Nval=nValue, Eval = eValue)
                else:
                    public2 = PublicKey.objects.filter(user=request.user.username)[0]
                #public = form.save(commit=False)
                # public2.user=request.user.username
                # public2.Nval=nValue
                # public2.Eval=eValue
                print("saving...")
                public2.save()
                print("key saved")
            except Exception as e:
                print(e)
                print("Key failed")
    return render(request, 'messaging.html', context_dict)


def reports(request):
    report_list = Report.objects.filter(Q(security=False) | Q(users=request.user) | Q(groups=request.user.groups.all())).order_by('views')
    if request.user.is_staff:
        report_list=Report.objects.all()
    folder_list = ReportFolder.objects.filter(owner_id=request.user.id)
    params = []
    if request.method == 'POST':
        if request.POST.get('delete-btn'):
            reportid = request.POST.get('reportID')
            try:
                Report.objects.get(id=reportid).delete()
            except Report.DoesNotExist:
                pass
    if request.method == 'POST':
        items = request.POST
        for item in items:
            if "cat" in item:
                num = item[3:]
                param = {"cat" : request.POST.get("cat" + str(num)),
                         "con" : request.POST.get("con" + str(num)),
                         "val" : request.POST.get("val" + str(num))}
                params.append(param)
    new_list = []
    exclude = []
    for param in params:
        con = param["con"]
        cat = param["cat"]
        val = param["val"]
        if val == "":
            continue
        if con == 'AND':
            if cat == "Description":
                for report in report_list:
                    if str(report.description) != str(val):
                        exclude.append(str(report.author) + str(report.date))
            elif cat == "Created After":
                date_object = datetime.strptime(val, '%b %d %Y')
                for report in report_list:
                    if report.date.date() <= date_object.date():
                        exclude.append(str(report.author) + str(report.date))
            elif cat == "Created Before":
                date_object = datetime.strptime(val, '%b %d %Y')
                for report in report_list:
                    if report.date.date() >= date_object.date():
                        exclude.append(str(report.author) + str(report.date))
            elif cat == "Created On":
                date_object = datetime.strptime(val, '%b %d %Y')
                for report in report_list:
                    if report.date.date() != date_object.date():
                        exclude.append(str(report.author) + str(report.date))
            else:
                for report in report_list:
                    if str(report.author) != str(val):
                        exclude.append(str(report.author) + str(report.date))
        else:
            continue
    for param in params:
        con = param["con"]
        cat = param["cat"]
        val = param["val"]
        if val == "":
            continue
        if con == 'OR':
            if cat == "Description":
                for report in report_list:
                    if str(report.description) == str(val):
                        if str(report.author) + str(report.date) in exclude:
                            exclude.remove(str(report.author) + str(report.date))
            elif cat == "Created After":
                date_object = datetime.strptime(val, '%b %d %Y')
                for report in report_list:
                    if report.date.date() > date_object.date():
                        if str(report.author) + str(report.date) in exclude:
                            exclude.remove(str(report.author) + str(report.date))
            elif cat == "Created Before":
                date_object = datetime.strptime(val, '%b %d %Y')
                for report in report_list:
                    if report.date.date() < date_object.date():
                        if str(report.author) + str(report.date) in exclude:
                            exclude.remove(str(report.author) + str(report.date))
            elif cat == "Created On":
                date_object = datetime.strptime(val, '%b %d %Y')
                for report in report_list:
                    if report.date.date() == date_object.date():
                        if str(report.author) + str(report.date) in exclude:
                            exclude.remove(str(report.author) + str(report.date))
            else:
                for report in report_list:
                    if str(report.author) == str(val):
                        if (str(report.author) + str(report.date)) in exclude:
                            exclude.remove(str(report.author) + str(report.date))
        else:
            continue
    for report in report_list:
        if str(report.author) + str(report.date) not in exclude:
            new_list.append(report)

    context_dict = {"Reports": new_list, "Folders": folder_list}

    return render(request, 'reports.html', context_dict)


def fda_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                data = {'success': True}
            else:
                data = {'success': False, 'error': 'User is not active'}

        else:
            data = {'success': False, 'error': 'Wrong username and/or password'}

        return HttpResponse(json.dumps(data), content_type='application/json')

    return HttpResponseBadRequest()


def fda_list_reports(request):
    if request.user.is_authenticated():
        report_list = Report.objects.all()
        reports = {'num': [], 'Description': [], 'Author': [], 'Date': [], 'Encrypted': [], 'Content': [], 'ID': []}
        num = 0
        for report in report_list:
            num+=1
            reports['num'].append(num)
            reports['Description'].append(report.description)
            reports['Author'].append(report.author.username)
            reports['Date'].append(str(report.date)[:11])
            reports['Encrypted'].append(report.encrypted)
            reports['Content'].append(report.content)
            reports['ID'].append(report.id)
        data = {'success': True, 'reports': reports}
    else:
        data = {'success': False, 'error': 'User not authenticated'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def fda_get_report(request):
    if request.user.is_authenticated():
        report = Report.objects.get(id=request.GET.get('reportID'))
        files = ReportFile.objects.filter(reporter=report)
        r = {
            'Description': report.description,
            'Author': report.author.username,
            'Date': str(report.date),
            'Encrypted': report.encrypted,
            'Content': report.content,
            'ID': report.id
        }
        if files:
            f = []
            for file in files:
                file_info = {
                    'name': file.file.name,
                    'url': file.file.url
                }
                f.append(file_info)
            data = {'report' : r, 'files' : f}
        else:
            data = {'report' : r}
        return HttpResponse(json.dumps(data), content_type='application/json')


def groups(request):
    group_list  =request.user.groups.all()
    context_dict = {'groups': group_list}
    return render(request, 'groups.html', context_dict)