from OrgnzApp.views import contract as OrgAutcontract, ticket_hub
from Contracts.TicketMarketplaceDEPLOY import TicketFunctions
from UserApp.views import contract as UserAuthcontract
from Contracts.adminControlDEPLOY import Deploy
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
# from .deboly import Contract


from web3 import Web3

w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))


contract = Deploy()


contract.deployOrg()


def index(request):

    if 'address' in request.session:
        isLogin = True
    else:
        isLogin = False
    if 'ORGN' in request.session:
        isORN = True
    else:
        isORN = False



    context = {
        'isLogin': isLogin,
        'isORN': isORN,

    }

    return render(request, 'index.html', context)


contract.admin_register(
    '0xf08b7c68D244f0E7959c56Eb043E31102235bc75', 'ali', '12345')


def registerType(request):

    if 'address' in request.session:
        isLogin = True
    else:
        isLogin = False
    if 'ORGN' in request.session:
        isORN = True
    else:
        isORN = False

    context = {
        'isLogin': isLogin,
        'isORN': isORN,

    }

    return render(request, 'registerType.html', context)


def about(request):
    if 'address' in request.session:
        isLogin = True
    else:
        isLogin = False
    if 'ORGN' in request.session:
        isORN = True
    else:
        isORN = False

    context = {
        'isLogin': isLogin,
        'isORN': isORN,

    }

    return render(request, 'about.html', context)

def doneBuy(request):
    if 'address' in request.session:
        isLogin = True
    else:
        isLogin = False
    if 'ORGN' in request.session:
        isORN = True
    else:
        isORN = False

    context = {
        'isLogin': isLogin,
        'isORN': isORN,

    }

    return render(request, 'doneBuy.html', context)


def activity(request):
    if 'address' in request.session:
        isLogin = True
    else:
        isLogin = False
    if 'ORGN' in request.session:
        isORN = True
    else:
        isORN = False

    context = {
        'isLogin': isLogin,
        'isORN': isORN,

    }

    return render(request, 'activity.html', context)


def help(request):
    if 'address' in request.session:
        isLogin = True
    else:
        isLogin = False
    if 'ORGN' in request.session:
        isORN = True
    else:
        isORN = False

    context = {
        'isLogin': isLogin,
        'isORN': isORN,

    }

    return render(request, 'help.html', context)


def singleTicket(request):
    if 'address' in request.session:
        isLogin = True
    else:
        isLogin = False
    if 'ORGN' in request.session:
        isORN = True
    else:
        isORN = False

    context = {
        'isLogin': isLogin,
        'isORN': isORN,

    }

    return render(request, 'singleTicket.html', context)

def search(request):
    isLogin = True if 'address' in request.session else False
    isORN = True if 'ORGN' in request.session else False
    all_tickets = ticket_hub.getAllTickets()
    ticket_output = {}
    if "ticketName" in request.GET:
        print("hi from request ", request.GET["ticketName"])
        for ticket in all_tickets:
            ticket_fun = TicketFunctions(ticket)
            ticket_details = ticket_fun.getTicketDetail()
            if request.GET["ticketName"] in ticket_details:
                ticket_details.append(ticket)
                ticket_output[ticket] = ticket_details

    context = {
            'isLogin': isLogin,
            'isORN': isORN,
            'ticket_output': ticket_output
    }
    return render(request, "search.html", context)


def collectionTicket(request):
    isLogin = True if 'address' in request.session else False
    isORN = True if 'ORGN' in request.session else False
    if 'Tickaddress' in request.session:
        ticket_address = request.session['Tickaddress']
        #del request.session['Tickaddress']
        ticket_to_show = TicketFunctions(ticket_address)
        number_of_tickets = ticket_to_show.getTotalTickets()
        ticket_details = ticket_to_show.getTicketDetail()
        #print(ticket_details)
        list_of_tickets = []
        second_sale = {}
        is_sec_seal = False
        print(number_of_tickets)

        for i in range(1, 1+number_of_tickets):
            second_sale_chake = ticket_to_show.getSecTicketDetail(i)

            print(type(second_sale_chake[5]))
            print(second_sale_chake)
            if ticket_to_show.chackOwner(i):
                list_of_tickets.append(i)

            print(list_of_tickets)
            if second_sale_chake[5] and not ticket_to_show.chackOwner(i):
                print("hi from in saied")
                is_sec_seal = True
                second_sale[1] = second_sale_chake




        if request.method == "POST":
            address = request.session['address']
            ticket_id = request.POST['id']
            ticket_to_show.buyTicket(_address=address, tokenId=int(ticket_id), _ticketPrice=int(ticket_details[3]))
            print("##### DONE #####")
            return redirect(reverse('AdminApp:doneBuy'))





        #print(list_of_tickets)
        context = {
                'ticket_address':ticket_address,
                'list_of_tickets': list_of_tickets,
                'ticket_details': ticket_details,
                'second_sale': second_sale,
                'isLogin': isLogin,
                'isORN': isORN,
                'is_sec_seal': is_sec_seal
        }


    else:
        context = {
                'isLogin': isLogin,
                'isORN': isORN,

        }




    return render(request, 'collection.html', context)


def contatct(request):
    if 'address' in request.session:
        isLogin = True
    else:
        isLogin = False
    if 'ORGN' in request.session:
        isORN = True
    else:
        isORN = False

    context = {
        'isLogin': isLogin,
        'isORN': isORN,

    }

    return render(request, 'contatct.html', context)


def mart(request):
    totalTickets = ticket_hub.getAllTickets()
    ticket_detl ={}
    for i in totalTickets:

        ticket_functions = TicketFunctions(i)
        num_tik = ticket_functions.getTotalTickets()
        ticket = list(ticket_functions.getTicketDetail())
        ticket.append(str(num_tik))

        ticket_detl[i] = ticket

        #print(ticket_detl)

    if request.method == 'POST':
        request.session['Tickaddress'] = request.POST['Tickaddress']
        return redirect(reverse('AdminApp:collectionTicket'))




    if 'address' in request.session:
        isLogin = True
    else:
        isLogin = False
    if 'ORGN' in request.session:
        isORN = True
    else:
        isORN = False

    context = {
        'isLogin': isLogin,
        'isORN': isORN,
        'ticket_detl': ticket_detl,

    }

    return render(request, 'brows.html', context)


def adminLogin(request):
    if request.method == 'GET':
        return render(request, 'adminlogin.html', {})
    if request.method == 'POST':

        address = request.POST['address']
        password = request.POST['password']
        isRegister = contract.isRegister(address)
        #print('hi from login ', isRegister)
        if isRegister:
            contract.login(address=address, password=password)
            isLogin = contract.isLogin(address)
            if isLogin:
                #print('hi from login ')
                request.session['address'] = address
                messages.success(request, 'Account was login for ' + address)
                return redirect('/adminpage/')

            else:
                messages.error(request, 'There is an a error in your request!')
                return render(request, 'adminlogin.html', {})
        else:
            messages.error(request, 'User Address is not Register!')
            return render(request, 'adminlogin.html', {})
    else:
        return render(request, 'adminlogin.html', {})


def logout(request):
    address = request.session['address']
    contract.logout(address=address)
    del request.session['address']
    context = {

    }
    return render(request, 'adminlogin.html', context)


def adminPage(request):

    if 'address' in request.session:
        isLogin = True
    else:
        isLogin = False

    context = {
        'isLogin': isLogin,

    }
    return render(request, 'adminPage.html', context)


def adminPageUser(request):
    addresses = UserAuthcontract.getAllUserAddresses()
    user_detail = {}

    for address in addresses:
        user_detail[address] = UserAuthcontract.getUser(address)

    if 'address' in request.session:
        isLogin = True
    else:
        isLogin = False

    context = {
        'isLogin': isLogin,
        'user_detail': user_detail,

    }
    return render(request, 'adminPageUser.html', context)


def adminPageOrg(request):
    if request.method == 'GET':
        pass

    if request.method == 'POST':
        address = request.POST['address']
        if 'confirm' in request.POST:
            OrgAutcontract.changeUserValidation(address)

        elif 'delete' in request.POST:
            OrgAutcontract.removeOrganizer(address)

    addresses = OrgAutcontract.getAllUserAddresses()
    user_detail = {}
    user_valid = ''

    #for address in addresses:
    #    user_valid = 'VALID' if OrgAutcontract.checkIsUserValid(address) else 'NOT VALID'
    #    orgdic = OrgAutcontract.getUser(address)
    #    orgdic['validity'] = user_valid

    #    user_detail[address] = orgdic




    for address in addresses:
        if OrgAutcontract.checkIsUserValid(address):
            user_valid = 'VALID'
        else:
            user_valid = 'NOT VALID'
        t = OrgAutcontract.getUser(address)
        user_detail[address] = OrgAutcontract.getUser(address)
    #print(t)
    #print(user_detail)

    if 'address' in request.session:
        isLogin = True
    else:
        isLogin = False

    context = {
        'isLogin': isLogin,
        'user_detail': user_detail,
        'user_valid': user_valid

    }
    return render(request, 'adminPageOrg.html', context)
