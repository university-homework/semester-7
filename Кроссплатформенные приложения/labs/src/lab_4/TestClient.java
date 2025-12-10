package lab_4;

import java.io.*;
import java.net.*;
import java.util.concurrent.*;

public class TestClient {
    private static final String SERVER_HOST = "localhost";
    private static final int SERVER_PORT = 12345;
    private static final int NUM_CLIENTS = 10;
    private static final int REQUESTS_PER_CLIENT = 5;

    public static void main(String[] args) throws InterruptedException {
        System.out.println("Starting test with " + NUM_CLIENTS + " clients");

        ExecutorService executor = Executors.newFixedThreadPool(NUM_CLIENTS);
        CountDownLatch latch = new CountDownLatch(NUM_CLIENTS);

        long startTime = System.currentTimeMillis();

        for (int i = 0; i < NUM_CLIENTS; i++) {
            final int clientId = i;
            executor.execute(() -> {
                try {
                    testClient(clientId);
                    System.out.println("Client " + clientId + " finished");
                } catch (Exception e) {
                    System.out.println("Client " + clientId + " error: " + e.getMessage());
                } finally {
                    latch.countDown();
                }
            });
        }

        latch.await();
        executor.shutdown();

        long totalTime = System.currentTimeMillis() - startTime;
        System.out.println("\nAll clients finished in " + totalTime + "ms");
    }

    private static void testClient(int clientId) {
        try (
                Socket socket = new Socket(SERVER_HOST, SERVER_PORT);
                BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                PrintWriter out = new PrintWriter(socket.getOutputStream(), true)
        ) {
            // Тестовые числа
            long[] testNumbers = {1, 10, 24, 36, 100, 0, 13, 49, 72, 81};

            for (int i = 0; i < REQUESTS_PER_CLIENT; i++) {
                long number = testNumbers[(clientId + i) % testNumbers.length];
                out.println(number);

                String response = in.readLine();
                System.out.println("Client " + clientId + ": product(" + number + ") = " + response);

                Thread.sleep(50);
            }

            out.println("exit");
        } catch (Exception e) {
            System.out.println("Client " + clientId + " connection error: " + e.getMessage());
        }
    }
}
