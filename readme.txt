# Ethereum Vanity Address Finder

This repo provides Python and JS script for finding the salt needed to generate vanity Ethereum addresses using the `CREATE2` opcode. It's designed to efficiently brute-force salt values that lead to Ethereum contract addresses with a specified prefix pattern.

## Overview

Ethereum vanity addresses are those that have a specific set of characters at the beginning. This script utilizes the `CREATE2` opcode for deterministic contract address generation with a custom "vanity" pattern. I make use of Python's multiprocessing library, it parallelizes the search for an appropriate salt value that results in a contract address matching the desired pattern.

NOTE: If you want to generate a pattern of more than 6 or 7 consecutive characters you will need a lot of computing resources *and* further optimize the scripts provided (most likely by using a faster language).

## Features

- **Efficient Brute-Forcing**: Utilizes multiple CPU cores for parallel processing.
- **Customizable Pattern Matching**: Specify your desired address pattern.
- **Multiprocessing**: Distributes workload across available CPU cores to speed up the search process.

## Requirements

- Python 3.x
- [Web3.py](https://web3py.readthedocs.io/en/stable/) Python library

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/ethereum-vanity-address-finder.git
cd ethereum-vanity-address-finder
```

Install dependencies:
```bash
pip install web3
```

## Usage

**Set Up the Script**: Open `saltGanerator.py` and set your parameters:
   - `factory_contract_address`: Address of the deployed factory contract.
   - `contract_bytecode`: Bytecode of the contract you wish to deploy.
   - `target_pattern`: The desired starting pattern for the vanity address.

**Run the Script**:

```bash
python saltGanerator.py
```

The script will use *all* your available CPU cores and eventually output your desired vanity address and the corresponding salt value.

## How It Works

- The script divides the search space among multiple processes, each checking a unique set of salt values.
- Each process generates potential Ethereum addresses using `CREATE2` and checks if they match the specified pattern.
- Once a process finds a matching address, it signals others to stop, and the result is printed.
