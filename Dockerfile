# Utilizar una imagen base de Python
FROM python:3.9

# Establecer el directorio de trabajo en el contenedor
WORKDIR /code

# Copiar los archivos de requisitos e instalar las dependencias
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copiar el resto del código
COPY . /code/

# Exponer el puerto 80
EXPOSE 80

# Comando para ejecutar migraciones y luego iniciar la API
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 80"]