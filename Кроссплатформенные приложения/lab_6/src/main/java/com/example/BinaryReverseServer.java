package com.example;

import io.grpc.Server;
import io.grpc.ServerBuilder;
import io.grpc.stub.StreamObserver;
import java.io.IOException;
import java.util.concurrent.TimeUnit;

import com.example.BinaryReverseProto.BinaryReverseRequest;
import com.example.BinaryReverseProto.BinaryReverseResponse;

public class BinaryReverseServer {
    static class BinaryReverseServiceImpl extends BinaryReverseServiceGrpc.BinaryReverseServiceImplBase {
        @Override
        public void calculateB(BinaryReverseRequest request,
                               StreamObserver<BinaryReverseResponse> responseObserver) {
            int m = request.getM();

            if (m <= 0) {
                BinaryReverseResponse errorResponse = BinaryReverseResponse.newBuilder()
                        .setM(m)
                        .setBResult(-1)
                        .setDescription("Ошибка: m должно быть положительным числом")
                        .build();
                responseObserver.onNext(errorResponse);
                responseObserver.onCompleted();
                return;
            }

            BinaryReverseResult result = calculateBinaryReverse(m);

            BinaryReverseResponse response = BinaryReverseResponse.newBuilder()
                    .setM(m)
                    .setBResult(result.bResult)
                    .setBinaryRepresentation(result.binary)
                    .setReversedBinary(result.reversedBinary)
                    .setDescription(String.format(
                            "B(%d) = %d (Двоичное: %s, Перевернутое: %s)",
                            m, result.bResult, result.binary, result.reversedBinary
                    ))
                    .build();

            responseObserver.onNext(response);
            responseObserver.onCompleted();
        }

        @Override
        public void calculateBStream(BinaryReverseRequest request,
                                     StreamObserver<BinaryReverseResponse> responseObserver) {
            int m = request.getM();

            for (int i = 0; i < 4; i++) {
                int currentM = m + i;
                BinaryReverseResult result = calculateBinaryReverse(currentM);

                BinaryReverseResponse response = BinaryReverseResponse.newBuilder()
                        .setM(currentM)
                        .setBResult(result.bResult)
                        .setBinaryRepresentation(result.binary)
                        .setReversedBinary(result.reversedBinary)
                        .setDescription(String.format("B(%d) = %d", currentM, result.bResult))
                        .build();

                responseObserver.onNext(response);

                try {
                    Thread.sleep(500);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    responseObserver.onError(e);
                    return;
                }
            }

            responseObserver.onCompleted();
        }

        private static class BinaryReverseResult {
            int bResult;
            String binary;
            String reversedBinary;

            BinaryReverseResult(int bResult, String binary, String reversedBinary) {
                this.bResult = bResult;
                this.binary = binary;
                this.reversedBinary = reversedBinary;
            }
        }

        private BinaryReverseResult calculateBinaryReverse(int m) {
            String binary = Integer.toBinaryString(m);
            String reversedBinary = new StringBuilder(binary).reverse().toString();

            while (reversedBinary.length() > 1 && reversedBinary.charAt(0) == '0') {
                reversedBinary = reversedBinary.substring(1);
            }

            int bResult = Integer.parseInt(reversedBinary, 2);

            return new BinaryReverseResult(bResult, binary, reversedBinary);
        }
    }

    public static void main(String[] args) throws IOException, InterruptedException {
        int port = 9090;
        Server server = ServerBuilder.forPort(port)
                .addService(new BinaryReverseServiceImpl())
                .build()
                .start();

        System.out.println("===========================================");
        System.out.println("gRPC Binary Reverse Server");
        System.out.println("===========================================");
        System.out.println("Сервер запущен на порту: " + port);
        System.out.println("Сервис: B(m) - переворачивание двоичного представления");
        System.out.println("Примеры:");
        System.out.println("  B(13) = 11  (1101₂ → 1011₂)");
        System.out.println("  B(10) = 5   (1010₂ → 0101₂ = 101₂)");
        System.out.println("  B(5)  = 5   (101₂ → 101₂)");
        System.out.println("  B(8)  = 1   (1000₂ → 0001₂ = 1₂)");
        System.out.println("===========================================");
        System.out.println("Ожидаем запросы...");
        System.out.println("Для остановки нажмите Ctrl+C");
        System.out.println("===========================================");

        // Добавляем shutdown hook для корректного завершения
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            System.out.println("\nЗавершение работы сервера...");
            server.shutdown();
            try {
                if (!server.awaitTermination(5, TimeUnit.SECONDS)) {
                    server.shutdownNow();
                }
            } catch (InterruptedException e) {
                server.shutdownNow();
            }
            System.out.println("Сервер остановлен");
        }));

        server.awaitTermination();
    }
}
