# Pricing in Ride-share Platforms: A Queueing-Theoretic Approach
The computational analysis of the research paper: [Pricing in Ride-share Platforms: A Queueing-Theoretic Approach](http://www.columbia.edu/~ww2040/8100F16/Riquelme-Johari-Banerjee.pdf)

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install packages:
```bash
pip install numpy
pip install matplotlib
pip install pandas
pip install scipy
```

## Structure 
Two different platform pricing strategies are used:
* Static Pricing
* Dynamic Pricing | Single-Threshold Pricing 
The underlying equations are used to replicate the figures in the large market limit.
Furthermore, an Agent-based model is used and benchmarked against the theoretic results.

## Static Pricing
### Theoretic
Run [static_theoretic.main()](static_theoretic.py) from [main.py](main.py).
### Agent
Run [static_agent.main()](static_agent.py) from [main.py](main.py).
### Simulation
The agent-based model is simulated by matching n drivers and passengers in the system: [static_simulation](static_simulation.py).
The simulation time may fluctuate slightly due to the randomly distributed interarrival times. For time frame analysis the [simulation](static_simulation.py) has to be modified in Line 34:
```bash
simulation_time = 2400       # Can be modified
if result_df.loc[i, "start_time"] > simTime:
    return True
```

## Dynamic Pricing
### Theoretic
Run [dynamic_theoretic.main()](dynamic_theoretic.py) from [main.py](main.py).
### Agent
Run [dynamic_agent.main()](dynamic_agent.py) from [main.py](main.py).
### Simulation
The [agent-based model](dynamic_simulation.py) is simulated for a specified amount of time. An object-oreinted approach is used to account for the number of drivers and passenger in the system a time *clock*.

## Equations & Figures

[Model_Queue](Model_Queue.py) accounts for all equations used from the research paper and the Code to create the figures

## 🤝 Support

Contributions, issues, and feature requests are welcome!

## License
[MIT](https://choosealicense.com/licenses/mit/)
