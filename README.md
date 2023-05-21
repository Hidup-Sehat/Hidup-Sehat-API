# KITA LAPOR - API

API menggunakan FASTAPI & FIREBASE

# Instructions

## Setup

1. Clone Repo
2. Disarankan instal WSL. Jika tidak bisa langsung lompat ke-10
3. Instal python3.9. Jika pakai WSL bisa ikuti [langkah ini](https://linuxhint.com/install-python-ubuntu-22-04/).
4. Cek Python apakah sudah terinstal:

```
which python3.9
```

5. Instal pip pada WSL:

```
sudo apt install python3.9-distutils
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.9 get-pip.py

# clean up the installation file
rm get-pip.py
```

6. Cek apakah pip sudah terinstal pada WSL:

```
which pip3.9
```

7. Memasang Virtual Environment pada WSL:

```
apt-get install python3-venv
python3.9 -m pip install virtualenv
```

8. Buat Virtual Environment baru:

```
python3.9 -m venv hidup-sehat
```

9. Aktifkan Virtual Environment:

```
source hidup-sehat/bin/activate
```

10. Instal package-package yang terdaftar pada requirements.txt

```
pip3.9 install -r requirements.txt
```

11. Jalankan server dan mulai pengembangan

```
uvicorn app.main:app --reload
```

## Development

1. Aktifkan Virtual Environment:

```
source hidup-sehat/bin/activate
```

2. Jalankan server dan mulai pengembangan

```
uvicorn app.main:app --reload
```

API menjalankan berbagai layanan sebagai berikut:

Backend: http://localhost:8000/v1
Backend OpenAPI docs: http://localhost:8000/docs/