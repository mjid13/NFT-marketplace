import marshal
import json
from solcx import compile_source, install_solc
from web3 import Web3
from .accounts import privateKey


class Deploy:
    def __init__(self, _NAME, _BASETOKENURI, _address):
        with open(f"C:/Users/X/Desktop/BetcProj/marketPlace/Contracts/TicketMarketplaceABI.json", "r") as file:
            self.abi = file.read()

        with open(f"C:/Users/X/Desktop/BetcProj/marketPlace/Contracts/TicketMarketplaceBYTE.txt", "r") as file:
            self.bytecode = file.read()

        # compiled_sol = compile_source(solidity_source)
        # print(compiled_sol)

        # self.bytecode = compiled_sol[f'<stdin>:TicketMarketplace']['bin']
        # self.abi = compiled_sol[f'<stdin>:TicketMarketplace']['abi']

        self.w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

        self.mainAddress = _address

        self.w3.eth.default_account = self.mainAddress

        self.contract1 = self.w3.eth.contract(
            abi=self.abi, bytecode=self.bytecode)

        tx_hash = self.contract1.constructor(
            _NAME, "ETH", _BASETOKENURI).transact()
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        self.contract_address = tx_receipt.contractAddress
        #print(self.contract_address)

        self.contract = self.w3.eth.contract(
            address=self.contract_address, abi=self.abi)

    def contract_address(self):
        ca = self.contract_address
        return ca

    def createTicket(self,
                     ticketNum,
                     name,
                     description,
                     imageURL,
                     price,
                     royalty,
                     isOnSale,
                     eventDate,
                     eventTime,
                     ticketClass):
        # Get the latest transaction count
        nonce = self.w3.eth.getTransactionCount(self.mainAddress)

        # Submit the transaction to call the `createTicket` function
        result = self.contract.functions.createTicket(ticketNum,
                                                      name,
                                                      description,
                                                      imageURL,
                                                      price,
                                                      royalty,
                                                      isOnSale,
                                                      eventDate,
                                                      eventTime,
                                                      ticketClass).build_transaction({
                                                          "from": self.mainAddress,
                                                          "nonce": nonce,
                                                          "gas": 2000000,
                                                          "gasPrice": self.w3.eth.gas_price,
                                                      })
        # Sign the transaction
        signed_transcation = self.w3.eth.account.signTransaction(
            result, privateKey[self.mainAddress])
        # Send the transaction
        tx_hash = self.w3.eth.sendRawTransaction(
            signed_transcation.rawTransaction)  # Wait for the transaction to be mined
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        return tx_receipt



    def getTicketDetail(self, _ticketId):
        detail = self.contract.functions.getTicketDetail(_ticketId).call()
        return detail

    def getUserTickets(self):
        total = self.contract.functions.getUserTickets(

        ).call()
        return total


class TicketFunctions:
    def __init__(self,  _address):
        with open(f"C:/Users/X/Desktop/BetcProj/marketPlace/Contracts/TicketMarketplaceABI.json", "r") as file:
            self.abi = file.read()

        self.w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
        self.contract_address = self.w3.eth.contract(
            address=_address, abi=self.abi)

    def setTicketForSale(self, address, tokenId, price):
        # Get the latest transaction count
        nonce = self.w3.eth.getTransactionCount(address)
        # Submit the transaction to call the `LOGIN` function
        transaction = self.contract_address.functions.setTicketForSale(int(tokenId), int(price)
        ).build_transaction(
                {
                        "from": address,
                        "nonce": nonce,
                        "gas": 1000000,
                        "gasPrice": self.w3.eth.gasPrice,
                }
        )
        # Sign the transaction
        signed_transaction = self.w3.eth.account.signTransaction(transaction, privateKey[address])
        # Send the transaction
        tx_hash = self.w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
        # Wait for the transaction to be mined
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)

        # Return the transaction receipt
        return tx_receipt

    def cancelSale(self, address, tokenId):
        # Get the latest transaction count
        nonce = self.w3.eth.getTransactionCount(address)
        # Submit the transaction to call the `LOGIN` function
        transaction = self.contract_address.functions.cancelSale(int(tokenId)).build_transaction(
                {
                        "from": address,
                        "nonce": nonce,
                        "gas": 1000000,
                        "gasPrice": self.w3.eth.gasPrice,
                }
        )
        # Sign the transaction
        signed_transaction = self.w3.eth.account.signTransaction(transaction, privateKey[address])
        # Send the transaction
        tx_hash = self.w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
        # Wait for the transaction to be mined
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)

        # Return the transaction receipt
        return tx_receipt



    def getTotalTickets(self):
        total = self.contract_address.functions.getTotalTickets().call()
        return total

    def getTicketDetail(self):
        detail = self.contract_address.functions.getTicketDetail(
            1).call()
        return detail

    def getSecTicketDetail(self, Tid):
        detail = self.contract_address.functions.getTicketDetail(Tid).call()
        return detail

    def getUserTickets(self):
        total = self.contract_address.functions.getUserTickets(

        ).call()
        return total

    def chackOwner(self, tokenId):
        total = self.contract_address.functions.chackOwner(tokenId).call()
        return total

    def buyTicket(self, _address, tokenId, _ticketPrice):
        nonce = self.w3.eth.getTransactionCount(_address)

        # Submit the transaction to call the `register` function
        transaction = self.contract_address.functions.buyTicket(tokenId).build_transaction(
            {
                "from": _address,
                "value": _ticketPrice,
                'nonce':nonce,
                "gas": 2000000,
                "gasPrice": self.w3.eth.gasPrice,
            }
        )
        # Sign the transaction
        signed_transaction = self.w3.eth.account.signTransaction(
             transaction, privateKey[_address])
         # Send the transaction
        tx_hash = self.w3.eth.sendRawTransaction(
             signed_transaction.rawTransaction)
        # # Wait for the transaction to be mined
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)

        # Return the transaction receipt
        return tx_receipt, transaction

    def burn(self, address, TOKEN_ID):

        transaction = self.contract_address.functions.burn(
                TOKEN_ID
        ).transact(
                {
                        "from": address,
                        "gas": 1000000,
                        "gasPrice": self.w3.eth.gasPrice,
                }
        )
        # Sign the transaction
        # signed_transaction = self.w3.eth.account.signTransaction(transaction, privateKey[address])
        # # Send the transaction
        # tx_hash = self.w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
        # Wait for the transaction to be mined
        tx_receipt = self.w3.eth.waitForTransactionReceipt(transaction)

        # Return the transaction receipt
        return tx_receipt



'''
ticket_contract = Deploy(_address='0x75cE2d76722654A492d8b158915e6177F3E35927')
print('the address is :',ticket_contract.contract_add())
ticket_contract.contract_ticket(name='any',
                                ticketNum=5,
                                ticketClass='vip',
                                eventDate='any',
                                eventTime='any',
                                isOnSale=True,
                                description='any',
                                imageURL='any',
                                royalty=12,
                                price=12)

total = ticket_contract.getTotalTickets()
print(total)

    def setTicketForSale(self, address, tokenId,
                         price
                         ):
        # Get the latest transaction count
        nonce = self.w3.eth.getTransactionCount(address)

        # Submit the transaction to call the `register` function
        transaction = self.contract.functions.register(
                address, tokenId,
                price
        ).build_transaction(
                {
                        "from": address,
                        "nonce": nonce,
                        "gas": 1000000,
                        "gasPrice": self.w3.eth.gasPrice,
                }
        )
        # Sign the transaction
        signed_transaction = self.w3.eth.account.signTransaction(transaction, privateKey[address])
        # Send the transaction
        tx_hash = self.w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
        # Wait for the transaction to be mined
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        return tx_receipt

    '''

# n = Deploy()

# n.deploy_nft()

# s = n.contract_ticket(5, "name", "description", "imageURL", 12, 12, True, 'as ', '12', '1')
# print(s)
