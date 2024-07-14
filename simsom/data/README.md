A small network to test variations of SimSoM model. 
- The base network, `follower_network.gml` is a small version of the follower network described in [SimSoM main repo](https://github.com/osome-iu/SimSoM). Raw data link [here](https://github.com/osome-iu/SimSoM/tree/main/data)
- We make sure that this small network (~1k nodes) have an echo chamber structure (2 communities, roughly balanced size) and the following attributes that can be use for running the simulations: ["label", "party", "misinfo"]

# Network descriptions

## vary_network folder
- This folder contains networks created using varying levels of bad actors connectivity (gamma). The values are: GAMMAS=[0.0001, 0.001, 0.01, 0.1]
- The first index in the name is the gamma value used, e.g: `network_00.gml` use `GAMMAS[0] = 0.0001`

## network_baseline.gml (Baseline)
- A network without inauthentic (bad) actors  
- The same as `follower_network.gml`, except that nodes have additional attributes: ['bot', 'uid']

## follower_network.gml (Raw follower network)

- Filter out a subgraph containing nodes with partisanship info 
- k-core decomposition until ~ 1k nodes in core

- make sure the degree of humans is comparable with degree of bad actorss for the default gamma=0.01
    e.g: if degree of humans is 100, then degree of bad actorss should be ~100, which is only possible with 100/0.01 = 10k nodes
- make sure that there's enough humans in a category (e.g. lib or conservative) so bad actors targeting is possible 
    e.g: if gamma==0.01 & number of bad actors followers =10, there should be at least 10 nodes in each category

### Network stats 

Nodes that have partisanship info:  15056
Number of nodes in each party:  {'rep': 8216, 'dem': 6840}
Downsample nodes from one party, sampling 6840 nodes each..
Building friend network from sampled 13680 nodes...
57704 nodes and 9885871 edges initially(average number of friends: 171.3203764037155)
Target sample graph is much smaller than the actual graph (0.07), retaining only a random sample of 2000 nodes...
2000 nodes and 86157 edges after filtering
28-core has 1001 nodes, 76842 edges
28-core after edge-sampling has 1001 nodes, 30030 edges, and average number of friends 30.0