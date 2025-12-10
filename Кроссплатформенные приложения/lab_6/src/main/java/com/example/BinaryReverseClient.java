package com.example;

import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import io.grpc.StatusRuntimeException;

import java.util.Arrays;
import java.util.List;
import java.util.concurrent.TimeUnit;

import com.example.BinaryReverseProto.BinaryReverseRequest;
import com.example.BinaryReverseProto.BinaryReverseResponse;

public class BinaryReverseClient {

    private final ManagedChannel channel;
    private final BinaryReverseServiceGrpc.BinaryReverseServiceBlockingStub blockingStub;

    public BinaryReverseClient(String host, int port) {
        this.channel = ManagedChannelBuilder.forAddress(host, port)
                .usePlaintext()
                .build();
        this.blockingStub = BinaryReverseServiceGrpc.newBlockingStub(channel);
    }

    public void shutdown() throws InterruptedException {
        channel.shutdown().awaitTermination(5, TimeUnit.SECONDS);
    }

    // Метод для вызова unary RPC
    public void calculateB(int m) {
        System.out.println("\n=== Вычисляем B(" + m + ") ===");

        try {
            // Создаем запрос
            BinaryReverseRequest request = BinaryReverseRequest.newBuilder()
                    .setM(m)
                    .build();

            // Отправляем запрос и получаем ответ
            BinaryReverseResponse response = blockingStub.calculateB(request);

            // Выводим результат
            printResponse(response);

        } catch (StatusRuntimeException e) {
            System.out.println("Ошибка gRPC: " + e.getStatus());
        }
    }

    // Метод для тестирования нескольких чисел
    public void testMultipleNumbers() {
        System.out.println("\n=== Тестирование функции B(m) ===");
        System.out.println("Функция B(m): переворачивает двоичное представление числа");

        List<Integer> testNumbers = Arrays.asList(1, 2, 3, 5, 8, 10, 13, 21, 255);

        for (int m : testNumbers) {
            calculateB(m);
        }
    }

    // Метод для вызова streaming RPC
    public void calculateBStream(int startM) {
        System.out.println("\n=== Streaming: вычисляем B(m) для чисел от " + startM + " до " + (startM + 3) + " ===");

        try {
            BinaryReverseRequest request = BinaryReverseRequest.newBuilder()
                    .setM(startM)
                    .build();

            // Получаем поток ответов
            java.util.Iterator<BinaryReverseResponse> responses =
                    blockingStub.calculateBStream(request);

            while (responses.hasNext()) {
                BinaryReverseResponse response = responses.next();
                System.out.println("  " + response.getDescription());
            }

        } catch (StatusRuntimeException e) {
            System.out.println("Ошибка gRPC: " + e.getStatus());
        }
    }

    // Вспомогательный метод для вывода результата
    private void printResponse(BinaryReverseResponse response) {
        System.out.println("m = " + response.getM());
        System.out.println("Двоичное представление: " + response.getBinaryRepresentation());
        System.out.println("Перевернутое двоичное: " + response.getReversedBinary());
        System.out.println("B(m) = " + response.getBResult());
        System.out.println("Описание: " + response.getDescription());
    }

    public static void main(String[] args) throws InterruptedException {
        // Создаем клиента, подключаемся к localhost:9090
        BinaryReverseClient client = new BinaryReverseClient("localhost", 9090);

        try {
            System.out.println("===========================================");
            System.out.println("gRPC Binary Reverse Client");
            System.out.println("===========================================");
            System.out.println("Подключаюсь к серверу...");
            System.out.println("Тестирование функции B(m):");
            System.out.println("  B(m) - переворачивает двоичное представление числа m");
            System.out.println("===========================================");

            // Тест 1: Одиночные вычисления
            client.calculateB(13);
            client.calculateB(10);
            client.calculateB(5);
            client.calculateB(255);

            // Тест 2: Несколько чисел
            client.testMultipleNumbers();

            // Тест 3: Streaming
            client.calculateBStream(1);
            client.calculateBStream(10);

            // Тест 4: Граничные случаи
            System.out.println("\n=== Граничные случаи ===");
            client.calculateB(1);  // Минимальное положительное
            client.calculateB(0);  // Ноль (должна быть ошибка)
            client.calculateB(1023); // 1023 = 1111111111₂ → перевернутое = 1023

        } finally {
            // Закрываем соединение
            client.shutdown();
        }
    }
}
