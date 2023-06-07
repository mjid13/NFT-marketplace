import json
from solcx import compile_source, install_solc
from web3 import Web3
from .accounts import privateKey


class Deploy:
    def __init__(self):

        with open("C:/Users/X/Desktop/BetcProj/marketPlace/Contracts/CustmerAuthABI.json", "r") as file:
            self.abi = file.read()

        with open("C:/Users/X/Desktop/BetcProj/marketPlace/Contracts/CustmerAuthBYTE.txt", "r") as file:
            self.bytecode = file.read()

        self.w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
        self.mainAddress = self.w3.eth.accounts[0]

        self.w3.eth.default_account = self.w3.eth.accounts[0]
        self.contract = self.w3.eth.contract(abi=self.abi, bytecode=self.bytecode)
        nonce = self.w3.eth.getTransactionCount(self.mainAddress)

        # Submit the transaction that deploys the contract
        transaction = self.contract.constructor().transact()


        # Wait for the transaction to be mined
        tx_receipt = self.w3.eth.waitForTransactionReceipt(transaction)

        # Get the contract instance
        self.contract = self.w3.eth.contract(address=tx_receipt.contractAddress, abi=self.abi)


    def customer_register(self, address, name,
                          phone, email, password
                          ):
        # Get the latest transaction count
        nonce = self.w3.eth.getTransactionCount(address)

        # Submit the transaction to call the `register` function
        transaction = self.contract.functions.register(
                address, name, phone, email, password
        ).build_transaction(
                {
                        "from": address,
                        "nonce": nonce,
                        "gas": 1000000,
                        "gasPrice": self.w3.eth.gas_price,
                }
        )
        # Sign the transaction
        signed_transaction = self.w3.eth.account.sign_transaction(transaction, privateKey[address])

        # Send the transaction
        tx_hash = self.w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
        # Wait for the transaction to be mined
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        # Return the transaction receipt
        return tx_receipt

    def changeUserPassword(self, address, password):
        # Submit the transaction to call the `register` function
        nonce = self.w3.eth.getTransactionCount(address)
        transaction = self.contract.functions.changeUserPassword(address, password).build_transaction({
                "from": address,
                "nonce": nonce,
                "gas": 1000000,
                "gasPrice": self.w3.eth.gasPrice,
        })

        # Sign the transaction
        signed_transaction = self.w3.eth.account.signTransaction(transaction, privateKey[address])

        # Send the transaction
        tx_hash = self.w3.eth.sendRawTransaction(signed_transaction.rawTransaction)

        # Wait for the transaction to be mined
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)

        # Return the transaction receipt
        return tx_receipt

    def changeUserProfile(self, address, name, phone, email):
        # Submit the transaction to call the `register` function
        nonce = self.w3.eth.getTransactionCount(address)
        transaction = self.contract.functions.changeUserProfile(address, name, email, phone).build_transaction({
                "from": address,
                "nonce": nonce,
                "gas": 1000000,
                "gasPrice": self.w3.eth.gasPrice,
        })

        # Sign the transaction
        signed_transaction = self.w3.eth.account.signTransaction(transaction, privateKey[address])

        # Send the transaction
        tx_hash = self.w3.eth.sendRawTransaction(signed_transaction.rawTransaction)

        # Wait for the transaction to be mined
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)

        # Return the transaction receipt
        return tx_receipt

    def login(self, address, password):
        # Get the latest transaction count
        nonce = self.w3.eth.getTransactionCount(address)
        # Submit the transaction to call the `LOGIN` function
        transaction = self.contract.functions.login(
                address, password
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

    def logout(self, address):
        # Get the latest transaction count
        nonce = self.w3.eth.getTransactionCount(address)
        # Submit the transaction to call the `LOGOUT` function
        transaction = self.contract.functions.logout(address).build_transaction(
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

    def isRegister(self, address):
        status = self.contract.functions.checkIsUserRegister(address).call()
        return status

    def isLogin(self, address):
        status = self.contract.functions.checkIsUserLogged(address).call()
        return status

    def getAllUserAddresses(self):
        users = self.contract.functions.getAllUserAddresses().call()
        return users

    def getUser(self, address):
        # Call the `UserDetail` struct for the user
        user = self.contract.functions.getUserDetail(address).call()

        user_detail = {'name': user[0], 'phone': user[1], 'email': user[2]}

        return user_detail

    def wallet_accunte(self):
        import random
        address = random.choice(list(privateKey.keys()))

        return address
