import itertools
from web3 import Web3
import multiprocessing

factory_contract_address = '' # factory that generates vanity contract
contract_bytecode = ''
target_pattern = '0x00000' # how you want your addy to look like. more cool = more computation and time!

bytecode_hash = Web3.solidityKeccak(['bytes'], [contract_bytecode])

def worker(start, step, factory_address, pattern, bytecode_hash, found_flag, result_queue):
    result = find_cool_address(start, step, factory_address, pattern, bytecode_hash, found_flag)
    if result[0] is not None:
        result_queue.put(result)

def main():
    processes = []
    result_queue = multiprocessing.Queue()
    found_flag = multiprocessing.Value('i', 0)
    num_cores = multiprocessing.cpu_count()

    for i in range(num_cores):
        p = multiprocessing.Process(target=worker, args=(i, num_cores, factory_contract_address, target_pattern, bytecode_hash, found_flag, result_queue))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    while not result_queue.empty():
        salt, address = result_queue.get()
        print(f"Found vanity address: {address} with salt: {salt}")

def find_cool_address(start, step, factory_address, pattern, bytecode_hash, found_flag):
    for salt in itertools.count(start=start, step=step):
        if found_flag.value:  # Check if another worker has already found the address
            break
        potential_address = Web3.solidityKeccak(
            ['bytes', 'address', 'uint256', 'bytes'],
            ['0xff', factory_address, salt, bytecode_hash]
        )[-20:]

        if potential_address.hex().startswith(pattern):
            found_flag.value = True  # Signal other workers to stop
            return salt, potential_address.hex()
    return None, None

if __name__ == "__main__":
    main()