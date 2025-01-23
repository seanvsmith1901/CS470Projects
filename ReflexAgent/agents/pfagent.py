import math

import numpy as np

from .baseagent import Agent

class PFAgent(Agent):
    def __init__(self):
        super().__init__()

    def act(self, robot_pos, goal_pos, dist_sensors):
        # TODO: implement potential fields
        trajectory = np.zeros(2)
        dx = (goal_pos[0] - robot_pos[0])
        dy = (goal_pos[1] - robot_pos[1])
        # agith SO
        # now I gotta figure out how the fetch to implement the rest of this fetcher
        # and I gotta start digging into the distance sensors
        # but here is my thought
        # if any of them are too close
        # we label them with a bad
        # where the size of the vector is proportional to how close it is

        attractive_strength = np.linalg.norm(np.array(goal_pos) - np.array(robot_pos))
        dx += attractive_strength * (goal_pos[0] - robot_pos[0])
        dy += attractive_strength * (goal_pos[1] - robot_pos[1])
        alpha_constant = 1
        radius = 30


        if (abs(dx) > 1 or (abs(dy) > 1)):


            inc = 2.0 * math.pi / 16 # literally the angle of the current position sensor
            theta = 0.0
            offset = robot_pos[2] * math.pi / 100

            threshold = 15  # how far something has to be in order to blow up my sensors
            for i in range(0, 16):
                if (dist_sensors[i] < threshold):
                    repulsion_strength = max(0, radius - dist_sensors[i]) * 0.5
                    #if dist_sensors[i] < radius:
                        #dx += np.sign(math.cos(theta + offset)) * 100000
                        #dy += np.sign(math.sin(theta + offset)) * 100000
                    #else:
                    print("I have an obstacle at angle " + str(theta + offset))
                    # if we have something that is upsetting (like we have an angle)
                    distance = dist_sensors[i]
                    print("here is how far away the fetcher is" + str(distance))
                    dx += -(distance - radius) * math.cos(theta + offset) * repulsion_strength
                    dy += -(distance - radius) * math.sin(theta + offset) * repulsion_strength
                theta = inc + theta
                # kind of a dumb way to do it, but it might make more sense if I dive into it further

        # final thing - adjust the final trajectory as needed
        trajectory[0] = dx
        trajectory[1] = dy

        trajectory_norm = np.linalg.norm(trajectory)
        if trajectory_norm != 0:
            trajectory = trajectory / trajectory_norm

        return trajectory
