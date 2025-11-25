const express = require('express');
const path = require('path');
const app = express();

// База данных пациентов
let patients = [
    { id: 1, name: 'Иванов Иван', age: 45, diagnosis: 'Гипертония' },
    { id: 2, name: 'Петрова Мария', age: 32, diagnosis: 'Астма' },
    { id: 3, name: 'Сидоров Алексей', age: 50, diagnosis: 'Диабет' }
];

// Главная страница
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Все пациенты
app.get('/patients', (req, res) => {
    res.json({ 
        success: true, 
        count: patients.length,
        data: patients 
    });
});

// Пациент по ID
app.get('/patients/:id', (req, res) => {
    const patient = patients.find(p => p.id === parseInt(req.params.id));
    if (patient) {
        res.json({ success: true, data: patient });
    } else {
        res.status(404).json({ success: false, error: 'Пациент не найден' });
    }
});

// Статистика по возрасту
app.get('/patients/stats/total-age', (req, res) => {
    const totalAge = patients.reduce((sum, patient) => sum + patient.age, 0);
    res.json({ 
        success: true, 
        data: { 
            totalAge,
            patientCount: patients.length,
            averageAge: (totalAge / patients.length).toFixed(1)
        } 
    });
});

// Поиск по имени
app.get('/patients/search/by-name/:name', (req, res) => {
    const name = req.params.name.toLowerCase();
    const foundPatients = patients.filter(p => 
        p.name.toLowerCase().includes(name)
    );
    res.json({
        success: true,
        count: foundPatients.length,
        data: foundPatients
    });
});

// Поиск по диагнозу
app.get('/patients/search/by-diagnosis/:diagnosis', (req, res) => {
    const diagnosis = req.params.diagnosis.toLowerCase();
    const foundPatients = patients.filter(p => 
        p.diagnosis.toLowerCase().includes(diagnosis)
    );
    res.json({
        success: true,
        count: foundPatients.length,
        data: foundPatients
    });
});

// Запуск сервера
app.listen(3000, () => {
    console.log('Сервер запущен: http://localhost:3000');
});