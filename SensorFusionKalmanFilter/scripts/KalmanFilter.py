import numpy as np

# Assumed
ACCEL_STD = 0.5
INIT_POS_STD = 0
INIT_VEL_STD = 0.5


class KalmanFilter:

    def __init__(self):
        # is initialised
        self.is_initialized = False

        # covariance matrix
        self.covariance = np.zeros((4, 4), dtype=np.float)

        # state vector
        self.state = []

        # time_interval
        self.dt = 0.1

    def initialise(self, gps, time_interval):
        """
        Initialise the state vector and covariance matrix using GPS location.
        """
        self.dt = time_interval
        state = np.array([gps.latitude, gps.longitude, 0.5, 0.5])
        self.state = state

        self.covariance[0:2, 0:2] = gps.covariance[0:2, 0:2]
        self.covariance[2:4, 2:4] = np.diag([INIT_VEL_STD ** 2, INIT_VEL_STD ** 2])
        self.is_initialized = True

    def predict(self, dt):
        """
        Kalman Filter prediction step

        """
        transition_matrix = np.array([[1, 0, dt, 0], [0, 1, 0, dt], [0, 0, 1, 0], [0, 0, 0, 1]])
        Q = np.diag([ACCEL_STD ** 2, ACCEL_STD ** 2])
        L = np.array([[(0.5 * dt ** 2), 0], [0, (0.5 * dt * dt)], [dt, 0], [0, dt]])

        # update global state and covariance
        self.state = transition_matrix.dot(self.state)
        self.covariance = transition_matrix.dot(self.covariance).dot(transition_matrix.transpose()) + L.dot(Q).dot(
            L.transpose())

    def handle_gps(self, dt, gps):
        # get  predicted state
        state = np.array(self.state)

        # get measurement
        z = np.array([gps.latitude, gps.longitude])

        # convert the state at time t into predicted sensor observations at time t
        H = np.array([[1, 0, 0, 0],
                      [0, 1, 0, 0]])
        R = gps.covariance[0:2, 0:2]

        z_hat = H.dot(state.transpose()) + np.array([1, 2]) * 10 ** -2

        # innovation
        y = z - z_hat

        # innovation covariance
        S = H.dot(self.covariance).dot(H.transpose()) + R

        # kalman gain
        K = self.covariance.dot(H.transpose()).dot(np.linalg.inv(S))

        # update global states
        self.state = state + K.dot(y)
        self.covariance = (np.identity(4) - K.dot(H)).dot(self.covariance)

    def handle_odom(self, dt, odom):
        # get current state
        state = np.array(self.state)

        # get current measurement
        z = np.array([odom.pose[0], odom.pose[1]])

        # convert the state at time t into predicted sensor observations at time t
        H = np.array([[1, 0, 0, 0],
                      [0, 1, 0, 0]])
        R = odom.pose_covariance[0:2, 0:2]

        # adding noise
        z_hat = H.dot(state.transpose()) + np.array([1, 2]) * 10 ** -2

        # innovation
        y = z - z_hat

        # innovation covariance
        S = H.dot(self.covariance).dot(H.transpose()) + R

        # kalman gain
        K = self.covariance.dot(H.transpose()).dot(np.linalg.inv(S))

        # update states
        self.state = state + K.dot(y)
        self.covariance = (np.identity(4) - K.dot(H)).dot(self.covariance)

    def handle_imu(self, dt, imu):
        # get current state
        state = np.array(self.state)

        # get measurements
        z = np.array([imu.linear_velocity[0] * self.dt, imu.linear_velocity[1] * self.dt])

        # convert the state at time t into predicted sensor observations at time t
        H = np.array([[0, 0, 1, 0],
                      [0, 0, 0, 1]])
        R = imu.linear_velocity_covariance[0:2, 0:2]

        z_hat = H.dot(state.transpose()) + np.array([1, 2]) * 10 ** -5

        # innovation
        y = z - z_hat

        # innovation covariance
        S = H.dot(self.covariance).dot(H.transpose()) + R

        # kalman gain
        K = self.covariance.dot(H.transpose()).dot(np.linalg.inv(S))

        # update state
        self.state = state + K.dot(y)
        self.covariance = (np.identity(4) - K.dot(H)).dot(self.covariance)

    def kalman_filter(self, gps, use_gps: bool, odom, use_odom: bool, imu, use_imu: bool, time_interval):
        """
        run kalman filter prediction and update step depending if the sensors are updated.
        """
        if not self.is_initialized:
            self.initialise(gps, time_interval)

        else:
            # prediction step
            self.predict(self.dt)

            # if odometer is available use odometry
            if use_odom:
                self.handle_odom(dt=self.dt, odom=odom)

            # if gps is available use gps
            if use_gps:
                self.handle_gps(dt=self.dt, gps=gps)

            # use imu if available
            if use_imu:
                self.handle_imu(self.dt, imu)

        return self.state[0:2]
