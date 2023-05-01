import math


class KDTreeNode:
    def __init__(self, point, axis, left=None, right=None):
        self.point = point  # The k-dimensional point represented as a tuple or list
        self.axis = axis    # The axis (dimension) used to split the data at this node
        self.left = left    # The left child node, representing points less than the split value
        self.right = right  # The right child node, representing points greater than or equal to the split value

    def __str__(self):
        return f"KDTreeNode(point={self.point}, axis={self.axis})"

    def __repr__(self):
        return self.__str__()

def build_kd_tree(points, depth=0):
    if not points:
        return None
    k = len(points[0])  # Number of dimensions
    axis = depth % k    # Current splitting axis
    # Sort points and find the median
    points.sort(key=lambda x: x[axis])
    median = len(points) // 2
    # Create the current node and recursively build left and right subtrees
    node = KDTreeNode(point=points[median], axis=axis)
    node.left = build_kd_tree(points[:median], depth + 1)
    node.right = build_kd_tree(points[median + 1:], depth + 1)
    return node


def build_balanced_kd_tree(points, depth=0):
    if not points:
        return None
    k = len(points[0])  # Number of dimensions
    axis = depth % k    # Current splitting axis
    # Sort points and find the median
    points.sort(key=lambda x: x[axis])
    median = len(points) // 2
    # Create the current node and recursively build left and right subtrees
    node = KDTreeNode(point=points[median], axis=axis)
    node.left = build_balanced_kd_tree(points[:median], depth + 1)
    node.right = build_balanced_kd_tree(points[median + 1:], depth + 1)
    return node

def insert_kd_tree(node, point, depth=0):
    if node is None:
        k = len(point)
        axis = depth % k
        return KDTreeNode(point, axis)

    axis = node.axis
    if point[axis] < node.point[axis]:
        node.left = insert_kd_tree(node.left, point, depth + 1)
    else:
        node.right = insert_kd_tree(node.right, point, depth + 1)

    return node

def euclidean_distance(point1, point2):
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(point1, point2)]))

def nearest_neighbor_search(node, query_point, best=None, depth=0):
    if node is None:
        return best
    # Calculate the distance between the query point and the current node's point
    current_distance = euclidean_distance(query_point, node.point)
    # Update the best point if necessary
    if best is None or current_distance < euclidean_distance(query_point, best.point):
        best = node
    # Determine the splitting axis and the search order for child nodes
    axis = node.axis
    near, far = (node.left, node.right) if query_point[axis] < node.point[axis] else (node.right, node.left)
    # Recursively search the near subtree
    best = nearest_neighbor_search(near, query_point, best, depth + 1)
    # Check if the far subtree could contain a closer point
    if (node.point[axis] - query_point[axis]) ** 2 < euclidean_distance(query_point, best.point):
        best = nearest_neighbor_search(far, query_point, best, depth + 1)
    return best

def update_best_neighbors(best, current, k):
    current_distance, current_node = current
    best.sort(key=lambda x: x[0], reverse=True)
    if len(best) < k:
        best.append(current)
    elif current_distance < best[0][0]:
        best[0] = current
    return best

def k_nearest_neighbors_search(node, query_point, k, best=None, depth=0):
    if node is None:
        return best
    if best is None:
        best = []
    # Calculate the distance between the query point and the current node's point
    current_distance = euclidean_distance(query_point, node.point)
    # Update the best points if necessary
    best = update_best_neighbors(best, (current_distance, node), k)
    # Determine the splitting axis and the search order for child nodes
    axis = node.axis
    near, far = (node.left, node.right) if query_point[axis] < node.point[axis] else (node.right, node.left)
    # Recursively search the near subtree
    best = k_nearest_neighbors_search(near, query_point, k, best, depth + 1)
    # Check if the far subtree could contain a closer point
    if not best or (node.point[axis] - query_point[axis]) ** 2 < best[0][0]:
        best = k_nearest_neighbors_search(far, query_point, k, best, depth + 1)
    return best


def k_d_tree_example():
    # Example points in 2D space
    points = [(3, 6), (17, 15), (13, 15), (6, 12), (9, 1), (2, 7), (10, 19)]
    # Build an initial k-d tree
    root = None
    for point in points:
        root = insert_kd_tree(root, point)
    # Insert a new point into the k-d tree
    new_point = (5, 8)
    root = insert_kd_tree(root, new_point)
    # Build a balanced k-d tree
    rootA = build_balanced_kd_tree(points)
    # Query point
    query_point = (5, 10)
    # Search for the nearest neighbor
    nearest_neighbor = nearest_neighbor_search(rootA, query_point)
    print("Query point:", query_point)
    print("Nearest neighbor:", nearest_neighbor.point)
    # Quasi-real example
    weather_stations = [
        (1, 37.7749, -122.4194),  # San Francisco
        (2, 34.0522, -118.2437),  # Los Angeles
        (3, 40.7128, -74.0060),  # New York
        (4, 41.8781, -87.6298),  # Chicago
        (5, 29.7604, -95.3698),  # Houston
    ]
    weather_station_tree = build_balanced_kd_tree([station[1:] for station in weather_stations])
    query_point = (36.1699, -115.1398)
    k = 2
    nearest_neighbors = k_nearest_neighbors_search(weather_station_tree, query_point, k)
    # Extract the nearest neighbors as a list of station IDs, sorted by distance
    nearest_station_ids = []
    for distance, neighbor in sorted(nearest_neighbors):
        for station in weather_stations:
            if neighbor.point == station[1:]:
                nearest_station_ids.append(station[0])
                break
    print("Query point (Las Vegas):", query_point)
    print(f"{k} nearest weather stations:", nearest_station_ids)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    k_d_tree_example()
