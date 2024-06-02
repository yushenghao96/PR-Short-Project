import numpy as np

class KalmanFilter:
    def __init__(self, n_languages):
        # initialize parameters of kalman filter
        self.state = np.array([1/n_languages] * n_languages)  # Assuming equal probability for each language
        self.covariance = np.eye(n_languages) * 0.01  # Assuming small uncertainty
        self.transition_matrix = np.eye(n_languages)
        self.observation_matrix = np.eye(n_languages)
        self.process_noise_covariance = np.eye(n_languages) * 0.001
        self.observation_noise_covariance = np.eye(n_languages) * 0.0008

        # Initialize and define parameters
        self.n_languages = n_languages
        self.prob_history = []
        self.cov_history = []
        self.n_languages = n_languages

    def predict(self):
        # calculate the new values of the predict box
        self.state = np.dot(self.transition_matrix, self.state)
        self.covariance = np.dot(np.dot(self.transition_matrix, self.covariance), self.transition_matrix.T) + self.process_noise_covariance

    def update(self, observation):
        # calculate the new values of the update box
        innovation = observation - np.dot(self.observation_matrix, self.state)
        innovation_covariance = np.dot(np.dot(self.observation_matrix, self.covariance), self.observation_matrix.T) + self.observation_noise_covariance
        kalman_gain = np.dot(np.dot(self.covariance, self.observation_matrix.T), np.linalg.inv(innovation_covariance))

        self.state = self.state + np.dot(kalman_gain, innovation)
        self.prob_history.append(self.state.tolist())
        self.covariance = np.dot((np.eye(self.state.shape[0]) - np.dot(kalman_gain, self.observation_matrix)), self.covariance)
        self.cov_history.append(self.covariance.tolist())

    def removeLastProb(self):
        # Remove last values in case of deleting letters
        self.prob_history = np.delete(self.prob_history, -1, 0).tolist()
        self.cov_history = np.delete(self.cov_history, -1, 0).tolist()
        if len(self.prob_history) == 0:
            self.state = np.array([1/self.n_languages] * self.n_languages)
            self.covariance = np.eye(self.n_languages) * 0.01
            self.prob_history = []
            self.cov_history = []
        else:
            self.state = self.prob_history[-1]
            self.covariance = self.cov_history[-1]
