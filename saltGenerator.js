const ethers = require('ethers');
const factoryContract = '...';
const provider = ethers.getDefaultProvider('ropsten');

async function findCoolAddress(bytecode) {
    let salt = 0;
    while (true) {
        let computedAddress = ethers.utils.getCreate2Address(
            factoryContract,
            ethers.utils.hexZeroPad(ethers.utils.hexlify(salt), 32),
            ethers.utils.keccak256(bytecode)
        );

        if (computedAddress.startsWith('0x0000')) { // how you want your addy to look like. more cool = more computation and time!
            console.log(`Found vanity address: ${computedAddress} with salt: ${salt}`);
            break;
        }

        salt++;
    }

    return salt;
}

async function main() {
    const factory = new ethers.Contract(factoryContract, Factory.abi, provider);
    const bytecode = await factory.getBytecode();

    const salt = await findVanityAddress(bytecode);
    console.log(`Use this salt for deployment: ${salt}`);
}

main();