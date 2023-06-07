from django.shortcuts import render, redirect
from django.contrib import messages
# from .deboly import Contract

from web3 import Web3

from Contracts.OrgAuthDEPLOY import Deploy
from Contracts.TicketMarketplaceDEPLOY import Deploy as ticket_deploy, TicketFunctions
from Contracts.NFTRegistryDEPLOY import Deploy as hub_deploy
from django.urls import reverse


contract = Deploy()
ticket_hub = hub_deploy()
ticket_hub.deployNftRegistry()
# contract.deployOrg()
# ticket_contract = ticket_contract


# ticket_contract.deploy_nft('hi', 'HI', 'URl')


def login1(request):
    if request.method == 'GET':
        return render(request, 'login.html', {})
    if request.method == 'POST':

        address = request.POST['address']
        password = request.POST['password']
        isRegister = contract.isRegister(address)
        #print('hi from login ', isRegister)
        if isRegister:
            contract.login(address=address, password=password)
            isLogin = contract.isLogin(address)
            isValid = contract.checkIsUserValid(address)
            if isValid:
                if isLogin:
                    #print('hi from login ')
                    request.session['address'] = address
                    request.session['ORGN'] = address
                    messages.success(
                        request, 'Account was login for ' + address)
                    return redirect('/Orgprofile/')

                else:
                    messages.error(
                        request, 'There is an a error in your request!')
                    return render(request, 'login.html', {})
            else:
                messages.error(request,
                               'Sorry, You are not Valid to login as organizer yet!\n please wait for ADMIN to Confirm your account details ')
                return render(request, 'login.html', {})
        else:
            messages.error(request, 'User Address is not Register!')
            return render(request, 'login.html', {})
    else:
        return render(request, 'login.html', {})


def orgRegister(request):
    if request.method == 'GET':
        return render(request, 'orgRegister.html', {})

    if request.method == 'POST':
        name = request.POST['name']
        password = request.POST['email']
        phone = request.POST['phone']
        email = request.POST['password']
        address = request.POST['address']
        if contract.isRegister(address) == False:

            contract.organizer_register(address=address, name=name, phone=str(phone),
                                        password=password, email=email,
                                        )
            messages.success(request, 'You Successful Registered')

            return render(request, 'orgSuccessful.html', {})

        else:
            messages.error(request, 'Account Address Already Registered!')
            return render(request, 'orgRegister.html', {})
    else:
        return render(request, 'orgRegister.html', {})



def changeProfile(request):
    if request.method == 'GET':
        return render(request, 'OrgchangeProfile.html', {})

    if request.method == 'POST':
        print("This is the post: ",request.POST)
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        address = request.session['address']
        contract.changeUserProfile(address=address, name=name, phone=str(phone), email=email,
                                   )
        return redirect(reverse('OrgnzApp:profile'))

    else:
        return render(request, 'OrgchangeProfile.html', {})

def changePass(request):


    if request.method == 'POST':
        password = request.POST['password']
        address = request.session['address']
        contract.changeUserPassword(address=address, password=password)
        return redirect(reverse('OrgnzApp:profile'))

    else:
        return render(request, 'OrgchangePass.html', {})



def profile(request):
    if 'ORGN' in request.session:
        isORN = True
    else:
        isORN = False

    if 'address' in request.session:
        address = request.session['address']
        details = contract.getUser(address=address)
        #print(details)
        name = details['name']
        email = details['email']
        phone = details['phone']
        isLogin = True
        context = {
            'name': name,
            'email': email,
            'phone': phone,
            'isLogin': isLogin,
            'isORN': isORN,
        }
    else:
        context = {
            'empty': []
        }
    return render(request, 'Oprofile.html', context)


def logout(request):
    address = request.session['address']
    contract.logout(address=address)
    del request.session['address']
    del request.session['ORGN']
    context = {

    }
    return render(request, 'index.html', context)


def orgSuccessful(request):
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
    return render(request, 'orgSuccessful.html', context)

def burnSuccessful(request):
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
    return render(request, 'burnSuccessful.html', context)

def burnfaild(request):
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
    return render(request, 'burnfaild.html', context)


def burn(request):
    if 'address' in request.session:
        isLogin = True
    else:
        isLogin = False
    if 'ORGN' in request.session:
        isORN = True
    else:
        isORN = False


    if 'Tickaddress' in request.session:
        ticket_address = request.session['Tickaddress']
        ticket_to_show = TicketFunctions(ticket_address)
        if request.method == 'POST':
            try:
                address = request.session['address']
                ticket_id = request.POST['id']
                ticket_to_show.burn(
                        address=address, TOKEN_ID=int(ticket_id))
                print(f"you Burn the Ticket ^^🔥🔥🔥 {ticket_id}")
                return redirect(reverse('OrgnzApp:burnSuccessful'))
            except:
                return redirect(reverse('OrgnzApp:burnfaild'))





    context = {
        'isLogin': isLogin,
        'isORN': isORN,

    }
    return render(request, 'burn.html', context)


def burnList(request):
    if 'address' in request.session:
        isLogin = True
        address = request.session['address']
    else:
        isLogin = False
        address = ' '
    if 'ORGN' in request.session:
        isORN = True
    else:
        isORN = False

    all_tickets = ticket_hub.getOrganizerNFT(address=address)
    ownedT = {}
    for i in all_tickets:
        ticket_funcation = TicketFunctions(i)
        ticket_ditails = ticket_funcation.getTicketDetail()
        ownedT[i] = ticket_ditails

    if request.method == 'POST':
        request.session['Tickaddress'] = request.POST['Tickaddress']
        return redirect(reverse('OrgnzApp:burn'))

    context = {
            'isLogin': isLogin,
            'isORN': isORN,
            'ownedT': ownedT

    }


    return render(request, 'burnList.html', context)


def showticket(request):
    if 'address' in request.session:
        isLogin = True
        address = request.session['address']
    else:
        isLogin = False
        address = ' '
    if 'ORGN' in request.session:
        isORN = True
    else:
        isORN = False

    all_tickets = ticket_hub.getOrganizerNFT(address=address)
    ownedT = {}
    for i in all_tickets:
        ticket_funcation = TicketFunctions(i)
        ticket_ditails = ticket_funcation.getTicketDetail()
        ownedT[i]= ticket_ditails





    context = {
        'isLogin': isLogin,
        'isORN': isORN,
        'ownedT': ownedT

    }
    return render(request, 'showTickets.html', context)


def sold(request):
    if 'address' in request.session:
        address = request.session['address']
        isLogin = True
    else:
        isLogin = False
        address = ' '
    if 'ORGN' in request.session:
        isORN = True
    else:
        isORN = False


    totalTickets = ticket_hub.getAllTickets()
    sold = {}
    sold_cunt = []
    for i in totalTickets:
        ownedTick = ticket_hub.getOwnedNFTs(address=address, ticketsList=i)
        ticket_functions = TicketFunctions(i)
        total_ids= ticket_functions.getTotalTickets()
        for j in range(1, total_ids+1):
            if j not in ownedTick:
                sold_cunt.append(j)

        ticket_detail = ticket_functions.getTicketDetail()
        ticket_detail.append(sold_cunt)
        sold[i]= ticket_detail
        print(sold)

    context = {
        'isLogin': isLogin,
        'isORN': isORN,
        'sold': sold

    }
    return render(request, 'sold.html', context)


def notSold(request):
    if 'address' in request.session:
        address = request.session['address']
        isLogin = True
    else:
        isLogin = False
        address = ' '
    if 'ORGN' in request.session:
        isORN = True
    else:
        isORN = False

    totalTickets = ticket_hub.getAllTickets()
    ownedT = {}
    for i in totalTickets:
        ownedTick = ticket_hub.getOwnedNFTs(address=address, ticketsList=i)
        ticket_functions = TicketFunctions(i)
        ticket_detail = ticket_functions.getTicketDetail()
        ticket_detail.append(ownedTick)
        ownedT[i] = ticket_detail

    context = {
            'isLogin': isLogin,
            'isORN': isORN,
            'ownedT': ownedT

    }
    return render(request, 'notSold.html', context)


def createNFT(request):
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

    if 'address' in request.session:
        address = request.session['address']
    if request.method == 'POST':
        ticketNum = request.POST['ticketNum']
        name = request.POST['name']
        description = request.POST['description']
        imageURL = request.POST['imgUrl']
        price = request.POST['price']
        royalty = request.POST['royalty']
        isOnSale = True
        eventDate = request.POST.get('date')
        eventTime = request.POST.get('time')
        ticketClass = request.POST['type']
        #print('DATE  : ', eventDate)
        #print(eventTime)
        ticket_contract = ticket_deploy(
            _NAME=name, _BASETOKENURI=imageURL, _address=address)

        ticket_contract.createTicket(ticketNum=int(ticketNum),
                                     name=name,
                                     description=description,
                                     imageURL=imageURL,
                                     price=int(price),
                                     royalty=int(royalty),
                                     isOnSale=isOnSale,
                                     eventDate=str(eventDate),
                                     eventTime=str(eventTime),
                                     ticketClass=ticketClass)

        ticket_hub.createUserNFT(
            address=address, nftAddress=ticket_contract.contract_address)
        return render(request, 'createSuccessful.html', context)



    return render(request, 'createNFT.html', context)
