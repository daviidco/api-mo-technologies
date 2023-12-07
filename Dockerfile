# Usa una imagen base de Python
FROM python:3.9

# Establece la variable de entorno PYTHONUNBUFFERED para evitar problemas con la salida de Python
ENV PYTHONUNBUFFERED 1

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo requirements.txt y realiza la instalación de dependencias
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación al contenedor
COPY . /app/

# Ejecuta las migraciones cuando se inicie el contenedor
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

# Expone el puerto en el que se ejecuta la aplicación Django
EXPOSE 8080

# Ejecuta la aplicación Django
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "4", "technical_test.wsgi:application"]


