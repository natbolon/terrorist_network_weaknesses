# Identifying a Set of Key Players in a Terrorist Network
Network Tour of Data Science, 2018, EPFL

This is the directory for the project of the course "A Network Tour of Data Science" fall 2018, EPFL. This file contains practical information on the project implementation and how to run it. For more detailed explanation of the project (goals, implemented algorithms, ...), please refer to the report (`report.pdf`). 

The purpose of these project is learning various vulnerable points of a terrorist network by identifying a set of key players whose roles are vital to the success of such organizations. We seek to develop an appropriate methodology to evaluate the importance of each terrorist to the effectiveness of the network as a whole, and identify an optimal set of key terrorists that we recommend should be targeted in order to debilitate the network.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.



### Prerequisites

The required environment for running the code and reproducing the results is a computer with a valid installation of Python 3. More specifically, [Python 3.6](https://docs.python.org/3.6/) is used.

Besides that (and the built-in Python libraries), the following packages are used and have to be installed:

* [NumPy 1.13.3](http://www.numpy.org). `pip3 install --user numpy==1.13.3`
* [Matplotlib 2.0.2](https://matplotlib.org). `pip3 install --user matplotlib==2.0.2`

### Installing

To install the previously mentioned libraries a requirements.txt file is provided. The user is free to use it for installing the previously mentioned libraries.  


## Project Structure

The project has the following folder (and file) structure:

* `data/`. Directory containing original dataset from LINQS. [online] Linqs.soe.ucsc.edu. Available at: https://linqs.soe.ucsc.edu/node/236 [Accessed 11 Jan. 2019].

* `project/`. Folder containing the actual code files for the project:
    * `gephi/` Folder containing gephi files for visualization and exploration of the network.
    * `images/` Folder containing different images that are generated when running the different notebooks.
    * `fragmentation measures.py` Contains functions to compute fragmentation measures on the provided network.
    * `optimization_algorithms.py` Contains both optimization algorithms for fragmentation and information flow as well as the necessary functions to compute the respectives objective values. 
    * `data_exploration_functions.py` Contains several functions used for the import and parse of the data, creation of the network structure or identification of largest component among others.
    * `fragmentation.ipynb` Notebook containing initial data exploration as well as optimization task and results on the fragmentation problem. The provided notebook is already executed and shows the desired results.
    * `information_flow.ipynb` Notebook containing the data exploration and optimization task and results on the information diffusion problem. The provided notebook is already executed and shows the desired results. A new execution can take around 15 to 20 minutes. 
    * `adjacency.npy` Numpy file containing the structure of the adjacency matrix of the original network. Can be used to avoid creating it from scratch if a new execution of any of the two notebooks wants to be done. 

## Authors

* **Abrate, Marco Pietro** - 
* **Bolón Brun, Natalie** - 
* **Kakavandy, Shahow** - 
* **Park, Jangwon** - 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details




