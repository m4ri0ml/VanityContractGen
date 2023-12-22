pragma solidity ^0.8.0;

contract Factory {
    event Deployed(address addr, uint256 salt);

    function deploy(bytes memory code, uint256 salt) public {
        address addr;
        
        // Using CREATE2 opcode
        assembly {
            addr := create2(0, add(code, 0x20), mload(code), salt)
            if iszero(extcodesize(addr)) {
                revert(0, 0)
            }
        }

        emit Deployed(addr, salt);
    }

    function getBytecode() public pure returns (bytes memory) {
        bytes memory bytecode = type(YourContract).creationCode;
        return bytecode;
    }
}