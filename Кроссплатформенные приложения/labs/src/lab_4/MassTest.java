package lab_4;

import java.io.*;
import java.net.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class MassTest {
    private static final String SERVER_HOST = "localhost";
    private static final int SERVER_PORT = 12345;
    private static final int CONNECTION_COUNT = 50;

    public static void main(String[] args) throws InterruptedException {
        System.out.println("Testing " + CONNECTION_COUNT + " simultaneous connections");

        ExecutorService executor = Executors.newFixedThreadPool(CONNECTION_COUNT);
        CountDownLatch latch = new CountDownLatch(CONNECTION_COUNT);

        // Используем AtomicInteger для потокобезопасного подсчета
        AtomicInteger success = new AtomicInteger(0);
        AtomicInteger fail = new AtomicInteger(0);

        for (int i = 0; i < CONNECTION_COUNT; i++) {
            final int clientId = i;
            executor.execute(() -> {
                try {
                    Socket socket = new Socket(SERVER_HOST, SERVER_PORT);
                    System.out.println("Connection " + clientId + " successful");

                    // Отправляем одно число
                    PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
                    BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

                    out.println("24");
                    String response = in.readLine();
                    System.out.println("Connection " + clientId + " response: " + response);

                    Thread.sleep(500);
                    socket.close();
                    success.incrementAndGet();  // Увеличиваем счетчик успешных
                } catch (Exception e) {
                    System.out.println("Connection " + clientId + " failed: " + e.getMessage());
                    fail.incrementAndGet();  // Увеличиваем счетчик неудачных
                } finally {
                    latch.countDown();
                }
            });
        }

        latch.await();
        executor.shutdown();

        System.out.println("\n=== Test Results ===");
        System.out.println("Successful connections: " + success.get());
        System.out.println("Failed connections: " + fail.get());
        System.out.println("Success rate: " + (success.get() * 100.0 / CONNECTION_COUNT) + "%");
    }
}