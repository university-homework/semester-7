const http = require('http');
const url = require('url');
const querystring = require('querystring');

// Функция для проверки, есть ли в числе повторяющиеся цифры
function hasDuplicateDigits(num) {
    const digits = num.toString().split('');
    const uniqueDigits = new Set(digits);
    return digits.length !== uniqueDigits.size;
}

// Функция для нахождения N-го числа в последовательности
function findNthSequenceNumber(n) {
    let count = 0;
    let currentNumber = 1;
    
    while (count < n) {
        if (!hasDuplicateDigits(currentNumber)) {
            count++;
            if (count === n) {
                return currentNumber;
            }
        }
        currentNumber++;
    }
    return -1; // если не найдено
}

const server = http.createServer((request, response) => {
    const parsedUrl = url.parse(request.url, true);
    const pathname = parsedUrl.pathname;

    // Устанавливаем заголовки CORS для кросс-доменных запросов
    response.setHeader('Access-Control-Allow-Origin', '*');
    response.setHeader('Access-Control-Allow-Methods', 'GET, POST');
    response.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    
    if (pathname === '/') {
        // Главная страница
        response.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        response.write(`
            <!DOCTYPE html>
            <html lang="ru">
            <head>
                <meta charset="UTF-8">
                <title>Вариант 11 - Последовательность без повторяющихся цифр</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; }
                    .container { max-width: 600px; margin: 0 auto; }
                    .form-group { margin: 20px 0; }
                    label { display: block; margin-bottom: 5px; }
                    input { padding: 8px; width: 200px; }
                    button { padding: 10px 20px; background: #007cba; color: white; border: none; cursor: pointer; }
                    .result { margin-top: 20px; padding: 15px; background: #f5f5f5; border-radius: 5px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Вариант 11</h1>
                    <p>Найти N-ое число в последовательности без повторяющихся цифр</p>
                    
                    <div class="form-group">
                        <label for="n">Введите номер N:</label>
                        <input type="number" id="n" min="1" value="10">
                        <button onclick="calculate()">Найти число</button>
                    </div>
                    
                    <div id="result" class="result" style="display:none;"></div>
                    
                    <script>
                        function calculate() {
                            const n = document.getElementById('n').value;
                            
                            fetch('/calculate?n=' + n)
                                .then(response => response.json())
                                .then(data => {
                                    const resultDiv = document.getElementById('result');
                                    if (data.error) {
                                        resultDiv.innerHTML = '<strong>Ошибка:</strong> ' + data.error;
                                    } else {
                                        resultDiv.innerHTML = \`
                                            <strong>Результат:</strong><br>
                                            <strong>N = \${data.n}:</strong> \${data.result}<br>
                                            <strong>Последовательность:</strong> \${data.sequence.join(', ')}
                                        \`;
                                    }
                                    resultDiv.style.display = 'block';
                                })
                                .catch(error => {
                                    console.error('Error:', error);
                                    document.getElementById('result').innerHTML = '<strong>Ошибка при вычислениях</strong>';
                                    document.getElementById('result').style.display = 'block';
                                });
                        }
                        
                        // Вычислить для примера при загрузке
                        window.onload = calculate;
                    </script>
                </div>
            </body>
            </html>
        `);
        response.end();
    }
    else if (pathname === '/calculate') {
        // API endpoint для вычислений
        const query = parsedUrl.query;
        const n = parseInt(query.n);
        
        if (!n || n < 1) {
            response.writeHead(400, { 'Content-Type': 'application/json; charset=utf-8' });
            response.end(JSON.stringify({ error: 'Некорректное значение N' }));
            return;
        }
        
        // Находим N-е число
        const result = findNthSequenceNumber(n);
        
        // Генерируем часть последовательности для наглядности
        const sequence = [];
        let count = 0;
        let current = 1;
        while (count < Math.min(n, 20)) {
            if (!hasDuplicateDigits(current)) {
                count++;
                sequence.push(current);
            }
            current++;
        }
        
        response.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
        response.end(JSON.stringify({
            n: n,
            result: result,
            sequence: sequence,
            description: `N-ое число в последовательности без повторяющихся цифр`
        }));
    }
    else {
        response.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
        response.end('Страница не найдена');
    }
});

const PORT = 3000;
server.listen(PORT, () => {
    console.log(`Сервер запущен на http://localhost:${PORT}`);
    console.log('Вариант 11: Найти N-ое число в последовательности без повторяющихся цифр');
});
