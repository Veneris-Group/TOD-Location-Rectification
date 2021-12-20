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


Tasks to do:  

- Implementation:
    - Use the benchmark to test
- Writing:
    - Write a skelton of the paper: what story we want to tell in the paper: Focusing on automatically repairing TOD vulnerabilities and how automated vulnerabilites patching tools for smart contracts don't handle TOD type vulnerabilities.  
