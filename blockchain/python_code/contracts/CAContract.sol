pragma solidity >=0.4.22;

import "./TransactionContract.sol";

contract CAContract {
    uint256 counter = 0;

    function performTransaction(
        uint message,
        uint senderId,
        uint receiverId
    ) public returns (TransactionContract) {
        ++counter;
        TransactionContract contr = new TransactionContract(message, senderId, receiverId, counter);
        return contr;
    }
}
