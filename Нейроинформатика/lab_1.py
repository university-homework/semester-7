import random
from typing import List, Tuple, Dict
import numpy as np


class DigitRecognizer:
    def __init__(self, num_digits: int = 10, pattern_size: int = 15):
        self.num_digits = num_digits
        self.pattern_size = pattern_size
        self.weights = np.zeros((num_digits, pattern_size))
        self.biases = np.full(num_digits, 7.0)

    def train(self, training_data: List[List[str]], iterations: int = 10000):
        """Обучение модели на тренировочных данных"""
        for _ in range(iterations):
            # Выбираем случайную цифру для обучения
            target_digit = random.randint(0, self.num_digits - 1)
            target_pattern = training_data[target_digit]

            for current_digit in range(self.num_digits):
                prediction = self._predict_single(target_pattern, current_digit)

                if current_digit == target_digit:
                    if not prediction:
                        self._adjust_weights(target_pattern, current_digit, increase=True)
                else:
                    if prediction:
                        self._adjust_weights(target_pattern, current_digit, increase=False)

    def _predict_single(self, pattern: List[str], digit: int) -> bool:
        """Предсказание для одного класса цифр"""
        net = sum(int(pattern[i]) * self.weights[digit][i] for i in range(self.pattern_size))
        return net >= self.biases[digit]

    def _adjust_weights(self, pattern: List[str], digit: int, increase: bool):
        """Корректировка весов"""
        for i in range(self.pattern_size):
            if int(pattern[i]) == 1:
                if increase:
                    self.weights[digit][i] += 1
                else:
                    self.weights[digit][i] -= 1

    def recognize(self, pattern: List[str], confidence_threshold: float = 3.0) -> str:
        """Распознавание цифры с проверкой уверенности"""
        scores = self._calculate_scores(pattern)
        best_digit, best_score = self._get_best_match(scores)

        if best_score < confidence_threshold:
            return f"Искажённая или неопознанная цифра. Вероятно: {best_digit} (уверенность: {best_score:.1f})"
        return f"Я думаю, что это цифра: {best_digit} (уверенность: {best_score:.1f})"

    def _calculate_scores(self, pattern: List[str]) -> List[float]:
        """Вычисление скоринга для всех цифр"""
        return [
            sum(int(pattern[i]) * self.weights[digit][i] for i in range(self.pattern_size))
            - self.biases[digit]
            for digit in range(self.num_digits)
        ]

    def _get_best_match(self, scores: List[float]) -> Tuple[int, float]:
        """Нахождение лучшего совпадения"""
        best_score = max(scores)
        best_digit = scores.index(best_score)
        return best_digit, best_score

    def evaluate(self, test_cases: Dict[str, str]) -> None:
        """Оценка модели на тестовых данных"""
        print("Результаты тестирования:")
        print("-" * 50)

        for description, pattern_str in test_cases.items():
            pattern = list(pattern_str)
            result = self.recognize(pattern)
            print(f"{description:15} ({pattern_str}): {result}")

    def interactive_mode(self):
        """Интерактивный режим для пользовательского ввода"""
        print("\n" + "=" * 50)
        print("ИНТЕРАКТИВНЫЙ РЕЖИМ РАСПОЗНАВАНИЯ")
        print("=" * 50)

        while True:
            print("\nВведите 15 цифр 0 или 1 (пример: 111100111001111)")
            print("Или введите 'quit' для выхода:")

            user_input = input().strip().lower()

            if user_input == 'quit':
                print("Выход из программы.")
                break

            if len(user_input) != 15 or any(c not in '01' for c in user_input):
                print("Ошибка: ввод должен содержать ровно 15 символов (только 0 и 1)")
                continue

            result = self.recognize(list(user_input))
            print(f"Результат: {result}")


class DigitData:
    """Класс для хранения тренировочных данных"""

    @staticmethod
    def get_training_data() -> List[List[str]]:
        return [
            list('111101101101111'),  # 0
            list('001001001001001'),  # 1
            list('111001111100111'),  # 2
            list('111001111001111'),  # 3
            list('101101111001001'),  # 4
            list('111100111001111'),  # 5
            list('111100111101111'),  # 6
            list('111001001001001'),  # 7
            list('111101111101111'),  # 8
            list('111101111001111')  # 9
        ]

    @staticmethod
    def get_test_cases() -> Dict[str, str]:
        return {
            "Верная 5": '111100111001111',
            "Искажённая 5": '111100011001111',
            "Фейковая 0": '000000000000000',
            "Фейковая 1": '111111111111111',
            "Фейковая 2": '101010101010101',
            "Верная 8": '111101111101111',
            "Искажённая 8": '011101111101110'
        }


def main():
    # Инициализация данных и модели
    training_data = DigitData.get_training_data()
    test_cases = DigitData.get_test_cases()

    # Создание и обучение модели
    recognizer = DigitRecognizer()

    print("Начало обучения...")
    recognizer.train(training_data, iterations=10000)
    print("Обучение завершено!")

    # Тестирование модели
    recognizer.evaluate(test_cases)

    # Запуск интерактивного режима
    recognizer.interactive_mode()


if __name__ == "__main__":
    main()
