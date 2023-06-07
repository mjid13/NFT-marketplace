from solcx import compile_source, install_solc
from web3 import Web3
import json

# Connect to local Ganache instance
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

cont = ['adminControl', 'NFTRegistry', 'TicketMarketplace', 'OrgAuth', 'CustmerAuth']
'''
for i in cont:
    with open(f"./{i}.sol", "r") as file:
        solidity_source = file.read()


    compiled_sol = compile_source(solidity_source)
    print(compiled_sol)

    contract_bytecode = compiled_sol[f'<stdin>:{i}']['bin']
    contract_abi = compiled_sol[f'<stdin>:{i}']['abi']

    # print(contract_abi)
    with open(f'{i}ABI.json', 'w') as f:
        json.dump(contract_abi, f)

    # print(contract_abi)
    with open(f'{i}ByteCode.json', 'w') as f:
        json.dump(contract_bytecode, f)


'''
with open(f"./TicketMarketplace.sol", "r") as file:
    solidity_source = file.read()

compiled_sol = compile_source(solidity_source)
#print(compiled_sol)

bytecode = compiled_sol[f'<stdin>:TicketMarketplace']['bin']
abi = compiled_sol[f'<stdin>:TicketMarketplace']['abi']

#w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

mainAddress = '0xEb1005c38Ef8B4F81609E0BE497795ebF03fec2F'

with open('TicketMarketplaceABI.json', 'w') as f:
    json.dump(abi, f)

with open('TicketMarketplaceBYTE.txt', 'w') as f:
    f.write(bytecode)

contract = w3.eth.contract(abi=abi, bytecode=bytecode)

nonce = w3.eth.getTransactionCount(mainAddress)
w3.eth.default_account = w3.eth.accounts[0]
# Submit the transaction that deploys the contract
#transaction = contract.constructor().transact()
# Sign the transaction
#tx_receipt = w3.eth.waitForTransactionReceipt(transaction)
#contract_address = tx_receipt.contractAddress

#contract = w3.eth.contract(address=contract_address, abi=abi)
'''
#signed_transcation = w3.eth.account.signTransaction(transaction, '6577f88ff221f9568b6013144521e29aa74b2b175b3baf367959c078df705ea8')
# Send the transaction
tx_hash = w3.eth.sendRawTransaction(signed_transcation.rawTransaction)
# Wait for the transaction to be mined
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

# Get the contract instance
contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)


#contract = w3.eth.contract(abi=abi, bytecode=bytecode)

s = contract.functions.register(mainAddress, 'asd123', "asd123").build_transaction(
        {
                "from": mainAddress,
                "nonce": nonce,
                "gas": 1000000,
                "gasPrice": w3.eth.gasPrice,
        },
)

f = contract.functions.login(mainAddress, "asd123").build_transaction(
        {
                "from": mainAddress,
                "nonce": nonce,
                "gas": 1000000,
                "gasPrice": w3.eth.gasPrice,
        },
)

n = contract.functions.islogin(mainAddress).call()
k = contract.functions.tstt().call()


print(f)
print(n)
print(k)
print(s)'''
