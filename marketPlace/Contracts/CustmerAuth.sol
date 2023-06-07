// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
pragma experimental ABIEncoderV2;

// Define a contract for the registration system
contract CustmerAuth {

    address[] public addressList;


    struct UserDetail {
        address addr;
        string name;
        string phone;
        string email;
        string password;
        bool isUserLoggedIn;
        bool isUserRegister;
    }

    mapping(address => UserDetail) user;

    // user registration function
    function register(
        address _address,
        string memory _name,
        string memory _Phone,
        string memory _email,
        string memory _password

    ) public returns (bool) {
        // Check if there is no entry in the user mapping for the address
        if (user[_address].isUserRegister == false) {
            require(user[_address].addr != msg.sender);
            user[_address].addr = _address;
            user[_address].name = _name;
            user[_address].phone = _Phone;
            user[_address].email = _email;
            user[_address].password = _password;
            user[_address].isUserLoggedIn = false;
            user[_address].isUserRegister = true;
            addressList.push(msg.sender);
            return true;
        } else {
            return false;
        }
    }

    function changeUserPassword(address _address, string memory _password) public returns (bool){
        user[_address].email = _password;
        return true;
    }

    function changeUserProfile(address _address, string memory _name
                                    , string memory _email
                                    , string memory _Phone
                                    ) public returns (bool){
            user[_address].name = _name;
            user[_address].password = _email;
            user[_address].phone = _Phone;
            return true;
    }


    function getUserDetail(address _address)
        public
        view
        returns (
            string memory,
            string memory,
            string memory
        )
    {
        return (
            user[_address].name,
            user[_address].phone,
            user[_address].password
        );
    }

    // user login function
    function login(address _address, string memory _password)
        public
        returns (bool)
    {
        // Check if the password matches the stored password
        if (
            keccak256(abi.encodePacked(user[_address].email)) ==
            keccak256(abi.encodePacked(_password))
        ) {
            // Set the isUserLoggedIn flag to true
            user[_address].isUserLoggedIn = true;
            return true;
        } else {
            return false;
        }
    }

    function getAllUserAddresses() public view returns (address[] memory) {
        uint count = 0;
        for (uint i = 0; i < addressList.length; i++) {
            if (user[addressList[i]].isUserRegister) {
                count++;
            }
        }
        address[] memory userAddresses = new address[](count);
        count = 0;
        for (uint i = 0; i < addressList.length; i++) {
            if (user[addressList[i]].isUserRegister) {
                userAddresses[count] = addressList[i];
                count++;
            }
        }
        return userAddresses;
    }

    // check the user logged In or not
    function checkIsUserLogged(address _address) public view returns (bool) {
        return (user[_address].isUserLoggedIn);
    }

    // check the user Register In or not
    function checkIsUserRegister(address _address) public view returns (bool) {
        return (user[_address].isUserRegister);
    }

    // logout the user
    function logout(address _address) public returns (bool) {
        user[_address].isUserLoggedIn = false;
        return user[_address].isUserLoggedIn;
    }
}
