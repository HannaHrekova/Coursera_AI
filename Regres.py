from sklearn.linear_model import LinearRegression
import numpy as np

# Приклад даних: площа будинків (квадратні метри) та їх ціна (тисячі доларів)
X = np.array([[50], [100], [150], [200], [250]])  # площа
y = np.array([150, 300, 450, 600, 750])  # ціна

# Створюємо модель
model = LinearRegression()
model.fit(X, y)  # Навчаємо модель на даних

# Передбачаємо ціну для будинку з площею 120 квадратних метрів
predicted_price = model.predict([[120]])
print(f"Передбачувана ціна для будинку площею 120 м²: ${predicted_price[0]:.2f} тисяч")