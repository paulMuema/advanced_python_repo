# This code demonstrates a simple multi-threading scenario where multiple agents are used in performing a task
import threading
import time
import random

# Shared resource
shared_resource = 0
resource_lock = threading.Lock()

class Agent(threading.Thread):
    def __init__(self, name, task):
        super().__init__()
        self.name = name
        self.task = task

    def run(self):
        global shared_resource
        for _ in range(5):  # Each agent performs its task 5 times
            time.sleep(random.uniform(0.5, 1.5))  # Simulate work delay
            with resource_lock:  # Ensure safe access to shared resource
                print(f"{self.name} is performing task: {self.task}")
                shared_resource += 1
                print(f"{self.name} updated shared resource to {shared_resource}")

# Create multiple agents
agent1 = Agent("Agent 1", "Collect Data")
agent2 = Agent("Agent 2", "Process Data")
agent3 = Agent("Agent 3", "Analyze Data")

# Start agents
agent1.start()
agent2.start()
agent3.start()

# Wait for all agents to complete
agent1.join()
agent2.join()
agent3.join()

print(f"Final value of shared resource: {shared_resource}")