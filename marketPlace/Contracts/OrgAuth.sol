// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// Define a contract for the registration system
contract OrgAuth {

    address[] public addressList;
    address[] public conformedList;

    struct OrganizerDetail {
        address addr;
        string name;
        string phone;
        string email;
        string password;
        bool isUserValid;
        bool isUserLoggedIn;
        bool isUserRegister;
    }

    mapping(address => OrganizerDetail) organizer;

    // user registration function
    function register(
        address _address,
        string memory _name,
        string memory _email,
        string memory _Phone,
        string memory _password
    ) public returns (bool) {
        // Check if there is no entry in the user mapping for the address
        if (organizer[_address].isUserRegister == false) {
            require(organizer[_address].addr != msg.sender);
            organizer[_address].addr = _address;
            organizer[_address].name = _name;
            organizer[_address].email = _email;
            organizer[_address].phone = _Phone;
            organizer[_address].password = _password;
            organizer[_address].isUserLoggedIn = false;
            organizer[_address].isUserValid = false;
            organizer[_address].isUserRegister = true;
            addressList.push(msg.sender);
            return true;
        } else {
            return false;
        }
    }

    function removeOrganizer(address _address) public returns (bool) {
    require(organizer[_address].isUserRegister == true, "Organizer does not exist");

    // Remove organizer from mapping
    delete organizer[_address];

    // Remove organizer from addressList array
    for (uint i = 0; i < addressList.length; i++) {
        if (addressList[i] == _address) {
            // Swap with last element in array and then delete last element
            addressList[i] = addressList[addressList.length - 1];
            addressList.pop();
            break;
        }
    }

    return true;
}

   function changeUserPassword(address _address, string memory _password) public returns (bool){
        organizer[_address].email = _password;
        return true;
    }

    function changeUserProfile(address _address, string memory _name
                                    , string memory _email
                                    , string memory _Phone
                                    ) public returns (bool){
            organizer[_address].name = _name;
            organizer[_address].password = _email;
            organizer[_address].phone = _Phone;
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
            organizer[_address].name,
            organizer[_address].phone,
            organizer[_address].password
        );
    }

    function getAllUserAddresses() public view returns (address[] memory) {
        uint count = 0;
        for (uint i = 0; i < addressList.length; i++) {
            if (organizer[addressList[i]].isUserRegister) {
                count++;
            }
        }
        address[] memory userAddresses = new address[](count);
        count = 0;
        for (uint i = 0; i < addressList.length; i++) {
            if (organizer[addressList[i]].isUserRegister) {
                userAddresses[count] = addressList[i];
                count++;
            }
        }
        return userAddresses;
    }



    // user login function
    function login(address _address, string memory _password)
        public
        returns (bool)
    {
        // Check if the password matches the stored password
        if (
            keccak256(abi.encodePacked(organizer[_address].email)) ==
            keccak256(abi.encodePacked(_password))
        ) {
            // Set the isUserLoggedIn flag to true
            organizer[_address].isUserLoggedIn = true;
            return organizer[_address].isUserLoggedIn;
        } else {
            return false;
        }
    }

    // check the user logged In or not
    function checkIsUserLogged(address _address) public view returns (bool) {
        return (organizer[_address].isUserLoggedIn);
    }

    // check the user Register In or not
    function checkIsUserRegister(address _address) public view returns (bool) {
        return (organizer[_address].isUserRegister);
    }

    // check the user Register In or not
    function checkIsUserValid(address _address) public view returns (bool) {
        return (organizer[_address].isUserValid);
    }

    // logout the user
    function logout(address _address) public returns (bool) {
        organizer[_address].isUserLoggedIn = false;
        return organizer[_address].isUserLoggedIn;
    }

    function changeUserValidation(address _address) public returns (bool) {
    organizer[_address].isUserValid = !organizer[_address].isUserValid;
    if (organizer[_address].isUserValid == true) {
        conformedList.push(_address);
    } else {
        for (uint i = 0; i < conformedList.length; i++) {
            if (conformedList[i] == _address) {
                conformedList[i] = conformedList[conformedList.length-1];
                conformedList.pop();
                break;
            }
        }
    }
    return organizer[_address].isUserValid;
}



    function getConformedList() public view returns (address[] memory) {
        return conformedList;
    }
}
