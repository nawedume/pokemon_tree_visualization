# Pokemon Phylogenetic Tree Visualizatin

## About

A visualization of Pokemon genetic information.

This visualization is a Phylogenetic tree of Pokemon. It attempts to group Pokemon with similar "genetic traits" together, and allows a user to query for Pokemon data.

The tree was created by encoding the moves a Pokemon can learn into a binary vector and using that as its genetic sequence. Parent nodes between two Pokemon are created based off the similarity of their genetic codes. This is done using the unweighted pair group method with arithmetic mean (UPGMA).

Limitations:
- Only the first two generations of Pokemon were used.

## Screen shots

![](images/app.png?raw=true)
![](images/app-filter.png?raw=true)