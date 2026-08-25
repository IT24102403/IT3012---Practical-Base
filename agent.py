# agent.py

from collections import deque
import heapq
from random import random 

class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        # If standing directly on food, or just wander / move towards coordinates
        pos = percept['agent_pos']
        # Simple heuristic or fallback random sweep
        return random.choice(self.actions_pool)

class SearchAgent:

    def __init__(self):
        # Setting up for Step 1.3
        self.plan = []
        self.active_algo = 'BFS'

    def get_successors(self, state, percept):
        """Helper function to find valid adjacent states."""
        x, y = state
        width, height = percept.get('grid_size', (10, 10))
        walls = set(percept.get('walls', []))
        successors = []
        
        # Possible actions and resulting coordinates
        moves = {
            'Up': (x, y + 1), 
            'Down': (x, y - 1), 
            'Left': (x - 1, y), 
            'Right': (x + 1, y)
        }
        
        for action, (nx, ny) in moves.items():
            # Check grid boundaries and avoid walls
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in walls:
                successors.append((action, (nx, ny)))
                
        return successors

    def bfs_search(self, start, goal, percept):
        """Breadth-First search using a FIFO queue."""
        # Queue stores tuples of (current_state, path_to_reach_state)
        fronttier = deque([(start, [])])
        reached = {start}

        while frontier:
            state, path = frontier.popleft()

            if state == goal:
                return path

            for action, next_state in self.get_successors(state, percept):
                if next_state not in reached:
                    reached.add(next_state)
                    frontier.append((next_state, path + [action]))

        return []

    def dfs_search(self, start, goal, percept):
        """Depth-First Search using a LIFO stack."""
        # Stack stores tuples of (current_state, path_to_reach_state)
        frontier = [(start, [])] 
        reached = set()

        while frontier:
            state, path = frontier.pop()

            if state == goal:
                return path

            if state not in reached:
                reached.add(state)
                for action, next_state in self.get_successors(state, percept):
                    frontier.append((next_state, path + [action]))
                    
        return []


    def ucs_search(self, start, goal, percept):
        """Uniform-Cost Search using a Priority Queue."""
        # Priority Queue stores tuples of (cost, current_state, path_to_reach_state)
        frontier = [(0, start, [])] 
        reached = set()

        while frontier:
            cost, state, path = heapq.heappop(frontier)

            if state == goal:
                return path

            if state not in reached:
                reached.add(state)
                for action, next_state in self.get_successors(state, percept):
                    # In an unweighted grid, every step costs exactly 1
                    heapq.heappush(frontier, (cost + 1, next_state, path + [action]))
                    
        return []

    def send_and_act(self, percept):
        """Executes offline planning and returns the next action."""

        # 1. & 2. Check if self.plan is empty
        if not self.plan:
            all_food = percept.get('all_food', [])

            if not all_food:
                return "Stay" # No food left on the map

            # 3. Find the closest food pallet using Manhattan distance
            closest_food = min(all_food, key=lambda f:abs(f[0] - self.agent_pos[0]) + abs(f[1] - self.agent_pos[1]))

            # Execute the search method matching self.active_algo
            if self.active_algo == 'BFS':
                self.plan = self.bfs_search(self.agent_pos, closest_food, percept)
            elif self.active_algo == 'DFS':
                self.plan = self.dfs_search(self.agent_pos, closest_food, percept)
            elif self.active_algo == 'UCS':
                self.plan = self.ucs_search(self.agent_pos, closest_food, percept)
            
            # Add a 'Suck' action at the end to eat the food when we arrive
            if self.plan:
                self.plan.append("Suck")

        # 4. Return the first action from the plan
        if self.plan:
            action = self.plan.pop(0)
            
            # Update our internal position tracker if the action is a movement
            if action == 'Up': 
                self.agent_pos = (self.agent_pos[0], self.agent_pos[1] + 1)
            elif action == 'Down': 
                self.agent_pos = (self.agent_pos[0], self.agent_pos[1] - 1)
            elif action == 'Left': 
                self.agent_pos = (self.agent_pos[0] - 1, self.agent_pos[1])
            elif action == 'Right': 
                self.agent_pos = (self.agent_pos[0] + 1, self.agent_pos[1])
            
            return action
            
        return "Stay"