import numpy as np

class KalmanFilter:
    def __init__(self, n_languages):
        self.state = np.array([1/n_languages] * n_languages)  # Assuming equal probability for each language
        self.covariance = np.eye(n_languages) * 0.01  # Assuming small uncertainty
        self.transition_matrix = np.eye(n_languages)
        self.observation_matrix = np.eye(n_languages)
        self.process_noise_covariance = np.eye(n_languages) * 0.001
        self.observation_noise_covariance = np.eye(n_languages) * 0.001
        self.n_languages = n_languages

    def predict(self):
        self.state = np.dot(self.transition_matrix, self.state)
        self.covariance = np.dot(np.dot(self.transition_matrix, self.covariance), self.transition_matrix.T) + self.process_noise_covariance

    def update(self, observation):
        innovation = observation - np.dot(self.observation_matrix, self.state)
        innovation_covariance = np.dot(np.dot(self.observation_matrix, self.covariance), self.observation_matrix.T) + self.observation_noise_covariance
        kalman_gain = np.dot(np.dot(self.covariance, self.observation_matrix.T), np.linalg.inv(innovation_covariance))
        self.state = self.state + np.dot(kalman_gain, innovation)
        self.covariance = np.dot((np.eye(self.state.shape[0]) - np.dot(kalman_gain, self.observation_matrix)), self.covariance)


"""
# Initial state estimate (probabilities for each language)
initial_state = np.array([0.25, 0.25, 0.25, 0.25])  # Assuming equal probability for each language
# Initial covariance matrix
initial_covariance = np.eye(4) * 0.01  # Assuming small uncertainty
# Transition matrix (identity matrix as we don't have a dynamic model for language probabilities)
transition_matrix = np.eye(4)
# Observation matrix (identity matrix as we directly observe the language)
observation_matrix = np.eye(4)
# Process noise covariance (assuming small process noise)
process_noise_covariance = np.eye(4) * 0.001
# Observation noise covariance (assuming small observation noise)
observation_noise_covariance = np.eye(4) * 0.001



# Initialize Kalman filter
kalman_filter = KalmanFilter(initial_state,initial_covariance, transition_matrix, observation_matrix, process_noise_covariance, observation_noise_covariance)

# Example observation for English language
observation = np.array([1, 0, 0, 0])  # English
# # Initialize Kalman filter
# kalman_filter = KalmanFilter(initial_state, initial_covariance, transition_matrix, observation_matrix, process_noise_covariance, observation_noise_covariance)

# # Example observation for English language
# observation = np.array([0, 1, 0, 0])  # English

# # Update the Kalman filter with the observation
# kalman_filter.update(observation)

# # After update, you can get the current state (language probabilities)
# current_language_probabilities = kalman_filter.state
"""
