from djitellopy import TelloSwarm

def mission(drone, idx): # (a single tello drone object, the index number of the drone in the swarm)
    try:
        drone.takeoff() # commands the drone to take off
        drone.move_up(50 + idx * 20)  # Starts 50cm up, adds 20cm * idx cm for each drone to avoid collins and add varation
        drone.rotate_clockwise(90) # rotates the drone 90 degrees clockwise
        drone.land() # lands drone
    except Exception as e:
        print(f"Error: {e}")

        try:
            drone.land()
        except:
            pass # Avoid crash if connection already lost
    finally:
        drone.end()

def run_swarm():
    DRONE_IPS = ["IP", "IP"] # Add IPs Here!!

    swarm = TelloSwarm.fromIps(DRONE_IPS)

    swarm.connect()

    # Each drone can run the mission function in parallel
    swarm.parallel(mission)

if __name__ == "__main__": # ensuring the file is only executed when the file is run as the main program
    run_swarm()