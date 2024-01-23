import json
import math

# TODO: account for arm relative to robot's inherent size and the slightly raised hight of the arm
# Note everything is in meters and degrees

# Init map
distance_to_angle_map = {}

#This calculates the shooting angle required to reach the goal
def calculate_angle(x0):
    yf = 2.05
    xf = 0 # uneccessary for this calculation
    y0 = 0.0 # This is the height of the arm from the ground
    vi = 10
    l = 0.635
    g = 9.8
    
    initial_angle = 180.0
    range_from_initial = 180.0 # we test from 180 degrees to 0 degrees
    increment = 0.0001 
    moe = 0.001

    for i in range(int(range_from_initial/increment)):
        # Trial 3 - Bailey
        # test_height = y0 + l * math.sin(math.radians(initial_angle + 40)) + vi * ((xf + x0 + l * math.cos(math.radians(initial_angle + 40))) / (vi * math.cos(math.radians(initial_angle)))) * math.sin(math.radians(initial_angle)) - 1 / 2 * g * ((xf + x0 + l * math.cos(math.radians(initial_angle + 40))) / (vi * math.cos(math.radians(initial_angle)))) ** 2

        # value = l * math.sin(initial_angle) + vi * math.sin(initial_angle) * ((xf - x0 - l * math.cos(initial_angle))/(vi * math.cos(initial_angle))) - 1/2 * g * ((xf - x0 - l * math.cos(initial_angle))/(vi * math.cos(initial_angle)))**2
        #
        # if (moe >= abs(yf - value)):
        #     return initial_angle
        #
        # initial_angle += increment

        # Trial 1 - Bailey + Don
        # test_height = math.tan(initial_angle) * (x0 + l * math.cos(math.radians(140 - initial_angle))) - 1/2 * g * ((x0 + l * math.cos(math.radians(140-initial_angle))) / (vi * math.cos(math.radians(initial_angle))))**2 + l * math.sin(math.radians(140-initial_angle))

        # Trial 2 - Don
        # test_height = math.tan(math.radians(140-initial_angle))*(-l*math.cos(math.radians(initial_angle))-x0) - 1/2*g*((-l*math.cos(math.radians(initial_angle))-x0)/(vi*math.cos(math.radians(140-initial_angle))))**2 + l*math.sin(initial_angle)

        # Trial 4 - Don
        test_height = math.tan(math.radians(140-initial_angle))*(l*math.cos(math.radians(initial_angle))+x0) - 1/2 * g * ((x0+l*math.cos(math.radians(initial_angle)))/(vi*math.cos(math.radians(140-initial_angle))))**2 + l * math.sin(math.radians(initial_angle)) + y0

        if (moe >= abs(yf - test_height)):
            print("distance: " + str(x0) + ", initial angle: " + str(initial_angle) + ", test height: " + str(test_height))
            return initial_angle

        initial_angle -= increment

    return -100000

def insert_to_hashmap():
    d_min = 0.90
    d_max = 7.20
    increment = 0.01

    d_current = d_min

    for i in range(int((d_max - d_min)/increment)):

        # We add 40 degrees here because this converts the shooting angle to the arm angle
        distance_to_angle_map[d_current] = calculate_angle(d_current)
        d_current += increment

insert_to_hashmap()
print("angle at 0 m distance: " + str(calculate_angle(0)))

# Specify the file path where you want to save the JSON file
json_file_path = "angles.json"

# Save the hashmap to the JSON file
with open(json_file_path, 'w') as json_file:
    json.dump(distance_to_angle_map, json_file)

print(f"The hashmap has been saved to {json_file_path}")