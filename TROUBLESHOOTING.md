# Troubleshooting Guide

> Pembaruan terakhir: 2 Juni 2025

## "Network Error" saat Menambah Kategori

Jika Anda mendapatkan error seperti ini:
```
AppContext.jsx:63 Gagal tambah kategori: AxiosError {message: 'Network Error', name: 'AxiosError', code: 'ERR_NETWORK', config: {…}, request: XMLHttpRequest, …}
```

Atau ini:
```
POST http://localhost:6543/api/categories net::ERR_FAILED
```

Atau error CORS seperti ini:
```
Access to XMLHttpRequest at 'http://localhost:6543/api/categories' from origin 'http://localhost:3000' has been blocked by CORS policy: Response to preflight request doesn't pass access control check
```

Berikut adalah langkah-langkah untuk mengatasinya:

### ✅ PERBAIKAN TERBARU: CORS Configuration Fix

**Status:** ✅ DIPERBAIKI - CORS configuration telah diupdate

Perubahan yang telah dilakukan:
1. **Updated `backend/app/views/cors.py`** - Menambahkan proper CORS headers untuk OPTIONS requests
2. **Updated `backend/app/routes.py`** - Memperbaiki routing untuk CORS preflight requests  
3. **Updated `frontend/src/contexts/AppContext.jsx`** - Menambahkan better CORS error handling

**Cara menggunakan perbaikan:**
1. Restart backend server dengan menjalankan: `restart_backend.bat`
2. Test CORS dengan: `.\test-cors.ps1` 
3. Refresh halaman frontend di browser

### 1. Pastikan Backend Server Berjalan

Server backend harus dijalankan sebelum frontend. Gunakan script `start-app.bat` dan pilih opsi `[1] Start both Backend and Frontend` atau `[2] Start Backend Only`.

### 2. Periksa Koneksi Database PostgreSQL

- Pastikan PostgreSQL service berjalan
- Cek bahwa database `budget_db` sudah dibuat
- Verifikasi kredensial di file `backend/development.ini` sudah benar

Anda bisa menggunakan script `test-database.bat` untuk memeriksa koneksi database secara otomatis.

### 3. Periksa Port 6543

Pastikan tidak ada aplikasi lain yang menggunakan port 6543. Jalankan perintah ini di command prompt:
```
netstat -ano | find "6543"
```

### 4. Reset Application

Jika masalah berlanjut:
1. Tutup semua terminal yang menjalankan aplikasi
2. Restart komputer
3. Jalankan PostgreSQL service
4. Mulai backend dan frontend dengan script `start-app.bat`

### 5. Diagnosis Komprehensif

Jika masalah masih berlanjut, jalankan script diagnostik:
```
powershell -File diagnose-backend.ps1
```

Script ini akan memeriksa:
- Status PostgreSQL service
- Lingkungan Python dan virtual environment
- Koneksi database
- Ketersediaan port 6543
- Mencoba menjalankan server backend untuk mengidentifikasi masalah

### 6. Pemecahan Masalah Lanjutan

#### CORS Issues
Jika Anda melihat error CORS di console, mungkin ada masalah dengan konfigurasi CORS di backend. Cek file `backend/app/__init__.py` dan pastikan CORS diatur dengan benar.

#### Database Errors
Jika database error, coba:
1. Connect ke PostgreSQL dengan pgAdmin atau psql
2. Buat ulang database `budget_db`
3. Restart backend server

#### Timeout Issues
Jika request timeout, coba:
1. Periksa firewall settings
2. Pastikan antivirus tidak memblokir koneksi
3. Coba restart router dan komputer

### 7. Menggunakan Tool Test API Browser

Untuk menguji API langsung:
1. Buka file `backend-test.html` di browser
2. Klik tombol "Test Categories API"
3. Cek apakah API merespon dengan benar

## Fitur-fitur Bantuan di Aplikasi

### Indikator Status Jaringan
Aplikasi sudah dilengkapi dengan fitur-fitur bantuan untuk mendeteksi masalah koneksi:

1. **Status Indikator** - Muncul di pojok kanan bawah saat backend tidak tersambung
2. **Tombol "Jalankan Backend"** - Membantu menjalankan backend secara cepat
3. **Notifikasi Error** - Pesan kesalahan yang lebih detail dan solusi
4. **Otomatis Reconnect** - Aplikasi akan otomatis mencoba kembali tersambung ke backend

### Script Diagnosa
Terdapat beberapa script yang bisa dijalankan untuk diagnosa:

1. `start-app.bat` - Menu lengkap untuk menjalankan aplikasi
2. `diagnose-backend.ps1` - Diagnostik lengkap untuk masalah backend
3. `test-database.bat` - Test khusus untuk koneksi database

Jalankan script-script ini jika mengalami masalah koneksi.
