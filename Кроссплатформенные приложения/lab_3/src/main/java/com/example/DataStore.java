package com.example;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

public class DataStore {
    private static final DataStore instance = new DataStore();
    private final ConcurrentHashMap<Long, Product> productMap = new ConcurrentHashMap<>();
    private final AtomicLong idCounter = new AtomicLong();

    // Singleton pattern
    public static DataStore getInstance() {
        return instance;
    }

    private DataStore() {
        // Добавляем тестовые данные
        addProduct(new Product(1L, "Смартфон", "Электроника", 29999.99, 15, 0.3,
                "Смартфон с AMOLED экраном"));
        addProduct(new Product(2L, "Книга 'Война и мир'", "Книги", 899.50, 50, 1.2,
                "Классическая литература"));
        addProduct(new Product(3L, "Наушники беспроводные", "Электроника", 4999.99, 30, 0.2,
                "Bluetooth наушники с шумоподавлением"));
        addProduct(new Product(4L, "Футболка хлопковая", "Одежда", 1499.00, 100, 0.15,
                "Мужская футболка из 100% хлопка"));
        addProduct(new Product(5L, "Кофе в зернах", "Продукты", 1299.99, 40, 0.5,
                "Арабика, 100% натуральный кофе"));
    }

    // Получить товар по ID
    public Product getProduct(long id) {
        return productMap.get(id);
    }

    // Получить все товары
    public List<Product> getAllProducts() {
        return new ArrayList<>(productMap.values());
    }

    // Добавить товар
    public void addProduct(Product product) {
        if (product.getId() == 0) {
            long newId = idCounter.incrementAndGet();
            product.setId(newId);
        }
        productMap.put(product.getId(), product);
    }

    // Суммарная стоимость всех товаров
    public double getTotalValue() {
        return productMap.values().stream()
                .mapToDouble(p -> p.getPrice() * p.getQuantity())
                .sum();
    }

    // Суммарный вес всех товаров на складе
    public double getTotalWeight() {
        return productMap.values().stream()
                .mapToDouble(p -> p.getWeight() * p.getQuantity())
                .sum();
    }

    // Общее количество товаров на складе
    public int getTotalQuantity() {
        return productMap.values().stream()
                .mapToInt(Product::getQuantity)
                .sum();
    }
}
