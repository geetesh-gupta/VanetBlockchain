pragma solidity ^0.5.16;

contract AdditionContract {
  uint public state = 0;

  function add(uint value1, uint value2) public {
    state = value1 + value2;
  }

  function getState() public view returns (uint) {
      return state;
  }
}