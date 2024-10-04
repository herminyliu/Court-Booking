import json
import random
from datetime import datetime, timedelta


def generate_mouse_movement_tracklist(x_index):
    track_list = []

    # Generate number of records based on a normal distribution with mean 20 and standard deviation 3
    num_records = int(random.normalvariate(20, 3))

    # Generate mouse movement records
    x = 0
    y = 0
    t = 0
    for _ in range(num_records):
        x += random.randint(1, 3) * random.choice([-1, 1])  # Add a random change to x
        x = min(x, x_index)  # Ensure x doesn't exceed x_index
        y += random.choices([0, 1, -1], weights=[0.8, 0.1, 0.1])[0]  # Randomly adjust y
        y = max(-1, min(y, 1))  # Ensure y stays within bounds
        interval = int(random.normalvariate(18, 3))  # Generate time interval based on a normal distribution
        t += interval
        track_list.append({"x": x, "y": y, "type": "move", "t": t})

    # Adjust the last record to match x_index
    track_list[-1]["x"] = x_index

    return track_list


# Example usage
x_index = 108  # Change this value as needed
tracklist_data = generate_mouse_movement_tracklist(x_index)
print(json.dumps(tracklist_data, indent=2))
