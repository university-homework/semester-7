import numpy as np
from typing import List, Callable


class Layer:
    def __init__(self, input_size: int, output_size: int, activation: Callable, activation_derivative: Callable):
        self.weights = np.random.uniform(-1, 1, (input_size, output_size))
        self.bias = np.random.uniform(-1, 1, (1, output_size))
        self.activation = activation
        self.activation_derivative = activation_derivative
        self.input = None
        self.output = None
        self.z = None

    def forward(self, x: np.ndarray) -> np.ndarray:
        self.input = x
        self.z = np.dot(x, self.weights) + self.bias
        self.output = self.activation(self.z)
        return self.output


class NeuralNetwork:
    def __init__(self, learning_rate: float = 0.5):
        self.layers: List[Layer] = []
        self.learning_rate = learning_rate

    def add_layer(self, layer: Layer):
        self.layers.append(layer)

    def forward(self, x: np.ndarray) -> np.ndarray:
        for layer in self.layers:
            x = layer.forward(x)
        return x

    def backward(self, x: np.ndarray, y: np.ndarray) -> float:
        # Forward pass to cache values
        output = self.forward(x)

        # Calculate initial error
        error = output - y
        total_error = np.mean(np.square(error))

        # Backward pass
        for i in reversed(range(len(self.layers))):
            layer = self.layers[i]

            if i == len(self.layers) - 1:  # Output layer
                delta = error * layer.activation_derivative(layer.output)
            else:  # Hidden layers
                next_layer = self.layers[i + 1]
                delta = np.dot(delta, next_layer.weights.T) * layer.activation_derivative(layer.output)

            # Update weights and biases
            if i == 0:
                input_data = x
            else:
                input_data = self.layers[i - 1].output

            layer.weights -= self.learning_rate * np.dot(input_data.T, delta)
            layer.bias -= self.learning_rate * np.sum(delta, axis=0, keepdims=True)

        return total_error


# Activation functions
def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1 / (1 + np.exp(-x))


def sigmoid_derivative(x: np.ndarray) -> np.ndarray:
    return x * (1 - x)


def tanh(x: np.ndarray) -> np.ndarray:
    return np.tanh(x)


def tanh_derivative(x: np.ndarray) -> np.ndarray:
    return 1 - np.square(x)


def relu(x: np.ndarray) -> np.ndarray:
    return np.maximum(0, x)


def relu_derivative(x: np.ndarray) -> np.ndarray:
    return (x > 0).astype(float)


# Example usage
def main():
    # Training data
    X = np.array([[0.1, 0.5, 0.2],
                  [0.8, 0.2, 0.9],
                  [0.3, 0.7, 0.1],
                  [0.9, 0.4, 0.6]])

    y = np.array([[0, 1],
                  [1, 0],
                  [0, 1],
                  [1, 0]])

    # Create network
    nn = NeuralNetwork(learning_rate=0.5)

    # Add layers
    nn.add_layer(Layer(input_size=3, output_size=4,
                       activation=tanh, activation_derivative=tanh_derivative))
    nn.add_layer(Layer(input_size=4, output_size=2,
                       activation=sigmoid, activation_derivative=sigmoid_derivative))

    print("До обучения:")
    for i, sample in enumerate(X):
        prediction = nn.forward(sample.reshape(1, -1))
        print(f"Вход: {sample} -> Выход: {prediction[0]}, Ожидалось: {y[i]}")

    # Training
    epochs = 1000
    for epoch in range(epochs):
        total_error = 0
        for i in range(len(X)):
            error = nn.backward(X[i:i + 1], y[i:i + 1])
            total_error += error

        if epoch % 100 == 0:
            print(f"Эпоха {epoch}, Средняя ошибка: {total_error / len(X):.6f}")

    print("\nПосле обучения:")
    for i, sample in enumerate(X):
        prediction = nn.forward(sample.reshape(1, -1))
        print(f"Вход: {sample} -> Выход: {prediction[0]}, Ожидалось: {y[i]}")

    # Test with new data
    print("\nТест на новых данных:")
    test_data = np.array([[0.2, 0.6, 0.3],
                          [0.7, 0.1, 0.8]])

    for sample in test_data:
        prediction = nn.forward(sample.reshape(1, -1))
        print(f"Тест: {sample} -> Предсказание: {prediction[0]}")


if __name__ == "__main__":
    main()
