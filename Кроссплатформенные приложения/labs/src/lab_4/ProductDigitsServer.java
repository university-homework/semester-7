package lab_4;

import java.io.*;
import java.net.*;
import java.util.*;
import java.util.concurrent.*;

public class ProductDigitsServer {
    private static final int PORT = 12345;
    private static final int THREAD_POOL_SIZE = 10;
    private ServerSocket serverSocket;
    private ExecutorService threadPool;

    public ProductDigitsServer() {
        this.threadPool = Executors.newFixedThreadPool(THREAD_POOL_SIZE);
    }

    public void start() {
        try {
            serverSocket = new ServerSocket(PORT);
            System.out.println("Server started on port " + PORT);
            System.out.println("Service: Find smallest number with digit product = N");

            while (true) {
                Socket clientSocket = serverSocket.accept();
                System.out.println("New client: " + clientSocket.getInetAddress());
                threadPool.execute(new ClientHandler(clientSocket));
            }
        } catch (IOException e) {
            System.out.println("Server error: " + e.getMessage());
        }
    }

    public void stop() {
        try {
            if (serverSocket != null) serverSocket.close();
            if (threadPool != null) threadPool.shutdown();
        } catch (IOException e) {
            System.out.println("Error stopping server: " + e.getMessage());
        }
    }

    private static class ClientHandler implements Runnable {
        private Socket clientSocket;

        public ClientHandler(Socket socket) {
            this.clientSocket = socket;
        }

        @Override
        public void run() {
            try (
                    BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
                    PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true)
            ) {
                String inputLine;
                while ((inputLine = in.readLine()) != null) {
                    System.out.println("Received: " + inputLine + " from " + clientSocket.getInetAddress());

                    if (inputLine.equalsIgnoreCase("exit")) {
                        out.println("Goodbye!");
                        break;
                    }

                    try {
                        long n = Long.parseLong(inputLine);
                        String result = findSmallestNumberWithProduct(n);
                        out.println(result);
                    } catch (NumberFormatException e) {
                        out.println("ERROR: Please enter a valid positive integer");
                    } catch (Exception e) {
                        out.println("ERROR: " + e.getMessage());
                    }
                }
            } catch (IOException e) {
                System.out.println("Client handling error: " + e.getMessage());
            } finally {
                try {
                    clientSocket.close();
                    System.out.println("Client disconnected: " + clientSocket.getInetAddress());
                } catch (IOException e) {
                    System.out.println("Error closing client socket: " + e.getMessage());
                }
            }
        }

        // Основной алгоритм
        private String findSmallestNumberWithProduct(long n) {
            // Особые случаи
            if (n == 0) return "10"; // 0 * ? = 0, но 10 - минимальное с цифрой 0
            if (n == 1) return "1";  // произведение цифр 1 = 1

            if (n < 0) return "ERROR: Number must be positive";

            List<Integer> digits = new ArrayList<>();

            // Раскладываем на цифры от 9 до 2
            for (int digit = 9; digit >= 2; digit--) {
                while (n % digit == 0) {
                    digits.add(digit);
                    n /= digit;
                }
            }

            // Если после разложения осталось число > 1, значит N имеет простой множитель > 9
            if (n > 1) {
                return "NO_SOLUTION";
            }

            // Сортируем цифры для получения наименьшего числа
            Collections.sort(digits);

            // Собираем число из цифр
            StringBuilder result = new StringBuilder();
            for (int digit : digits) {
                result.append(digit);
            }

            return result.toString();
        }
    }

    public static void main(String[] args) {
        ProductDigitsServer server = new ProductDigitsServer();
        server.start();
    }
}
