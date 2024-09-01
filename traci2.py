import os
import optparse
import traci
import csv
import logging
import sys

def run():
    step = 0
    departure_times = {}
    arrival_times = {}

    try:
        with open("simulation_output2.csv", "w", newline='') as output_file:
            csv_writer = csv.writer(output_file)
            csv_writer.writerow(['Vehicle ID', 'Traveled Time'])

            while traci.simulation.getMinExpectedNumber() > 0:
                traci.simulationStep()
                for vehicle_id in traci.vehicle.getIDList():
                    if vehicle_id not in departure_times:
                        departure_times[vehicle_id] = traci.vehicle.getDeparture(vehicle_id)
                    # if vehicle_id not in arrival_times:
                    arrival_times[vehicle_id] = traci.simulation.getTime()

                step += 1

            for vehicle_id in departure_times:
                traveled_time = arrival_times[vehicle_id]-departure_times[vehicle_id]  
                csv_writer.writerow([vehicle_id, traveled_time])

    except Exception as e:
        logging.error(f"Error in simulation run: {e}")

    finally:
        traci.close()

def main():
    # Parse command-line options
    parser = optparse.OptionParser()
    parser.add_option("--nogui", action="store_true", default=False, help="Run the commandline version of SUMO")
    options, args = parser.parse_args()

    # Set SUMO_HOME environment variable
    sumo_home = os.getenv('SUMO_HOME', "C:\\Program Files (x86)\\Eclipse\\Sumo")
    print(sumo_home)
    # Construct SUMO command
    sumo_binary = "sumo-gui" if not options.nogui else "sumo"
    sumoBinary = "C:\\Program Files (x86)\\Eclipse\\Sumo\\bin\\sumo-gui.exe"
    sumoCmd = [sumoBinary, "-c", "jaipur.sumocfg"]

    try:
        # Start SUMO
        traci.start(sumoCmd)
        
        # Run simulation
        run()

    except traci.TraCIException as e:
        logging.error(f"TraCI error: {e}")
    except Exception as e:
        logging.error(f"Error starting SUMO or running simulation: {e}")

    finally:
        traci.close()

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stdout)

    # Run the main function
    main()
