// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "openzeppelin-contracts/contracts/token/ERC721/ERC721.sol";
import "openzeppelin-contracts/contracts/access/Ownable.sol";
import "openzeppelin-contracts/contracts/utils/Counters.sol";
import "openzeppelin-contracts/contracts/token/ERC721/extensions/ERC721Enumerable.sol";


contract TicketMarketplace is ERC721Enumerable, Ownable {
    using Counters for Counters.Counter;

    struct Ticket {
        string name;
        string description;
        string imageURL;
        uint256 price;
        uint256 royalty;
        bool isOnSale;
        bool isValid;
        string eventDate;
        string eventTime;
        string ticketClass;
        address creator;
        address owner;
        uint256 saleTimestamp;
    }

    Counters.Counter private _ticketIds;
    mapping(uint256 => Ticket) private _tickets;
    mapping(address => uint256[]) private _userTickets;

    // IPFS hash of the metadata file
    string private _baseTokenURI;

    event TicketCreated(
        uint256 indexed tokenId,
        string name,
        uint256 price,
        uint256 royalty,
        bool isOnSale,
        string eventDate,
        string eventTime,
        string ticketClass,
        address creator
    );
    event TicketSold(
        uint256 indexed tokenId,
        uint256 price,
        address oldOwner,
        address newOwner
    );

    constructor(
        string memory name,
        string memory symbol,
        string memory baseTokenURI
    ) ERC721(name, symbol) {
        _baseTokenURI = baseTokenURI;
    }

    function setBaseURI(string memory baseTokenURI) external onlyOwner {
        _baseTokenURI = baseTokenURI;
    }

    function _baseURI() internal view virtual override returns (string memory) {
        return _baseTokenURI;
    }

    function createTicket(
        uint256 ticketNum,
        string memory name,
        string memory description,
        string memory imageURL,
        uint256 price,
        uint256 royalty,
        bool isOnSale,
        string memory eventDate,
        string memory eventTime,
        string memory  ticketClass
    ) external onlyOwner {
        for (uint256 i = 1; i <= ticketNum; i++){
            _ticketIds.increment();
            uint256 newTicketId = _ticketIds.current();
            _tickets[newTicketId] = Ticket({
                name: name,
                description: description,
                imageURL: imageURL,
                price: price,
                royalty: royalty,
                isOnSale: isOnSale,
                isValid: true,
                eventDate: eventDate,
                eventTime: eventTime,
                ticketClass: ticketClass,
                creator: msg.sender,
                owner: msg.sender,
                saleTimestamp: 0
            });
            _mint(msg.sender, newTicketId);
            emit TicketCreated(
                newTicketId,
                name,
                price,
                royalty,
                isOnSale,
                eventDate,
                eventTime,
                ticketClass,
                msg.sender
            );
        }
    }

    function getTotalTickets() public view returns (uint256) {
        return totalSupply();
    }

    function getTicketDetail(uint256 _ticketId)
        public
        view
        returns (
            string memory,
            string memory,
            string memory,
            uint256,
            uint256,
            bool,
            string memory,
            string memory,
            string memory,
            address,
            address,
            uint256
        )
    {
        Ticket memory ticket = _tickets[_ticketId];
        return (
            ticket.name,
            ticket.description,
            ticket.imageURL,
            ticket.price,
            ticket.royalty,
            ticket.isOnSale,
            ticket.eventDate,
            ticket.eventTime,
            ticket.ticketClass,
            ticket.creator,
            ticket.owner,
            ticket.saleTimestamp
        );
    }



    function chackOwner(uint256 tokenId) public view returns (bool) {
        Ticket memory ticket = _tickets[tokenId];
        if (ownerOf(tokenId) == ticket.creator){
            return true;
        }
        else{
            return false;
        }

    }

    function buyTicket(uint256 ticketId) external payable {
        Ticket memory ticket = _tickets[ticketId];
        require(ticket.isOnSale, "Ticket is not available for purchase");
        require(msg.value >= ticket.price, "Insufficient funds to purchase ticket");
        if (ticket.royalty > 0) {
            uint256 royaltyAmount = (msg.value * ticket.royalty) / 100;
            payable(ticket.owner).transfer(msg.value - royaltyAmount);
            _transfer(ticket.owner, msg.sender, ticketId);
            payable(ticket.creator).transfer(royaltyAmount);
        }
        ticket.owner = msg.sender;
        ticket.isOnSale = false;
        ticket.saleTimestamp = block.timestamp;
        _tickets[ticketId] = ticket;
        emit TicketSold(ticketId, ticket.price, ticket.owner, msg.sender);

    }

    function setTicketForSale(uint256 tokenId, uint256 price) public {
        require(ownerOf(tokenId) == msg.sender, "Not ticket owner");
        require(_tickets[tokenId].isValid == true, "Invalid ticket");
        _tickets[tokenId].isOnSale = true;
        _tickets[tokenId].price = price;
    }

    function cancelSale(uint256 tokenId) public {
        require(ownerOf(tokenId) == msg.sender, "Not ticket owner");
        require(_tickets[tokenId].isValid == true, "Invalid ticket");
        _tickets[tokenId].isOnSale = false;
    }


    function getUserTickets(address user)
        external
        view
        returns (uint256[] memory)
    {
        return _userTickets[user];
    }

    function mint(address to, uint256 tokenId) external onlyOwner {
        _mint(to, tokenId);
    }

    function burn(uint256 tokenId) external onlyOwner {
        _burn(tokenId);
    }



    function invalidateTicket(uint256 tokenId) external onlyOwner {
        require(_tickets[tokenId].isValid == false, "Valid ticket");
        _tickets[tokenId].isValid = true;
    }


    function withdraw() external onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }
}

