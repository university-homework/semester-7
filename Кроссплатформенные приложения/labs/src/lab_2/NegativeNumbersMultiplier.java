package lab_2;

import java.util.Random;
import java.util.concurrent.ForkJoinPool;
import java.util.concurrent.RecursiveAction;

public class NegativeNumbersMultiplier {

    public static void main(String[] args) {
        int size = 10000000; // Большой массив для демонстрации
        int[] array = generateRandomArray(size);

        System.out.println("Исходный массив (первые 20 элементов):");
        printArray(array, 20);

        ForkJoinPool pool = new ForkJoinPool();

        long startTime = System.currentTimeMillis();

        pool.invoke(new MultiplyNegativeTask(array, 0, array.length));

        long endTime = System.currentTimeMillis();

        System.out.println("\nМассив после умножения отрицательных чисел на 2 (первые 20 элементов):");
        printArray(array, 20);
        System.out.println("\nВремя выполнения: " + (endTime - startTime) + " мс");

        // Сравнение с однопоточным вариантом
        testSingleThreadPerformance();
    }

    // RecursiveAction для ForkJoin Framework
    static class MultiplyNegativeTask extends RecursiveAction {
        private static final int THRESHOLD = 10000; // Порог для прямого выполнения
        private final int[] array;
        private final int start;
        private final int end;

        public MultiplyNegativeTask(int[] array, int start, int end) {
            this.array = array;
            this.start = start;
            this.end = end;
        }

        @Override
        protected void compute() {
            if (end - start <= THRESHOLD) {
                // Вычисляем непосредственно
                for (int i = start; i < end; i++) {
                    if (array[i] < 0) {
                        array[i] *= 2;
                    }
                }
            } else {
                // Делим задачу пополам
                int mid = (start + end) / 2;
                MultiplyNegativeTask left = new MultiplyNegativeTask(array, start, mid);
                MultiplyNegativeTask right = new MultiplyNegativeTask(array, mid, end);

                invokeAll(left, right);
            }
        }
    }

    // Однопоточная версия для сравнения производительности
    public static void multiplyNegativeSingleThread(int[] array) {
        for (int i = 0; i < array.length; i++) {
            if (array[i] < 0) {
                array[i] *= 2;
            }
        }
    }

    // Генерация случайного массива с отрицательными числами
    private static int[] generateRandomArray(int size) {
        int[] array = new int[size];
        Random random = new Random();

        for (int i = 0; i < size; i++) {
            // Генерируем числа от -100 до 100
            array[i] = random.nextInt(201) - 100;
        }
        return array;
    }

    // Вывод массива
    private static void printArray(int[] array, int count) {
        for (int i = 0; i < Math.min(count, array.length); i++) {
            System.out.print(array[i] + " ");
        }
        if (array.length > count) {
            System.out.print("...");
        }
        System.out.println();
    }

    // Тест производительности однопоточного vs многопоточного
    private static void testSingleThreadPerformance() {
        int size = 10000000;
        int[] array1 = generateRandomArray(size);
        int[] array2 = array1.clone(); // Копия для честного сравнения

        System.out.println("\n=== Сравнение производительности ===");

        // Многопоточный вариант
        long startTime = System.currentTimeMillis();
        ForkJoinPool pool = new ForkJoinPool();
        pool.invoke(new MultiplyNegativeTask(array1, 0, array1.length));
        long multiThreadTime = System.currentTimeMillis() - startTime;

        // Однопоточный вариант
        startTime = System.currentTimeMillis();
        multiplyNegativeSingleThread(array2);
        long singleThreadTime = System.currentTimeMillis() - startTime;

        System.out.println("Размер массива: " + size);
        System.out.println("Многопоточное время: " + multiThreadTime + " мс");
        System.out.println("Однопоточное время: " + singleThreadTime + " мс");
        System.out.println("Ускорение: " + (double)singleThreadTime/multiThreadTime + "x");

        // Проверка корректности
        boolean correct = true;
        for (int i = 0; i < array1.length; i++) {
            if (array1[i] != array2[i]) {
                correct = false;
                break;
            }
        }
        System.out.println("Результаты идентичны: " + correct);
    }
}