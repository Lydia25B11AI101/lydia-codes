"""
Program Title: 2D-Tree (K-Dimensional Tree for 2D Points)
Author: Lydia S. Makiwa
Date: June 2, 2026

Description:
Implements a 2-Dimensional spatial-partitioning Tree (K-D Tree) in Python. 
It supports building the tree from a list of coordinates, spatial search queries,
and finding the Nearest Neighbor to a target point. Crucial for KNN classifiers in AIML.
"""

import math

class Node:
    def __init__(self, point, left=None, right=None):
        self.point = point  # Coordinates (x, y)
        self.left = left
        self.right = right

class KDTree2D:
    def __init__(self, points):
        self.root = self._build_tree(points, depth=0)
        
    def _build_tree(self, points, depth):
        if not points:
            return None
            
        # Determine current split axis (0 for x, 1 for y)
        axis = depth % 2
        
        # Sort points by axis and find median
        points.sort(key=lambda x: x[axis])
        median_idx = len(points) // 2
        
        return Node(
            point=points[median_idx],
            left=self._build_tree(points[:median_idx], depth + 1),
            right=self._build_tree(points[median_idx + 1:], depth + 1)
        )

    def nearest_neighbor(self, target):
        """
        Public method to find the nearest neighbor to a target point.
        """
        best_node = None
        best_dist = float('inf')
        
        def search(node, depth):
            nonlocal best_node, best_dist
            if node is None:
                return
                
            axis = depth % 2
            
            # Calculate distance between current node point and target
            dist = math.dist(node.point, target)
            if dist < best_dist:
                best_dist = dist
                best_node = node
                
            # Determine which subtree to search first
            if target[axis] < node.point[axis]:
                next_branch = node.left
                opposite_branch = node.right
            else:
                next_branch = node.right
                opposite_branch = node.left
                
            search(next_branch, depth + 1)
            
            # Check if we need to search the opposite subtree
            # (i.e. does the hyper-sphere around target cross the splitting hyper-plane?)
            if abs(target[axis] - node.point[axis]) < best_dist:
                search(opposite_branch, depth + 1)
                
        search(self.root, 0)
        return best_node.point, best_dist

# --- Working Demo ---
if __name__ == "__main__":
    print("--- 2D K-Dimensional Tree Spatial Search ---")
    
    # Dataset representing 2D spatial points (X, Y)
    spatial_points = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
    print(f"Coordinates Dataset: {spatial_points}")
    
    # Build KD-Tree
    tree = KDTree2D(spatial_points)
    
    # Define query point
    query = (9, 2)
    print(f"\nQuery Point: {query}")
    
    # Find nearest neighbor
    neighbor, distance = tree.nearest_neighbor(query)
    print(f"Nearest Neighbor Found: {neighbor}")
    print(f"Calculated Euclidean Distance: {distance:.4f}")
    
    # Check mathematically
    raw_distances = {pt: round(math.dist(pt, query), 4) for pt in spatial_points}
    print(f"\nLinear Search Verification:")
    for pt, dist in raw_distances.items():
        print(f"  Distance to {pt}: {dist}")