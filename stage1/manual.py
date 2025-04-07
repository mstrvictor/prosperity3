import math
from collections import defaultdict

def find_most_profitable_arbitrage(nodes, edges, start_node, max_trades=5):
    """
    Find the most profitable arbitrage opportunity starting and ending at a specific node with at most max_trades trades.
    
    Args:
        nodes: List of node names
        edges: List of tuples (from_node, to_node, exchange_rate)
        start_node: The node where the cycle must start and end
        max_trades: Maximum number of trades allowed (default: 5)
    
    Returns:
        tuple: (profit, path) where profit is the maximum profit multiplier and path is the sequence of nodes
    """
    # Ensure start_node is valid
    if start_node not in nodes:
        return 1.0, []
    
    # Create a rate lookup for efficient profit calculation
    rate_lookup = {}
    for u, v, rate in edges:
        rate_lookup[(u, v)] = rate
    
    # Convert to negative log for Bellman-Ford
    # We use negative log to find shortest path (maximize profit)
    log_edges = [(u, v, -math.log(rate)) for u, v, rate in edges]
    
    # Create adjacency list for efficient neighbor lookup
    graph = defaultdict(list)
    for u, v, weight in log_edges:
        graph[u].append((v, weight))
    
    # Function to calculate profit of a path
    def calculate_profit(path):
        profit = 1.0
        for i in range(len(path) - 1):
            from_node, to_node = path[i], path[i+1]
            profit *= rate_lookup.get((from_node, to_node), 0)
        return profit
    
    # Use a more exhaustive approach to find cycles
    best_profit = 1.0
    best_path = []
    
    # Run modified Bellman-Ford for each possible cycle length
    for cycle_length in range(2, max_trades + 2):  # +2 because we count start_node twice
        # Initialize distances for this iteration
        distances = {node: {0: float('inf')} for node in nodes}
        distances[start_node][0] = 0
        
        # Initialize predecessors for path reconstruction
        predecessors = {node: {0: None} for node in nodes}
        
        # Relax edges for each step in the path
        for step in range(1, cycle_length):
            for u in nodes:
                if step-1 not in distances[u]:
                    continue
                    
                for v, weight in graph[u]:
                    if step not in distances[v] or distances[u][step-1] + weight < distances[v].get(step, float('inf')):
                        distances[v][step] = distances[u][step-1] + weight
                        predecessors[v][step] = u
        
        # Check for paths back to start_node
        for step in range(1, cycle_length):
            if step in distances[start_node] and distances[start_node][step] < 0:
                # Reconstruct path
                path = [start_node]
                current = start_node
                current_step = step
                
                while current_step > 0:
                    current = predecessors[current][current_step]
                    path.insert(0, current)
                    current_step -= 1
                
                path.append(start_node)  # Complete the cycle
                
                # Calculate profit and update if better
                profit = calculate_profit(path)
                if profit > best_profit:
                    best_profit = profit
                    best_path = path
    
    # Use a second approach: k-length simple paths
    def dfs(node, path, visited, depth):
        nonlocal best_profit, best_path
        
        if depth == 0:
            if node == start_node and len(path) > 1:
                cycle_path = path + [start_node]
                profit = calculate_profit(cycle_path)
                if profit > best_profit:
                    best_profit = profit
                    best_path = cycle_path
            return
        
        visited.add(node)
        for neighbor, _ in graph[node]:
            if neighbor not in visited or neighbor == start_node:
                path.append(neighbor)
                if neighbor != start_node:
                    dfs(neighbor, path, visited, depth - 1)
                else:
                    dfs(neighbor, path, visited, 0)  # Force end if we reach start_node
                path.pop()
        visited.remove(node)
    
    # Start DFS from the start node
    dfs(start_node, [start_node], set(), max_trades)
    
    return best_profit, best_path

def format_result(profit, path):
    """Format the result for display"""
    if not path:
        return "No profitable arbitrage cycle found."
    
    result = f"Most profitable arbitrage cycle: {' -> '.join(path)}\n"
    result += f"Profit multiplier: {profit:.6f}x"
    return result

# Example usage
if __name__ == "__main__":
    # Example data
    nodes = ["SNOWBALLS", "PIZZAS", "NUGGETS", "SEASHELLS"]
    edges = [
        ("SNOWBALLS", "SNOWBALLS", 1.0),
        ("SNOWBALLS", "PIZZAS", 1.45),
        ("SNOWBALLS", "NUGGETS", 0.52),
        ("SNOWBALLS", "SEASHELLS", 0.72),
        ("PIZZAS", "SNOWBALLS", 0.7),
        ("PIZZAS", "PIZZAS", 1.0),
        ("PIZZAS", "NUGGETS", 0.31),
        ("PIZZAS", "SEASHELLS", 0.48),
        ("NUGGETS", "SNOWBALLS", 1.95),
        ("NUGGETS", "PIZZAS", 3.1),
        ("NUGGETS", "NUGGETS", 1.0),
        ("NUGGETS", "SEASHELLS", 1.49),
        ("SEASHELLS", "SNOWBALLS", 1.34),
        ("SEASHELLS", "PIZZAS", 1.98),
        ("SEASHELLS", "NUGGETS", 0.64),
        ("SEASHELLS", "SEASHELLS", 1.0),
    ]
    
    # Specify the start/end node
    start_node = "SEASHELLS"
    
    profit, path = find_most_profitable_arbitrage(nodes, edges, start_node, max_trades=5)
    print(format_result(profit, path))




# Most profitable arbitrage cycle: SEASHELLS -> SNOWBALLS -> NUGGETS -> PIZZAS -> SNOWBALLS -> SEASHELLS -> SEASHELLS
# Profit multiplier: 1.088680x