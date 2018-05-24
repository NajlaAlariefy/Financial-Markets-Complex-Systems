# Are Stock Markets Self-Organising Criticalities?


## Intro

The project is a multi-agent based system simulating a single stock market. It was built to investigate the dynamics of stock markets, attempting to draw an analogy between it and the Abelian (Bak-Tang-Wiesenfeld) sandpile simulation using evidence of power-law behaviour, to study self-organising criticality and non-Gaussian statistics.  Both simulations are used to build up intuition about the behaviour of complex systems, which are systems that have many components and a lot of energy flow between them. The modified Abelian sandpile simulation can be found [here](https://github.com/NajlaAlariefy/BTW-Sandpile).


## Setup

You can run this simulation in the **Stock Market Simulation.ipynb** iPython notebook:   

1. Download the repo  
2. Make sure you have [Jupyter Notbook](https://jupyter.org/install) installed
3. Run the cells in Notebook, and explore the data!


## Files

1. main.py : this file contains the default setting of running the simulation through the CLI, but for explorative analysis the notebook is recommended
2. stock_market.py : this file contains the main function **run_market** that runs the simulation
3. stock.py : the Stock class module
4. trader.py : the Trader class module
5. util.py : data representation functions (i.e. plots and wrangling)
6. distributions.py : a function plotting all distributions on a given histogram. [Source](https://stackoverflow.com/a/37616966/2211869)
