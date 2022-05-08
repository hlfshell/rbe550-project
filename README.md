# RBE 550 Final Project - Global + Local Planner for an Urban Environment Delivery Robot

<img src="videos/final.gif"/>

This is the final project for RBE550 - a group project wherein we created a simulated for a delivery robot. This robot would make deliveries to an fro a centraliezd grocery store for a given neighborhood. For this assingment, we created, from scratch, a virtual simulated urban environment with obstacles (static, such as trash cans, traffic cones, dumpsters, parked bikes) and dynamic obstacles (moving cars) with a set of predetermined addresses for delivery.

The robot would be given an address at random, and then utilize a global planner (which was aware of only street corners and delivery addresses) to create a city street plan of travel. For each node in this plan an additional local planner was utilized, which used the kinematic model of the robot to determine available movements and create a plan for the robot.

The robot would avoid obstacles within the road, and appropriately wait at sidewalks for cars passing through.

Note that the videos are of a higher quality and make it easy to see our tiny to-scale robot move about its path.

<img src="videos/final2.gif"/>