
import web3 from 'web3';

async function getAddress() {
    // Check if the user has the MetaMask extension installed and is logged in
    if (typeof window.ethereum !== 'undefined') {
        // Request access to the user's accounts
        try {
            await window.ethereum.enable();
            // Get the user's accounts
            const accounts = await web3.eth.getAccounts();
            // Get the first account
            const address = accounts[0];
            // Send the address to the Django server using an HTTP request
            const response = await fetch('/index/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ address: address })
            });
            console.log(response);
        } catch (error) {
            console.error(error);
        }
    } else {
        console.error('MetaMask is not installed or not logged in');
    }
}

