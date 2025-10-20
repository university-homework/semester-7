const http = require('http');
const fs = require('fs');
const path = require('path');

const server = http.createServer((request, response) => {
    const url = request.url;

    // Страница 1: методом response.write
    if (url === '/page1') {
        response.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        response.write('<!DOCTYPE html>');
        response.write('<html lang="ru">');
        response.write('<head>');
        response.write('<meta charset="UTF-8">');
        response.write('<title>Страница 1 - response.write</title>');
        response.write('</head>');
        response.write('<body>');
        response.write('<h1>Добро пожаловать на страницу 1!</h1>');
        response.write('<p>Эта страница отправлена с помощью метода response.write()</p>');
        response.write('<ul>');
        response.write('<li><a href="/page1">Страница 1</a></li>');
        response.write('<li><a href="/page2">Страница 2</a></li>');
        response.write('<li><a href="/page3">Страница 3</a></li>');
        response.write('</ul>');
        response.write('</body>');
        response.write('</html>');
        response.end();
    }

    // Страница 2: методом fs.createReadStream()
    else if (url === '/page2') {
        response.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });

        const filePath = path.join(__dirname, 'page2.html');

        // Создаем файл page2.html если он не существует
        if (!fs.existsSync(filePath)) {
            const page2Content = `<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Страница 2 - createReadStream</title>
</head>
<body>
    <h1>Добро пожаловать на страницу 2!</h1>
    <p>Эта страница отправлена с помощью метода fs.createReadStream()</p>
    <ul>
        <li><a href="/page1">Страница 1</a></li>
        <li><a href="/page2">Страница 2</a></li>
        <li><a href="/page3">Страница 3</a></li>
    </ul>
</body>
</html>`;
            fs.writeFileSync(filePath, page2Content);
        }
        const readStream = fs.createReadStream(filePath);
        readStream.pipe(response);
    }

    // Страница 3: методом fs.readFile() и response.end()
    else if (url === '/page3') {
        const filePath = path.join(__dirname, 'page3.html');

        // Создаем файл page3.html если он не существует
        if (!fs.existsSync(filePath)) {
            const page3Content = `<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Страница 3 - readFile + end</title>
</head>
<body>
    <h1>Добро пожаловать на страницу 3!</h1>
    <p>Эта страница отправлена с помощью метода fs.readFile() и response.end()</p>
    <ul>
        <li><a href="/page1">Страница 1</a></li>
        <li><a href="/page2">Страница 2</a></li>
        <li><a href="/page3">Страница 3</a></li>
    </ul>
</body>
</html>`;
            fs.writeFileSync(filePath, page3Content);
        }

        fs.readFile(filePath, 'utf8', (err, data) => {
            if (err) {
                response.writeHead(500, { 'Content-Type': 'text/html; charset=utf-8' });
                response.end('Ошибка чтения файла');
                return;
            }
            response.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
            response.end(data);
        });
    }

    // Главная страница с навигацией
    else {
        response.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        response.write('<!DOCTYPE html>');
        response.write('<html lang="ru">');
        response.write('<head>');
        response.write('<meta charset="UTF-8">');
        response.write('<title>Главная страница</title>');
        response.write('</head>');
        response.write('<body>');
        response.write('<h1>Добро пожаловать на главную страницу!</h1>');
        response.write('<p>Выберите страницу для просмотра:</p>');
        response.write('<ul>');
        response.write('<li><a href="/page1">Страница 1 - response.write()</a></li>');
        response.write('<li><a href="/page2">Страница 2 - fs.createReadStream()</a></li>');
        response.write('<li><a href="/page3">Страница 3 - fs.readFile() + response.end()</a></li>');
        response.write('</ul>');
        response.write('</body>');
        response.write('</html>');
        response.end();
    }
});

const PORT = 3000;
server.listen(PORT, () => {
    console.log(`Сервер запущен на http://localhost:${PORT}`);
    console.log('Доступные страницы:');
    console.log('http://localhost:3000/page1 - метод response.write()');
    console.log('http://localhost:3000/page2 - метод fs.createReadStream()');
    console.log('http://localhost:3000/page3 - метод fs.readFile() + response.end()');
});
