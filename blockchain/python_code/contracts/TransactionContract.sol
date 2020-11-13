pragma solidity >=0.4.22;

contract TransactionContract {
    struct Message_info {
        uint senderID;
        uint receiverID;
        uint message;
    }

    mapping(uint256 => Message_info) public transactions;

    constructor(
        uint  message,
        uint  senderID,
        uint  receiverID,
        uint256 ids
    ) public {
        Message_info memory received = Message_info({
            senderID: senderID,
            receiverID: receiverID,
            message: message
        });
        transactions[ids] = received;
    }
}
