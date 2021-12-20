pragma solidity ^0.4.18;

contract Purchase {
    uint256 price;
    address owner;
    
    event Purchase(address _buyer, uint256 _price);
    event PriceChange(address _owner, uint256 _price);
    
    modifier ownerOnly() {
        require(msg.sender == owner);
        _;
    }

    constructor() {
        // constructor
        owner = msg.sender;
        price = 100;
    }

    function buy() returns (uint256) {   
        owner = msg.sender;
        Purchase(msg.sender, price);
        return price;
    }

    function setPrice(uint256 _price) ownerOnly() {
        price = _price;
        PriceChange(owner, price);
    }
}
