from scripts.GPS import GPS
from scripts.Odometry import Odometry
from scripts.IMU import IMU
from scripts.Visualization import Visualization
from scripts.KalmanFilter import KalmanFilter
import numpy as np
import time

if __name__ == "__main__":

    # Set update interval for sensors
    TIME_INTERVAL = 0.1
    GPS_INTERVAL = 0.2  # 5Hz
    ODOM_INTERVAL = 0.1  # 10Hz
    IMU_INTERVAL = 0.007  # 143Hz

    # Initialise sensors the 1st value is automatically initialized
    gps_sensor = GPS()
    odometry = Odometry()
    imu = IMU()

    # Initialise kalman filter this initialises the state and covariance matrix
    kalman_filter = KalmanFilter()

    # Initialise the visualisation
    viz = Visualization

    # Initialise variables to store the trajectory and error
    x, y = [], []
    x_gps, y_gps = [], []
    err = []
    x_est, y_est = [], []

    # select sensors to use
    use_gps = True
    use_odom = True
    use_imu = True

    # break condition
    continue_loop = True

    # start timers for sensors
    print("Starting Estimation")
    start_time = time.time()
    gps_stat_time = time.time()
    odom_start_time = time.time()
    imu_start_time = time.time()

    # Loops until sensors fail
    while True:
        # try:

        # run kalman filter every 0.1 s
        if time.time() - start_time >= TIME_INTERVAL:
            # store trajectory for plotting
            x_gps.append(gps_sensor.latitude)
            y_gps.append(gps_sensor.longitude)
            x.append(odometry.pose[0])
            y.append(odometry.pose[1])

            # Run filter
            est = kalman_filter.kalman_filter(gps=gps_sensor, use_gps=use_gps,
                                              odom=odometry, use_odom=use_odom,
                                              imu=imu, use_imu=use_imu,
                                              time_interval=TIME_INTERVAL)
            # print([gps_sensor.latitude, gps_sensor.longitude], est, odometry.pose[0:2])

            # store estimates
            x_est.append(est[0])
            y_est.append(est[1])

            # Compute RMSE
            err.append(np.sqrt((gps_sensor.latitude - est[0]) ** 2 + (gps_sensor.longitude - est[1]) ** 2))
            # err.append(np.sqrt((odometry.pose[0] - est[0]) ** 2 + (odometry.pose[1] - est[1]) ** 2))

            # set use sensors to false until they are updated
            use_gps = False
            use_odom = False
            use_imu = False
            start_time = time.time()

        # Update gps very 0.2s
        if time.time() - gps_stat_time > GPS_INTERVAL:
            continue_loop = gps_sensor.update_data()
            # check if sensor fails
            if continue_loop:
                use_gps = True
            gps_stat_time = time.time()

        """
        # Update odom very 0.1s
        if time.time() - odom_start_time >= ODOM_INTERVAL:

            continue_loop = odometry.update_data()
            if continue_loop:
                use_odom = True
            odom_start_time = time.time()

        # update IMU every 0.007s
        if time.time() - imu_start_time >= IMU_INTERVAL:
            continue_loop = imu.update_data()
            if continue_loop:
                use_imu = True
            imu_start_time = time.time()
        """
        if not continue_loop:
            break
    # except Exception as e:
    #     print(e)
    #     break

    # Plot trajectory and error
    viz.plot_trajectory(x=None, y=None, x_est=x_est, y_est=y_est, x_gps=x_gps, y_gps=y_gps, sav_fig=False)
    viz.plot_error(np.linspace(0, len(x), len(x), dtype=np.float64) * TIME_INTERVAL, err, save_fig=False)
