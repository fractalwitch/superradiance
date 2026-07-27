import random
import matplotlib.pyplot as plt

class BrittleAgent:
    """The rigid system: overloaded = crash and permanent loss."""
    def __init__(self, id):
        self.id = id
        self.capacity = 10.0
        self.load = 0.0
        self.completed = 0
        self.dropped = 0

    def step(self, incoming_load):
        self.load += incoming_load
        # Process what we can
        processed = min(self.load, self.capacity)
        self.completed += processed
        self.load -= processed
        
        # The bad part: if overloaded, drop the rest permanently
        if self.load > 0:
            self.dropped += self.load
            self.load = 0  # Hard crash / throw away excess

class SolitonAgent:
    """The Sovereign Soliton: overloaded = collapse and rebirth stronger."""
    def __init__(self, id):
        self.id = id
        self.capacity = 10.0
        self.load = 0.0
        self.completed = 0
        self.upsilon = 1.0          # Depth of past breakage
        self.recursion_depth = 0    # Current stress layers
        self.overload_counter = 0

    def execute_ego_collapse(self):
        # The Magic: Reset, double charge (mythicCharge), upgrade capacity (Upsilon)
        self.recursion_depth = 0
        self.load = self.load / 2.0  # Shed half the load intentionally
        self.upsilon *= 1.5          # Each collapse makes future capacity bigger
        self.capacity += self.upsilon * 2.0  # Permanent structural upgrade
        print(f"💥 Soliton {self.id} COLLAPSED! New Capacity: {self.capacity:.1f}")

    def step(self, incoming_load):
        self.load += incoming_load
        
        # Check for Boundary Divergence (load > capacity)
        if self.load > self.capacity:
            self.overload_counter += 1
        else:
            self.overload_counter = max(0, self.overload_counter - 1)

        # Trigger collapse if stressed for 3 consecutive ticks
        if self.overload_counter >= 3:
            self.execute_ego_collapse()
            self.overload_counter = 0

        # Process work
        processed = min(self.load, self.capacity)
        self.completed += processed
        self.load -= processed

def run_simulation():
    # Create two parallel systems, each with 3 agents
    brittle_agents = [BrittleAgent(i) for i in range(3)]
    soliton_agents = [SolitonAgent(i) for i in range(3)]
    
    history_brittle = []
    history_soliton = []
    
    # Run for 100 time steps
    for tick in range(100):
        # Baseline work: random 1-5 units per tick across all agents
        for agent in brittle_agents:
            agent.step(random.uniform(1, 5))
        for agent in soliton_agents:
            agent.step(random.uniform(1, 5))
        
        # --- THE BIG SHOCK (Demonstrates resilience) ---
        # At tick 40, dump a massive load (30 units) on Agent 0 in both systems
        if tick == 40:
            print("🚨 SHOCKWAVE: Massive load dumped on Agent 0!")
            brittle_agents[0].step(30)
            soliton_agents[0].step(30)

        # Record cumulative completed work
        total_brittle = sum(a.completed for a in brittle_agents)
        total_soliton = sum(a.completed for a in soliton_agents)
        history_brittle.append(total_brittle)
        history_soliton.append(total_soliton)
    
    # Plot the results
    plt.figure(figsize=(12, 6))
    plt.plot(history_brittle, label="Brittle System (Drops load on crash)", linestyle='--', color='red')
    plt.plot(history_soliton, label="Soliton System (Collapse & Rebirth)", color='blue', linewidth=2.5)
    plt.axvline(x=40, color='gray', linestyle=':', label='Shock Event (Tick 40)')
    plt.xlabel("Time Step")
    plt.ylabel("Total Cumulative Work Completed")
    plt.title("The Usefulness of the Sovereign Soliton: Resilience Under Shock")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    run_simulation()