FROM python:3.11

WORKDIR /app

ENV SECRET_KEY=django-insecure-$t(32!@1!_t&tsrfgd@()!&gmjcu&=d&03--wu4qc8@4oxe32i
ENV DEBUG=True
ENV ALLOWED_HOSTS=*

ENV API_URL=http://localhost:8000/

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
