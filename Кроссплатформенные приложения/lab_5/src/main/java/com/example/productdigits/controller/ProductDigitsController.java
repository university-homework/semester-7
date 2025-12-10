package com.example.productdigits.controller;

import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class ProductDigitsController {

    @GetMapping("/product-digits/{n}")
    public ProductDigitsResponse getSmallestNumber(@PathVariable long n) {
        String result = findSmallestNumberWithProduct(n);

        return new ProductDigitsResponse(
                n,
                result,
                result.equals("NO_SOLUTION") ? "ERROR" : "OK",
                result.equals("NO_SOLUTION") ?
                        "No natural number exists with product of digits = " + n :
                        "Success"
        );
    }

    @GetMapping("/product-digits")
    public ProductDigitsResponse getSmallestNumberWithParam(@RequestParam long n) {
        return getSmallestNumber(n);
    }

    private String findSmallestNumberWithProduct(long n) {
        // Особые случаи
        if (n == 0) return "10"; // Минимальное число с цифрой 0
        if (n == 1) return "1";  // 1 = 1

        if (n < 0) return "ERROR: Number must be positive";

        // Раскладываем на цифры
        java.util.List<Integer> digits = new java.util.ArrayList<>();

        for (int digit = 9; digit >= 2; digit--) {
            while (n % digit == 0) {
                digits.add(digit);
                n /= digit;
            }
        }

        // Если остался простой множитель > 9, решения нет
        if (n > 1) {
            return "NO_SOLUTION";
        }

        // Сортируем для получения наименьшего числа
        java.util.Collections.sort(digits);

        // Собираем результат
        StringBuilder result = new StringBuilder();
        for (int digit : digits) {
            result.append(digit);
        }

        return result.toString();
    }

    // Класс для JSON ответа
    public static class ProductDigitsResponse {
        private long input;
        private String result;
        private String status;
        private String message;

        public ProductDigitsResponse(long input, String result, String status, String message) {
            this.input = input;
            this.result = result;
            this.status = status;
            this.message = message;
        }

        // Геттеры
        public long getInput() { return input; }
        public String getResult() { return result; }
        public String getStatus() { return status; }
        public String getMessage() { return message; }
    }
}
