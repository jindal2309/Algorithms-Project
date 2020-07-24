# Missionaries and Cannibals Problem [Report Link](https://github.com/jindal2309/AlgorithmProject/blob/master/AlgorithmProjectReport%20.pdf)
#### Gaurav Kumar Jindal(gj3bg), Sanchit Sinha (ss7mu)

The missionaries and cannibals problem is a popular problem in Algorithms and Artificial Intelligence. In the problem, three missionaries and three cannibals are
on the Left bank {L} of a river, along with a boat that can hold up to two people. We have to find a sequence which we should follow to transport missionaries and cannibals to Right bank {R} without ever leaving a group
of missionaries in one place outnumbered by the cannibals in that place (if they were, the cannibals will eat the missionaries). Also, we have to satisfy another constraint of having at least one person in the boat i.e. 1 ≤ capacity
of boat ≤ 2 as the boat cannot cross the river by itself with no people on board.

We have generalised this problem to M: number of missionaries, C: number of cannibals, K: boat capacity. To solve this problem we have formulated this problem into a graph where state is represented by simple tuple
<m,c,dir> where m is the number of missionaries on the left bank {L}, c is the number of cannibals on the left bank {L}, dir is the direction of boat having value 1 for left to right and 0 for right to left. Our aim is to reach a
state having value <0,0,0> which means we have everyone on left bank crossed the river and boat is also at the right bank. We have solved this problem by using breadth first search (BFS) and depth first search (DFS).
The time complexity of BFS and DFS is the same that is O(V+E) where V and E are the vertex and edges of the graph. However, BFS always returns the shortest path.
