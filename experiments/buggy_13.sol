/**
 * Source Code first verified at https://etherscan.io on Thursday, April 25, 2019
 (UTC) */

pragma solidity >=0.4.22 <0.6.0;


contract BitCash {
    // Public variables of the token
  bool claimed_TOD20 = false;
address  owner_TOD20;
uint256 reward_TOD20;
function setReward_TOD20() public payable {
        require (!claimed_TOD20);

        require(msg.sender == owner_TOD20);
        owner_TOD20.transfer(reward_TOD20);
        reward_TOD20 = msg.value;
    }

    function claimReward_TOD20(uint256 submission) public {
        require (!claimed_TOD20);
        require(submission < 10);

        msg.sender.transfer(reward_TOD20);
        claimed_TOD20 = true;
    }
}