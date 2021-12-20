# Smart-Contract-Repair
Repository for anything related to Smart Contract Repair

## Links
* [SGaurd](https://github.com/duytai/sGuard.git)
* [Slither](https://github.com/crytic/slither)
* [SWC Registry](https://swcregistry.io/docs/SWC-114)
* [Ganache Web](https://www.trufflesuite.com/ganache)
* [Ganache Github](https://github.com/trufflesuite/ganache-core)
* [Solidity Parser](https://github.com/solidity-parser/parser)
* [OYENTE](https://github.com/enzymefinance/oyente)
* [libsubmarine](https://github.com/lorenzb/libsubmarine)

## Insertion Vulnerability: High-Level Solutions

### Trace Comparison Solution

**Key Observation**: A complete solution to TOD would be checking that the state of the global variables have not changed since time of the original transaction, i.e. are the variables the values you expected them to be? Thus, this problem can be reduced to finding the optimal subset of global variable checks for each function.

**Simplifying Assumption**: Let's limit our search to only pair-wise TODs, meaning the attacker can only execute 1 function before our function executes.

Suppose we have some sort of execution trace that keeps track of the state of the global variables. We can just do a comparison of these traces for each pair-wise combination of funciton executions. Where these traces differ is what is causing the TOD, and then we just put a require statement at the top of the function for the variable that changed. Suppose the contract contains N functions, then we could have N^2 combinations to check, which is tractable.

Using something like an Ether flow trace would be more efficient than a full state trace.

### Points-to Analysis Solution: 

```
For each variable v and a function f: we use Points-to_Analysis(f,v)[1]
to denote a function that returns the sets of contract fields that have relationships with v inside the function f.

For each public function f with a set of parameters P in a contract C 
(we assume that P contains only variables of type address) 
    For each p in P, we compute G = Points-to_Analysis(f,p)
        For each variable g in G, if there exists a public setter function f' 
        that can modify the value of g then we need to 
        add g as parameter to f and add a guard to guarantee that the value of g doesn't change. 

Now, the main challenge will be in computing the values in Points-to_Analysis(f,v). 

Here we can assume that we only care about variables that can be transferred such as rewards: 
For instance if we have in the code of f v.transfer(r) and r is a contract variable then 
we must have r outputted by Points-to_Analysis(f,v). 
``` 
[1](https://en.wikipedia.org/wiki/Alias_analysis)


## Displacement Vulnerability: High-Level Solution

TODO


## Installation of Usage

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
