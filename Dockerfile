# Usa una imagen base de Python
FROM python:3.11-slim

# Configura el directorio de trabajo
WORKDIR /app

# Copia los archivos de tu proyecto al contenedor
COPY . /app

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto en el que tu aplicación escuchará
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "utils/app.py"]
