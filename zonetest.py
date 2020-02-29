depth = [1,1,1,2,2,2,5,5,5,4,4,4,3,3,3,2,2,2]
batch = 3
average = 0
count = 0
zonecount = 0
zone = []

for x in range(len(depth)):
    average = average + depth[x]
    count = count + 1
    if count == batch:      
        average = average/batch
        zone.append(average)
        zonecount = zonecount + 1
        count = 0
        average = 0
        
zonecount = int(len(depth)/batch)
for x in range(zonecount):
    print(zone[x])
center = zone.index(max(zone))
print("Longest range zone", center)
center_distance = zone[center]
print("Longest range distance", center_distance)

left_total = 0
right_total = 0
for x in range(0,center-1): # sum the left side
    left_total = left_total + zone[x]
left_average = left_total/(center-1)

for x in range(center+1,zonecount): # sum the right side
    right_total = right_total + zone[x]
right_average = right_total/(zonecount-center-1)

print("Left average", left_average)
print("Right average", right_average)
if left_average > right_average:
    furthest_side_dist = left_average
else:
    furthest_side_dist = right_average

steer = center + (center_distance-furthest_side_dist)*0.1
print("steer", steer)
