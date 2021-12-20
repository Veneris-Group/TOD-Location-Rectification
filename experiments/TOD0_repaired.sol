pragma solidity >= 0.4.0;

contract MMarketPlace {
   address owner;
   uint private cost = 100;
   uint private inventory = 20;

   event Purchase(address _buyer, uint256 _amt);

   function increasePrice(uint increaseCost) {
      require( msg.sender == owner );
      cost += increaseCost;
   }

   function buy(uint256 costExpected) returns(uint) {
      require(cost == costExpected);
      uint amt = msg.value / cost;
      require( inventory > amt );
      inventory -= amt;
      Purchase(msg.sender, amt);
   }
}

