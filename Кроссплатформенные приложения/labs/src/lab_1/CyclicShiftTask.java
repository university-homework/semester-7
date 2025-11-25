package lab_1;

import java.util.Random;

public class CyclicShiftTask {
    public static void main(String[] args) throws InterruptedException {
        int rows = 6;
        int cols = 10;
        int shift = 2;

        int[][] matrix = generateRandomMatrix(rows, cols);

        System.out.println("Исходная матрица:");
        printMatrix(matrix);

        cyclicShiftParallel(matrix, shift, 4);

        System.out.println("\nМатрица после циклического сдвига на " + shift + ":");
        printMatrix(matrix);
    }

    // Параллельный циклический сдвиг с использованием Thread API
    public static void cyclicShiftParallel(int[][] matrix, int shift, int threadCount)
            throws InterruptedException {
        int rows = matrix.length;
        Thread[] threads = new Thread[threadCount];

        // Создаем и запускаем потоки
        for (int i = 0; i < threadCount; i++) {
            final int threadIndex = i;
            threads[i] = new Thread(() -> {
                // Распределяем строки между потоками
                for (int row = threadIndex; row < rows; row += threadCount) {
                    cyclicShiftRow(matrix[row], shift);
                }
            });
            threads[i].start();
        }

        // Ждем завершения всех потоков
        for (Thread thread : threads) {
            thread.join();
        }
    }

    // Генерация случайной матрицы
    public static int[][] generateRandomMatrix(int rows, int cols) {
        int[][] matrix = new int[rows][cols];
        Random random = new Random();

        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                matrix[i][j] = random.nextInt(100); // числа от 0 до 99
            }
        }
        return matrix;
    }

    // Циклический сдвиг одной строки
    private static void cyclicShiftRow(int[] row, int shift) {
        int n = row.length;
        int[] temp = new int[n];

        for (int i = 0; i < n; i++) {
            temp[(i + shift) % n] = row[i];
        }

        System.arraycopy(temp, 0, row, 0, n);
    }

    // Вывод матрицы на экран
    private static void printMatrix(int[][] matrix) {
        for (int i = 0; i < matrix.length; i++) {
            for (int j = 0; j < matrix[i].length; j++) {
                System.out.printf("%3d ", matrix[i][j]);
            }
            System.out.println();
        }
    }
}