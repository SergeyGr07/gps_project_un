import serial

# Открываем последовательный порт
ser = serial.Serial('COM1', 9600)

# Открываем файл для записи данных
with open('data.txt', 'w') as f:
    # Бесконечный цикл для чтения данных
    while True:
        # Читаем строку из последовательного порта
        line = ser.readline().decode().strip()
        # Записываем строку в файл
        f.write(line + '\n')
        # Сбрасываем буфер записи файла
        f.flush()


