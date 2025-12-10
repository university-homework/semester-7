package com.example;

public class Product {
    private long id;
    private String name;
    private String category;
    private double price;
    private int quantity;
    private double weight;
    private String description;

    // Конструктор без параметров
    public Product() {}

    // Конструктор с параметрами
    public Product(long id, String name, String category, double price,
                   int quantity, double weight, String description) {
        this.id = id;
        this.name = name;
        this.category = category;
        this.price = price;
        this.quantity = quantity;
        this.weight = weight;
        this.description = description;
    }

    // Геттеры
    public long getId() { return id; }
    public String getName() { return name; }
    public String getCategory() { return category; }
    public double getPrice() { return price; }
    public int getQuantity() { return quantity; }
    public double getWeight() { return weight; }
    public String getDescription() { return description; }

    // Сеттеры
    public void setId(long id) { this.id = id; }
    public void setName(String name) { this.name = name; }
    public void setCategory(String category) { this.category = category; }
    public void setPrice(double price) { this.price = price; }
    public void setQuantity(int quantity) { this.quantity = quantity; }
    public void setWeight(double weight) { this.weight = weight; }
    public void setDescription(String description) { this.description = description; }

    @Override
    public String toString() {
        return "com.example.Product{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", category='" + category + '\'' +
                ", price=" + price +
                ", quantity=" + quantity +
                ", weight=" + weight +
                ", description='" + description + '\'' +
                '}';
    }
}
