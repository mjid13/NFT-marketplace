// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;


import "openzeppelin-contracts/contracts/token/ERC721/extensions/ERC721Enumerable.sol";


contract NFTRegistry {
    mapping(address => address[]) public organizerContracts;
    address[] public organizers;
    address[] public tickets;

    function createOrganizerNFT(address nftTicket) public returns (address) {
        address nftAddress = address(nftTicket);
        organizerContracts[msg.sender].push(nftAddress);
        organizers.push(msg.sender);
        tickets.push(nftAddress);
        return address(nftTicket);
    }



    function getOwnedNFTs(address account, address nftContractAddress) public view returns (uint256[] memory) {
        IERC721Enumerable _nftContract = IERC721Enumerable(nftContractAddress);
        uint256 nftCount = _nftContract.balanceOf(account);
        uint256[] memory tempNftIds = new uint256[](nftCount);
        for (uint256 j = 0; j < nftCount; j++) {
            tempNftIds[j] = _nftContract.tokenOfOwnerByIndex(account, j);
        }

        return tempNftIds;
    }


    function mergeArrays(uint256[] memory array1, uint256[] memory array2) private pure returns (uint256[] memory) {
        uint256[] memory merged = new uint256[](array1.length + array2.length);
        uint256 index = 0;
        for (uint256 i = 0; i < array1.length; i++) {
            merged[index] = array1[i];
            index++;
        }
        for (uint256 i = 0; i < array2.length; i++) {
            merged[index] = array2[i];
            index++;
        }
        return merged;
    }


    function getOrganizerNFT(address _user)
        public
        view
        returns (address[] memory)
    {
        return organizerContracts[_user];
    }

    function getAllTickets() public view returns (address[] memory) {
        return tickets;
    }

    function getAllOrganizers() public view returns (address[] memory) {
        return organizers;
    }
}
