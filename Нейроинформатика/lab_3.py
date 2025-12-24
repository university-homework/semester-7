import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from tensorflow import keras
import keras_tuner as kt

DATA_PATH = 'bd3.xlsx'
MAX_TRIALS = 20
EXECUTIONS_PER_TRIAL = 1
TUNER_EPOCHS = 30
FINAL_TRAIN_EPOCHS = 80
TEST_SIZE = 0.2
VALIDATION_SPLIT = 0.2
RANDOM_STATE = 42
FEATURE_COLS = ['L1', 'L3', 'P1', 'F1', 'F2', 'F3', 'F4', 'R1', 'R2', 'R3', 'R5', 'A2', 'A4', 'A5', 'A6']
LABEL_COL = 'P'


def load_and_prepare_data(path):
    df = pd.read_excel(path)
    print(f"Загружено: {df.shape}")
    print(df.head())

    # Заполняем пропуски
    df = df.fillna(df.mean(numeric_only=True))
    for col in df.select_dtypes(exclude=[np.number]):
        df[col].fillna(df[col].mode()[0], inplace=True)

    X = df[FEATURE_COLS].copy()
    y = df[LABEL_COL].copy()

    # Масштабирование признаков
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X.values.astype(np.float32))

    # Кодирование меток
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    num_classes = len(np.unique(y_encoded))
    print(f"Классы: {num_classes}, {le.classes_}")

    return X_scaled, y_encoded, num_classes, le

X, y, num_classes, le = load_and_prepare_data(DATA_PATH)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
)


def build_model(hp):
    inputs = keras.Input(shape=(X_train.shape[1],))
    x = inputs

    num_layers = hp.Int('num_layers', 2, 5)
    units_base = hp.Choice('units_base', [64, 128, 256])
    activation = hp.Choice('activation', ['relu', 'tanh'])
    dropout = hp.Float('dropout', 0.0, 0.3, step=0.1)

    for i in range(num_layers):
        units = max(8, units_base // (2 ** i))
        x = keras.layers.Dense(units, activation=activation)(x)
        x = keras.layers.BatchNormalization()(x)
        if dropout > 0:
            x = keras.layers.Dropout(dropout)(x)

    if num_classes == 2:
        outputs = keras.layers.Dense(1, activation='sigmoid')(x)
        loss = 'binary_crossentropy'
        metrics = ['accuracy']
    else:
        outputs = keras.layers.Dense(num_classes, activation='softmax')(x)
        loss = 'sparse_categorical_crossentropy'
        metrics = ['accuracy']

    lr = hp.Float('learning_rate', 1e-4, 1e-2, sampling='log')
    model = keras.Model(inputs, outputs)
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=lr), loss=loss, metrics=metrics)
    return model


tuner = kt.RandomSearch(
    build_model,
    objective='val_accuracy',
    max_trials=MAX_TRIALS,
    executions_per_trial=EXECUTIONS_PER_TRIAL,
    directory='kt_dir',
    project_name='ns_model'
)

tuner.search(X_train, y_train, epochs=TUNER_EPOCHS, validation_split=VALIDATION_SPLIT, verbose=1)
best_hps = tuner.get_best_hyperparameters(num_trials=1)[0]


def train_fixed_model(hps):
    model = tuner.hypermodel.build(hps)
    history = model.fit(
        X_train, y_train,
        epochs=FINAL_TRAIN_EPOCHS,
        validation_split=VALIDATION_SPLIT,
        batch_size=32,
        verbose=1
    )
    loss, acc = model.evaluate(X_test, y_test, verbose=0)
    print(f"Тестовая точность (фиксированные эпохи): {acc:.3f}")
    return model, history, acc

model_fixed, hist_fixed, acc_fixed = train_fixed_model(best_hps)


def train_early_stopping_model(hps):
    model = tuner.hypermodel.build(hps)
    es = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    history = model.fit(
        X_train, y_train,
        epochs=FINAL_TRAIN_EPOCHS,
        validation_split=VALIDATION_SPLIT,
        batch_size=32,
        callbacks=[es],
        verbose=1
    )
    loss, acc = model.evaluate(X_test, y_test, verbose=0)
    print(f"Тестовая точность (EarlyStopping): {acc:.3f}")
    return model, history, acc

model_es, hist_es, acc_es = train_early_stopping_model(best_hps)


def plot_history(hist_fixed, hist_es, acc_fixed, acc_es):
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 2, 1)
    plt.plot(hist_fixed.history['accuracy'], label='обучение')
    plt.plot(hist_fixed.history['val_accuracy'], label='валидация')
    plt.title(f'Фиксированные эпохи\nТест: {acc_fixed:.3f}')
    plt.ylim(0, 1)
    plt.legend()
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(hist_es.history['accuracy'], label='обучение')
    plt.plot(hist_es.history['val_accuracy'], label='валидация')
    plt.title(f'EarlyStopping\nТест: {acc_es:.3f}')
    plt.ylim(0, 1)
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

plot_history(hist_fixed, hist_es, acc_fixed, acc_es)

model_es.save('best_ns_model.h5')
print("Модель сохранена: best_ns_model.h5")
