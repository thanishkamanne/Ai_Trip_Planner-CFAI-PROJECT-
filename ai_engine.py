import heapq
import time
from collections import deque
from typing import List, Tuple, Dict, Any
import networkx as nx

class SearchAlgorithms:
    @staticmethod
    def bfs(graph: nx.Graph, start: str, goal: str) -> Dict[str, Any]:
        start_time = time.time()
        queue = deque([(start, [start])])
        visited = set()
        explored_count = 0
        
        while queue:
            (node, path) = queue.popleft()
            if node not in visited:
                explored_count += 1
                visited.add(node)
                if node == goal:
                    return SearchAlgorithms._format_result(graph, path, explored_count, time.time() - start_time, "BFS")
                for neighbor in graph.neighbors(node):
                    queue.append((neighbor, path + [neighbor]))
        return {}

    @staticmethod
    def dfs(graph: nx.Graph, start: str, goal: str) -> Dict[str, Any]:
        start_time = time.time()
        stack = [(start, [start])]
        visited = set()
        explored_count = 0
        
        while stack:
            (node, path) = stack.pop()
            if node not in visited:
                explored_count += 1
                visited.add(node)
                if node == goal:
                    return SearchAlgorithms._format_result(graph, path, explored_count, time.time() - start_time, "DFS")
                for neighbor in graph.neighbors(node):
                    stack.append((neighbor, path + [neighbor]))
        return {}

    @staticmethod
    def ucs(graph: nx.Graph, start: str, goal: str, weight_key: str = 'cost') -> Dict[str, Any]:
        start_time = time.time()
        pq = [(0, start, [start])]
        visited = {}
        explored_count = 0
        
        while pq:
            (cost, node, path) = heapq.heappop(pq)
            if node in visited and visited[node] <= cost:
                continue
            
            explored_count += 1
            visited[node] = cost
            
            if node == goal:
                return SearchAlgorithms._format_result(graph, path, explored_count, time.time() - start_time, "UCS")
                
            for neighbor in graph.neighbors(node):
                edge_data = graph.get_edge_data(node, neighbor)
                new_cost = cost + edge_data.get(weight_key, 1)
                heapq.heappush(pq, (new_cost, neighbor, path + [neighbor]))
        return {}

    @staticmethod
    def a_star(graph: nx.Graph, start: str, goal: str, weight_key: str = 'cost') -> Dict[str, Any]:
        start_time = time.time()
        
        def heuristic(n1, n2):
            # Simple heuristic: assume straight line distance is proportional to edge count or dummy value
            return 0 # For simplicity in this graph without coordinates

        pq = [(0, start, [start], 0)]
        visited = {}
        explored_count = 0
        
        while pq:
            (f, node, path, g) = heapq.heappop(pq)
            if node in visited and visited[node] <= g:
                continue
                
            explored_count += 1
            visited[node] = g
            
            if node == goal:
                return SearchAlgorithms._format_result(graph, path, explored_count, time.time() - start_time, "A*")
                
            for neighbor in graph.neighbors(node):
                edge_data = graph.get_edge_data(node, neighbor)
                new_g = g + edge_data.get(weight_key, 1)
                new_f = new_g + heuristic(neighbor, goal)
                heapq.heappush(pq, (new_f, neighbor, path + [neighbor], new_g))
        return {}

    @staticmethod
    def greedy(graph: nx.Graph, start: str, goal: str) -> Dict[str, Any]:
        start_time = time.time()
        # Heuristic based on direct distance if available, else 0
        pq = [(0, start, [start])]
        visited = set()
        explored_count = 0
        
        while pq:
            (h, node, path) = heapq.heappop(pq)
            if node in visited: continue
            
            explored_count += 1
            visited.add(node)
            
            if node == goal:
                return SearchAlgorithms._format_result(graph, path, explored_count, time.time() - start_time, "Greedy")
                
            for neighbor in graph.neighbors(node):
                # Using distance as heuristic
                edge_data = graph.get_edge_data(node, neighbor)
                h_val = edge_data.get('distance', 0)
                heapq.heappush(pq, (h_val, neighbor, path + [neighbor]))
        return {}

    @staticmethod
    def _format_result(graph, path, explored, exec_time, algo_name):
        total_dist = 0
        total_cost = 0
        total_time = 0
        max_risk = 0
        traffic_sum = 0
        
        for i in range(len(path) - 1):
            data = graph.get_edge_data(path[i], path[i+1])
            total_dist += data['distance']
            total_cost += data['cost']
            total_time += data['time']
            max_risk = max(max_risk, data['weather_risk'])
            traffic_sum += data['traffic']
            
        return {
            "path": path,
            "total_distance": round(total_dist, 2),
            "total_cost": round(total_cost, 2),
            "total_time": round(total_time, 2),
            "avg_traffic": round(traffic_sum / (len(path)-1), 2) if len(path) > 1 else 0,
            "max_risk": round(max_risk, 2),
            "algorithm": algo_name,
            "explored_nodes": explored,
            "execution_time": round(exec_time * 1000, 4)
        }
