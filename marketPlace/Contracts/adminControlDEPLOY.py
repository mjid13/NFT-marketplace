import json
from solcx import compile_source, install_solc
from web3 import Web3
from .accounts import privateKey

class Deploy:
    def __init__(self):


        with open(f"./Contracts/adminControl.sol", "r") as file:
            solidity_source = file.read()

        compiled_sol = compile_source(solidity_source)
        #print(compiled_sol)

        self.bytecode = compiled_sol[f'<stdin>:adminControl']['bin']
        self.abi = compiled_sol[f'<stdin>:adminControl']['abi']


        self.w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

        self.mainAddress = self.w3.eth.accounts[0]


        self.contract = self.w3.eth.contract(abi=self.abi, bytecode=self.bytecode)

    def deployOrg(self):
        nonce = self.w3.eth.getTransactionCount(self.mainAddress)

        # Submit the transaction that deploys the contract
        transaction = self.contract.constructor().build_transaction(
                {
                        "from": self.mainAddress,
                        "nonce": nonce,
                        "gas": 1000000,
                        "gasPrice": self.w3.eth.gasPrice,
                },
        )
        # Sign the transaction
        signed_transcation = self.w3.eth.account.signTransaction(transaction, privateKey[self.mainAddress])
        # Send the transaction
        tx_hash = self.w3.eth.sendRawTransaction(signed_transcation.rawTransaction)
        # Wait for the transaction to be mined
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)

        # Get the contract instance
        self.contract = self.w3.eth.contract(address=tx_receipt.contractAddress, abi=self.abi)


    def admin_register(self, address, name, password
                          ):
        # Get the latest transaction count
        nonce = self.w3.eth.getTransactionCount(address)

        # Submit the transaction to call the `register` function
        transaction = self.contract.functions.register(
                address, name,password,
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


    def isLogin(self,address):
        status = self.contract.functions.islogin(address).call()
        return status

    def isRegister(self,address):
        status = self.contract.functions.checkIsUserRegister(address).call()
        return status

