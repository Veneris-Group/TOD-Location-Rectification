# Smart-Contract-Repair
Repository for anything related to Smart Contract Repair

## Links
* [Slither](https://github.com/crytic/slither)
* [SWC Registry](https://swcregistry.io/docs/SWC-114)


## Installation and Usage

creating and activating virtual environment (you can choose another name other than `sc_repair` if you would like)
```
conda create -n sc_repair python=3.8.5 
conda activate sc_repair
```

Command to deactive virtual environment when you are done
```
conda deactivate
```

required software
```
pip install slither-analyzer
pip install py-solc
pip install solc-select
```

slither requires a specific version of solc, 0.4.24 worked for me, not sure what other versions also work
```
solc-select install
solc-select install 0.4.24
solc-select use 0.4.24
```

Make sure you have the right solc version active
```
solc --version
> solc, the solidity compiler commandline interface
> Version: 0.4.24+commit.e67f0147.Darwin.appleclang
```

These are not required for core slither features, but some parts of slither need them
```
brew install graphviz
brew install xdot
```

To run the script, use the command
```
python smart_contract_repair.py /path/to/smart_contract.sol contract_name
```
 
## License

The MIT License applies to all the files in this repository, except for all the contracts files with names that start with Ethereum addresses `0x...`. These files are publicly available, were obtained using the [Etherscan APIs](https://etherscan.io/apis), and retain their original licenses. 
