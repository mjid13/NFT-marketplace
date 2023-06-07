import json
from solcx import compile_source, install_solc
from web3 import Web3
from .accounts import privateKey


class Deploy:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

        with open(f"C:/Users/X/Desktop/BetcProj/marketPlace/Contracts/NFTRegistryABI.json", "r") as file:
            self.abi = file.read()

        with open(f"C:/Users/X/Desktop/BetcProj/marketPlace/Contracts/NFTRegistryBYTE.txt", "r") as file:
            self.bytecode = file.read()

        # compiled_sol = compile_source(solidity_source)
        # print(compiled_sol)

        # self.bytecode = compiled_sol[f'<stdin>:NFTRegistry']['bin']
        # self.abi = compiled_sol[f'<stdin>:NFTRegistry']['abi']

        self.mainAddress = self.w3.eth.accounts[0]

        self.contract = self.w3.eth.contract(
            abi=self.abi, bytecode=self.bytecode)

    def deployNftRegistry(self):
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
        signed_transcation = self.w3.eth.account.signTransaction(
            transaction, privateKey[self.mainAddress])
        # Send the transaction
        tx_hash = self.w3.eth.sendRawTransaction(
            signed_transcation.rawTransaction)
        # Wait for the transaction to be mined
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)

        # Get the contract instance
        self.contract = self.w3.eth.contract(
            address=tx_receipt.contractAddress, abi=self.abi)

    def createUserNFT(self, address, nftAddress):
        # Get the latest transaction count
        nonce = self.w3.eth.getTransactionCount(address)

        # Submit the transaction to call the `register` function
        transaction = self.contract.functions.createOrganizerNFT(nftAddress).build_transaction(
            {
                "from": address,
                "nonce": nonce,
                "gas": 1000000,
                "gasPrice": self.w3.eth.gasPrice,
            }
        )
        # Sign the transaction
        signed_transaction = self.w3.eth.account.signTransaction(
            transaction, privateKey[address])
        # Send the transaction
        tx_hash = self.w3.eth.sendRawTransaction(
            signed_transaction.rawTransaction)
        # Wait for the transaction to be mined
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)

        # Return the transaction receipt
        return tx_receipt, transaction

    def getOrganizerNFT(self, address):
        status = self.contract.functions.getOrganizerNFT(address).call()
        return status

    def getOwnedNFTs(self, address, ticketsList):
        status = self.contract.functions.getOwnedNFTs(address, ticketsList).call()
        return status

    def getAllTickets(self):
        status = self.contract.functions.getAllTickets().call()
        return status

    def getAllOrganizers(self):
        status = self.contract.functions.getAllOrganizers().call()
        return status


'''
myd = Deploy()
mainAddress = '0xEb1005c38Ef8B4F81609E0BE497795ebF03fec2F'
myd.deployNftRegistry()
print(myd.createUserNFT(mainAddress,"ana","ANA",'assas'))

#n= myd.getUserNFT(mainAddress)

#print(n)


with open(f"C:/Users/X/Desktop/BetcProj/marketPlace/Contracts/NFTRegistry.sol", "r") as file:
    solidity_source = file.read()

compiled_sol = compile_source(solidity_source)
#print(compiled_sol)

bytecode = compiled_sol[f'<stdin>:NFTRegistry']['bin']
abi = compiled_sol[f'<stdin>:NFTRegistry']['abi']

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

mainAddress = '0xb23c702BD187F08f92c15744B6d4c71a82494295'

contract = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.getTransactionCount(mainAddress)
transaction = contract.constructor().build_transaction(
        {
                "from": mainAddress,
                "nonce": nonce,
                "gas": 1000000,
                "gasPrice": w3.eth.gasPrice,
        },
)
# Sign the transaction
signed_transcation = w3.eth.account.signTransaction(transaction, '08a1fcffe76c4dd951a1a839997172ae74da65124665c925dfcd038bfdd57859')
# Send the transaction
tx_hash = w3.eth.sendRawTransaction(signed_transcation.rawTransaction)
# Wait for the transaction to be mined
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

# Get the contract instance
contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)


print('status =', contract.functions.getAllUsers().call())
# Get the latest transaction count


# Submit the transaction to call the `register` function
transaction = contract.functions.createUserNFT(
         'name', 'email', 'asa').build_transaction(
                {
                 "from": mainAddress,
                    'to':'0x9ea4C632bAd7D452c00E54986b287Ef4198380c2',
                 "nonce": nonce,
                 "gas": 2000000,
                 "gasPrice": w3.eth.gasPrice,
                }
        )
# Sign the transaction
signed_transaction = w3.eth.account.signTransaction(transaction, '08a1fcffe76c4dd951a1a839997172ae74da65124665c925dfcd038bfdd57859')
# Send the transaction
tx_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
# Wait for the transaction to be mined
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

print(signed_transaction)



status = contract.functions.getAllUsers().call()
'''
