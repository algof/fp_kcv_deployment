# Deployment FP KCV

## Deployment di Railway

**Prerequisites:** punya akun GitHub dan repositories app yang fungsional

1. [https://railway.com](https://railway.com/)
2. Buka website di atas dan login dengan akun GitHub
3. Pastikan di GitHub sudah ada repositories yang siap deployment
4. Isi repositories : Dockerfile, main.py, requirements.txt, model
5. `Deploy a new project`
6. `Deploy from GitHub repo`
7. Pilih repo yang ingin di deploy 

## Deployment di Micrososft Azure

**Prerequisites:** : punya akun Microsoft Azure (free dari ITS)

1. [Azure](https://portal.azure.com/?Microsoft_Azure_Education_correlationId=c3c8a54e-f40c-4302-bd0a-015bc9a32c1a&Microsoft_Azure_Education_newA4E=true&Microsoft_Azure_Education_asoSubGuid=61a18394-4bb9-4f30-b719-636db39a8490#home)
2. Buka link di atas, pilih `Virtual machines`
3. Pilih `Create`, klik `Azure virtual machine`
4. Isi atribut-atribut form
    - `Resource group` : Create new
    - `Virtual machine name` : your_vm_name_here
    - `Region` : (Asia Pasific) Australia East
    - `Availability options` :  Availability zone
    - `Zone options` : Self-selected zone
    - `Security type` : Trusted launch virtual machines
    - `Image` : Ubuntu Server 22.04 LTS - x64 Gen2
    - `VM architecture` : x64
    - `Run with Azure Spot discount` : `Check` (Opsional)
    - `Authentication type` : SSH public key
    - `Username` : azureuser
    - `SSH public key source` : Generate new key pair
    - `SSH Key Type` : RSA SSH Format
    - `Key pair name` : your_key_name_here (untuk connect SSH dari local kita)
    - `Public inbound ports` : Allow selected ports
    - `Select inbound ports` : Check HTTP (80), HTTPS (443), dan SSH (22)
5. Review + create
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
Jika ingin akses tanpa lewat port 8501 dan reverse proxy
```sh
docker run -d -p 80:8501 fp_kcv
*-d buat daemon
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