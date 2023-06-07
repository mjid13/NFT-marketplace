// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;


contract adminControl {


     struct AdminDetail {
        address addr;
        string name;
        string password;
        bool isUserLoggedIn;
        bool isUserRegister;
    }

    mapping(address => AdminDetail) admin;

// admin registration function
    function register(
        address _address,
        string memory _name,
        string memory _password
    ) public returns (bool) {
        // Check if there is no entry in the user mapping for the address
        if (admin[_address].isUserRegister == false) {
            require(admin[_address].addr != msg.sender);
            admin[_address].addr = _address;
            admin[_address].name = _name;
            admin[_address].password = _password;
            admin[_address].isUserLoggedIn = false;
            admin[_address].isUserRegister = true;
            return true;
        } else {
            return false;
        }
    }
    string tst = "EMPTY";

    // user login function
    function login(address _address, string memory _password)
        public
        returns (bool)
    {
        // Check if the password matches the stored password
        if (
            keccak256(abi.encodePacked(admin[_address].password)) ==
            keccak256(abi.encodePacked(_password))
        ) {
            tst = "I Pass";
            // Set the isUserLoggedIn flag to true
            admin[_address].isUserLoggedIn = true;
            return admin[_address].isUserLoggedIn;
        } else {
            tst = "I Did't Pass";
            return false;
        }
    }


    function logout(address _address) public returns (bool) {
        admin[_address].isUserLoggedIn = false;
        return admin[_address].isUserLoggedIn;
    }

    function islogin(address _address) public view returns (bool) {
        return (admin[_address].isUserLoggedIn);
    }

    // check the user Register In or not
    function checkIsUserRegister(address _address) public view returns (bool) {
        return (admin[_address].isUserRegister);
    }

    function tstt() public view returns (string memory) {
        return tst;
    }


}
