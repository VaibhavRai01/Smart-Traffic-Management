import traci
import numpy as np

# SUMO configuration
sumo_cmd = ["sumo-gui", "-c", "jaipur.sumocfg"]

# Traffic parameters
MAX_STEPS = 1000
CONGESTION_THRESHOLD = 10  # Threshold for determining congestion


# Function to monitor traffic and get current vehicle state
def get_vehicle_state(vehicle_id):
    position = traci.vehicle.getPosition(vehicle_id)
    speed = traci.vehicle.getSpeed(vehicle_id)
    route_edges = traci.vehicle.getRoute(vehicle_id)
    current_edge = traci.vehicle.getRoadID(vehicle_id)
    return position, speed, route_edges, current_edge


# Function to calculate the reward (negative of travel time)
def calculate_reward(start_time, end_time):
    return -(end_time - start_time)


# Function to check congestion on a given edge
def is_edge_congested(edge_id, threshold=CONGESTION_THRESHOLD):
    num_vehicles = traci.edge.getLastStepVehicleNumber(edge_id)
    return num_vehicles > threshold


# Function to get alternate routes avoiding congestion
def get_alternate_route(current_edge, destination_edge):
    new_route = traci.simulation.findRoute(current_edge, destination_edge).edges
    return new_route


# Start the SUMO simulation
traci.start(sumo_cmd)
step = 0
active_vehicles = set()  # Track active vehicles
vehicle_depart_times = {}  # Track vehicle departure times

# Main simulation loop
while traci.simulation.getMinExpectedNumber()>0:
    traci.simulationStep()  # Advance the simulation by one step
    step += 1

    # Get the list of all vehicles currently in the simulation
    all_vehicles = traci.vehicle.getIDList()

    for vehicle_id in all_vehicles:
        if vehicle_id not in active_vehicles:
            active_vehicles.add(vehicle_id)
            vehicle_depart_times[vehicle_id] = traci.simulation.getTime()
            # print(f"New vehicle detected: {vehicle_id}")

        # Get current state of the vehicle
        position, speed, route_edges, current_edge = get_vehicle_state(vehicle_id)
        # print(f"Step {step}: Vehicle {vehicle_id} at {current_edge} with speed {speed}")

        # Check if the current path is congested and find an alternate route
        if is_edge_congested(current_edge):
            print(f"Edge {current_edge} is congested, finding alternate route for vehicle {vehicle_id}...")
            destination_edge = route_edges[-1]
            new_route = get_alternate_route(current_edge, destination_edge)
            traci.vehicle.setRoute(vehicle_id, new_route)
            print(f"New route for {vehicle_id}: {new_route}")

        # Check if the vehicle has reached its final edge
        if vehicle_id not in traci.vehicle.getIDList():
            end_time = traci.simulation.getTime()
            travel_time = end_time - vehicle_depart_times[vehicle_id]
            reward = calculate_reward(vehicle_depart_times[vehicle_id], end_time)
            print(
                f"Vehicle {vehicle_id} has reached the destination or exited the network. Travel time: {travel_time}, Reward: {reward}")
            active_vehicles.remove(vehicle_id)

# Close the simulation
traci.close()
