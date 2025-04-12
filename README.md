# Deployment FP KCV

## Langkah-langkah Deployment di Railway
1. [https://railway.com](https://railway.com/)
2. Buka website di atas dan login dengan akun GitHub
3. Pastikan di GitHub sudah ada repositories yang siap deployment
4. Isi repositories : Dockerfile, main.py, requirements.txt, model.pt
5. `Deploy a new project`
6. `Deploy from GitHub repo`
7. Pilih repo yang ingin di deploy 

## Langkah-langkah Deployment di Micrososft Azure
```sh
sudo apt-get update
sudo apt install docker.io

git clone https://github.com/algof/fp_kcv_deployment.git

cd fp_kcv_deployment

sudo docker build -t "image_name_here" .

sudo docker run -d -p 8501:8501 fp-kcv
*-d buat daemon

add new inbound rule for port 8501
add new DNS

akses lewat DNS:8501 atau VM_PUBLIC_IP:8501
```

# Langkah-langkah reverse proxy di Microsoft Azure
```sh
sudo apt install nginx
```
```sh
sudo systemctl status nginx
```
```sh
cd /etc/nginx/
```
```sh
sudo nano nginx.conf
```
uncomment server_names_hash_bucket_size <br>
ganti size ke 128

```sh
sudo nano /etc/nginx/sites-available/streamlit.com
```
```conf
server {
    listen 80;
    server_name dapagantenk.australiaeast.cloudapp.azure.com;

    client_max_body_size 200M;

    location / {
        proxy_pass http://localhost:8501;

        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # Basic headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_redirect off;
    }
}
```
```sh
sudo ln -s /etc/nginx/sites-available/streamlit.com /etc/nginx/sites-enabled
```
```sh
sudo nginx -t
```

```sh
sudo systemctl restart nginx
```
Coba akses tanpa port