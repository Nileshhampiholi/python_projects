# Localization Challenge

## Pre-challenge questions
1. How does accuracy in localization contribute to a successful autonomous vehicle?

   In self-driving cars knowing the location precisely and accurately is very important for successful navigation through the environment. The location is usually obtained through GPS but it has an accuracy of 1 to 10 meters. This error is too important and can potentially be fatal for the passengers or the environment of the autonomous vehicle. As this information is used to perform path planning, motion planning, and control for the vehicle.   

   For example with an error in GPS of 5 meters, a faulty trajectory would be generated leading the vehicle into a collision. Hence is it very important to accurately localize the vehicle with respect to the surroundings. 

   

2. Can we rely on a single sensor for localization? If not, please explain why.

   No, a single sensor cannot provide all the required data for localization and they are prone to noisy data thus multiple sensors are used. 

   For example, GPS can provide location and velocity, LIDAR can provide a visual environment of surroundings and distance to obstacles, and RADAR can provide relative velocities and distance to obstacles at a distance of around 250 to 300 meters. All this information can be used to localize the vehicle. 

   Also, sensors a prone to noisy and faulty data thus it is always advisable to use multiple sensors. Usually, redundant sensors providing the same information are used, and the mean of the sensor reading is used. Using redundant sensors makes the information more reliable as 





## Transform data to base coordinate frame

### GPS

Transform latitude(lat) , longitude(long), and altitude(alti) data into x,y,z positions using 1st values of lat, long and ati.  Transform the x,y,z positions to the base link coordinate frame using the relation provided in the "calib.yaml" file.  

### Odom

It is in the base coordinate system.

### IMU 

Read the data and rotate the velocities to match the base coordinate frame using the transformation provided in "calib.yaml"

## Kalman Filter

To keep the model simpler use a Linear Kalman filter with 4 states x, y, x', and y'. That is position in x,y coordinates, and linear velocities.  

+ Initial state  x_0 = [0.1, 0.1, 0.5, 0.5]
+ Initial Covariance = zeros(4,4)


### System Model 

Using the equation of motion 

+ x_1 = x_0 + t * v_0 + 0.5 a * t * t

+ v_1 = v_0 + a*t

![image](https://user-images.githubusercontent.com/19320161/192251669-fa6a553b-3a57-4471-a954-ba92e8f29e23.png)  

![image](https://user-images.githubusercontent.com/19320161/192251838-47ee0c6d-a952-42bd-a51f-dc71a54acac7.png)



### Predict 
![image](https://user-images.githubusercontent.com/19320161/192249897-131f1170-34b1-4a0a-b1d4-eb3c405411c6.png)  

![image](https://user-images.githubusercontent.com/19320161/192249966-20cb474f-0c7a-4189-b987-7452c7bf9152.png)  

### Update 
![image](https://github.com/Nileshhampiholi/Localization-Challenge/blob/main/plots/image-20220925155754167.png)

## Time synchronization

GPS = 5 Hz =   0.2s/cycle

ODOM= 10 Hz = 0.1 s/cycle

IMU = 143Hz = 0.007 s/cycle

The sensors are updated accordingly 

To keep it easy running LKF at a fixed interval of 0.1 second 

## Plots 

### Tracking on GPS 

![Figure_1](https://github.com/Nileshhampiholi/Localization-Challenge/blob/main/plots/Figure_1.png)


zoomed: 

![Figure_2](https://github.com/Nileshhampiholi/Localization-Challenge/blob/main/plots/Figure_2.png)



![Figure_3](https://github.com/Nileshhampiholi/Localization-Challenge/blob/main/plots/Figure_3.png)



![Figure_4](https://github.com/Nileshhampiholi/Localization-Challenge/blob/main/plots/Figure_4.png)



### Using all 2 sensors tracking with odometry as true trajectory. 

![Figure_5](https://github.com/Nileshhampiholi/Localization-Challenge/blob/main/plots/Figure_5.png)

![Figure_6](https://github.com/Nileshhampiholi/Localization-Challenge/blob/main/plots/Figure_6.png)

![error_all_sensors](https://github.com/Nileshhampiholi/Localization-Challenge/blob/main/plots/error_all_sensors.png)



## Post-Challenge Questions

1. Please provide the reasoning behind the filter you selected. Are there some other
    filters as well, which could have been selected?
    
    Since the task is to estimate only the x and y positions. The system dynamic can be modeled as a linear system of equations thus  I choose to implement the Linear Kalman filter. As it is easy to implement and solve the required problem.
    
    Alternately Extended Kalman filter, unscented Kalman filter, and particle filter could also be used to solve the task. But they are computationally expensive and complex to model.



## References 

1. https://stackoverflow.com/questions/11578636/acceleration-from-devices-coordinate-system-into-absolute-coordinate-system
2. https://mediatum.ub.tum.de/doc/1285843/document.pdf
3. https://medium.com/@CivilMaps/fusing-gps-and-imu-for-fun-and-sbets-5ab87ddec3d3
4. https://medium.com/@CivilMaps/fusing-gps-and-imu-for-fun-and-sbets-5ab87ddec3d3
5. https://medium.com/@CivilMaps/fusing-gps-and-imu-for-fun-and-sbets-5ab87ddec3d3
6. https://towardsdatascience.com/kalman-filter-intuition-and-discrete-case-derivation-2188f789ec3a
7. https://towardsdatascience.com/kalman-filter-an-algorithm-for-making-sense-from-the-insights-of-various-sensors-fused-together-ddf67597f35e
8. https://automaticaddison.com/extended-kalman-filter-ekf-with-python-code-example/
9. https://automaticaddison.com/how-to-derive-the-state-space-model-for-a-mobile-robot/
10. https://automaticaddison.com/how-to-derive-the-state-space-model-for-a-mobile-robot/
11. https://automaticaddison.com/extended-kalman-filter-ekf-with-python-code-example/
12. https://github.com/karanchawla/GPS_IMU_Kalman_Filter/tree/master/src
13. https://github.com/rsasaki0109/kalman_filter_localization
