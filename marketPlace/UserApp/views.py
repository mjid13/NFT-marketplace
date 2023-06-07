from django.shortcuts import render, redirect
from django.contrib import messages


from Contracts.CustmerAuthDEPLOY import Deploy
from OrgnzApp.views import ticket_hub
from Contracts.TicketMarketplaceDEPLOY import TicketFunctions
from django.urls import reverse


from web3 import Web3

contract = Deploy()




def login1(request):
    print('I got request ..')
    if request.method == 'GET':
        print('Its GET ..')
        return render(request, 'login1.html', {})
    if request.method == 'POST':
        print('Its POST ..')

        address = request.POST['address']
        password = request.POST['password']
        isRegister = contract.isRegister(address)
        if isRegister:
            print(' I cheked  if register')
            contract.login(address=address, password=password)
            isLogin = contract.isLogin(address)
            if isLogin:
                print(' I cheked  if login')
                request.session['address'] = address
                messages.success(request, 'Account was login for ' + address)
                return redirect('/profile/')

            else:
                messages.error(request, 'There is an a error in your request!')
                return render(request, 'login1.html', {})
        else:
            messages.error(request, 'User Address is not Register!')
            return render(request, 'login1.html', {})
    else:
        return render(request, 'login1.html', {})




def userRegister(request):
    if request.method == 'GET':
        return render(request, 'userRegister.html', {})

    if request.method == 'POST':
        name = request.POST['name']
        password = request.POST['email']
        phone = request.POST['phone']
        email = request.POST['password']
        address = request.POST['address']
        if contract.isRegister(address) == False:

            contract.customer_register(address=address, name=name, phone=str(phone),
                                       password=password, email=email,
                                       )
            messages.success(request, 'You Successful Registered')

            return render(request, 'custSuccessful.html', {})

        else:
            messages.error(request, 'Account Address Already Registered!')
            return render(request, 'userRegister.html', {})
    else:
        return render(request, 'userRegister.html', {})


def changeProfile(request):
    if request.method == 'GET':
        return render(request, 'changeProfile.html', {})

    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        address = request.session['address']
        contract.changeUserProfile(address=address, name=name, phone=str(phone), email=email,
                                   )
        return redirect(reverse('UserApp:profile'))

    else:
        return render(request, 'changeProfile.html', {})

def changePass(request):
    if request.method == 'GET':
        return render(request, 'changePass.html', {})

    if request.method == 'POST':
        password = request.POST['password']
        address = request.session['address']
        contract.changeUserPassword(address=address, password=password)
        return redirect(reverse('UserApp:profile'))

    else:
        return render(request, 'changePass.html', {})



def profile(request):

    if 'address' in request.session:
        address = request.session['address']
        details = contract.getUser(address=address)
        name = details['name']
        email = details['email']
        phone = details['phone']
        isLogin = True
        context = {
            'name': name,
            'email': email,
            'phone': phone,
            'isLogin': isLogin
        }
    else:
        context = {
            'empty': []
        }
    return render(request, 'profile.html', context)



def logout(request):
    address = request.session['address']
    contract.logout(address=address)
    del request.session['address']

    context = {

    }
    return render(request, 'index.html', context)



def custSuccessful(request):
    context = {

    }
    return render(request, 'custSuccessful.html', context)


def myTicket(request):
    if 'address' in request.session:
        address = request.session['address']
        isLogin = True
    else:
        isLogin = False
        address = ' '

    totalTickets = ticket_hub.getAllTickets()
    ownedT = {}
    for i in totalTickets:
        ownedTick = ticket_hub.getOwnedNFTs(address=address, ticketsList=i)
        ticket_functions = TicketFunctions(i)
        ticket_detail = ticket_functions.getTicketDetail()
        ticket_detail.append(ownedTick)
        ownedT[i]= ticket_detail

    if request.method == "POST":
        if "notseal" in request.POST:
            Tid = request.POST["Tid"]
            Taddress = request.POST["Tickaddress"]
            ticket_functions = TicketFunctions(Taddress)
            ticket_functions.cancelSale(address, Tid)
        else:
            Tid = request.POST["Tid"]
            Taddress = request.POST["Tickaddress"]
            price = request.POST["price"]
            ticket_functions = TicketFunctions(Taddress)
            ticket_functions.setTicketForSale(address, Tid, price)





    context = {
            'isLogin': isLogin,
            'ownedT':ownedT

    }
    return render(request, 'myTicket.html', context)


def saleTicket(request):
    if 'address' in request.session:
        address = request.session['address']
        isLogin = True
    else:
        isLogin = False
        address = ' '

    totalTickets = ticket_hub.getAllTickets()
    ownedT = {}
    for i in totalTickets:
        ownedTick = ticket_hub.getOwnedNFTs(address=address, ticketsList=i)
        ticket_functions = TicketFunctions(i)
        ticket_detail = ticket_functions.getTicketDetail()
        ticket_detail.append(ownedTick)
        ownedT[i]= ticket_detail

    print(ownedT)


    context = {
            'isLogin': isLogin,
            'ownedT':ownedT

    }
    return render(request, 'myTicket.html', context)
