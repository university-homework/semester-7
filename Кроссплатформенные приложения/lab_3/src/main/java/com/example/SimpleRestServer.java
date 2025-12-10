package com.example;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpExchange;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.util.List;

public class SimpleRestServer {
    private static final ObjectMapper objectMapper = new ObjectMapper();

    public static void main(String[] args) throws IOException {
        int port = 8000;
        HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);

        System.out.println("Сервер товаров-почтой");
        System.out.println("Порт: " + port);
        System.out.println("\n=========================================");
        System.out.println("Доступные эндпоинты:");
        System.out.println("  GET /api/products           - все товары");
        System.out.println("  GET /api/products/{id}      - товар по ID");
        System.out.println("  GET /api/products/total     - суммарная стоимость");
        System.out.println("  GET /api/products/stats     - статистика");
        System.out.println("=========================================");

        // Эндпоинт для всех товаров
        server.createContext("/api/products", exchange -> {
            String method = exchange.getRequestMethod();
            String path = exchange.getRequestURI().getPath();

            try {
                if ("GET".equals(method)) {
                    // Проверяем, запрашивается ли конкретный товар
                    if (path.matches("/api/products/\\d+")) {
                        handleGetProductById(exchange);
                    } else if (path.equals("/api/products/total")) {
                        handleGetTotalValue(exchange);
                    } else if (path.equals("/api/products/stats")) {
                        handleGetStats(exchange);
                    } else if (path.equals("/api/products")) {
                        handleGetAllProducts(exchange);
                    } else {
                        sendError(exchange, 404, "Не найдено");
                    }
                } else {
                    sendError(exchange, 405, "Метод не разрешен");
                }
            } catch (Exception e) {
                e.printStackTrace();
                sendError(exchange, 500, "Внутренняя ошибка сервера");
            } finally {
                exchange.close();
            }
        });

        server.setExecutor(null); // использовать дефолтный executor
        server.start();

        System.out.println("\nПримеры запросов:");
        System.out.println("  http://localhost:" + port + "/api/products");
        System.out.println("  http://localhost:" + port + "/api/products/1");
        System.out.println("  http://localhost:" + port + "/api/products/total");
    }

    private static void handleGetAllProducts(HttpExchange exchange) throws IOException {
        List<Product> products = DataStore.getInstance().getAllProducts();
        String response = objectMapper.writeValueAsString(products);

        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
        exchange.sendResponseHeaders(200, response.getBytes(StandardCharsets.UTF_8).length);

        try (OutputStream os = exchange.getResponseBody()) {
            os.write(response.getBytes(StandardCharsets.UTF_8));
        }
    }

    private static void handleGetProductById(HttpExchange exchange) throws IOException {
        String path = exchange.getRequestURI().getPath();
        String[] parts = path.split("/");

        if (parts.length < 4) {
            sendError(exchange, 400, "Неверный формат запроса");
            return;
        }

        try {
            long id = Long.parseLong(parts[3]);
            Product product = DataStore.getInstance().getProduct(id);

            if (product == null) {
                sendError(exchange, 404, "Товар с ID " + id + " не найден");
                return;
            }

            String response = objectMapper.writeValueAsString(product);

            exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
            exchange.sendResponseHeaders(200, response.getBytes(StandardCharsets.UTF_8).length);

            try (OutputStream os = exchange.getResponseBody()) {
                os.write(response.getBytes(StandardCharsets.UTF_8));
            }
        } catch (NumberFormatException e) {
            sendError(exchange, 400, "Неверный формат ID");
        }
    }

    private static void handleGetTotalValue(HttpExchange exchange) throws IOException {
        double totalValue = DataStore.getInstance().getTotalValue();

        ObjectNode responseNode = objectMapper.createObjectNode();
        responseNode.put("total_value", totalValue);
        responseNode.put("currency", "RUB");
        responseNode.put("message", "Суммарная стоимость всех товаров на складе");

        String response = objectMapper.writeValueAsString(responseNode);

        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
        exchange.sendResponseHeaders(200, response.getBytes(StandardCharsets.UTF_8).length);

        try (OutputStream os = exchange.getResponseBody()) {
            os.write(response.getBytes(StandardCharsets.UTF_8));
        }
    }

    private static void handleGetStats(HttpExchange exchange) throws IOException {
        DataStore dataStore = DataStore.getInstance();

        ObjectNode stats = objectMapper.createObjectNode();
        stats.put("total_products", dataStore.getAllProducts().size());
        stats.put("total_value", dataStore.getTotalValue());
        stats.put("total_quantity", dataStore.getTotalQuantity());
        stats.put("total_weight", dataStore.getTotalWeight());
        stats.put("currency", "RUB");
        stats.put("weight_unit", "кг");

        String response = objectMapper.writeValueAsString(stats);

        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
        exchange.sendResponseHeaders(200, response.getBytes(StandardCharsets.UTF_8).length);

        try (OutputStream os = exchange.getResponseBody()) {
            os.write(response.getBytes(StandardCharsets.UTF_8));
        }
    }

    private static void sendError(HttpExchange exchange, int code, String message) throws IOException {
        ObjectNode errorNode = objectMapper.createObjectNode();
        errorNode.put("error", true);
        errorNode.put("code", code);
        errorNode.put("message", message);

        String response = objectMapper.writeValueAsString(errorNode);

        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
        exchange.sendResponseHeaders(code, response.getBytes(StandardCharsets.UTF_8).length);

        try (OutputStream os = exchange.getResponseBody()) {
            os.write(response.getBytes(StandardCharsets.UTF_8));
        }
    }
}
