# ========== STAGE 1: BUILD ==========
FROM python:3.10-slim

WORKDIR /app

# Salin file requirements
COPY requirements.txt .

# Salin model weight and infrastructure
COPY model.pt .

# Install dependencies ke folder terpisah
RUN pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt

# Salin source code
COPY main.py .

# Jalankan aplikasi
CMD ["streamlit", "run", "main.py"]