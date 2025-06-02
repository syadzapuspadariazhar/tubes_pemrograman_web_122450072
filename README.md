# 💰 Budget Tracker - Aplikasi Manajemen Keuangan Personal
Syadza Puspadari Azhar - 122450072 - Tugas Besar Pemrograman Web 2025

## 📝 Deskripsi Aplikasi

Budget Tracker adalah aplikasi web modern untuk manajemen keuangan personal yang memungkinkan pengguna untuk:
- Melacak pemasukan dan pengeluaran secara real-time
- Mengategorikan transaksi untuk analisis yang lebih baik
- Memvisualisasikan data keuangan dengan grafik interaktif
- Mengelola anggaran bulanan dengan interface yang intuitif
- Melihat tren pengeluaran harian untuk kontrol keuangan yang lebih baik

Aplikasi ini dibangun dengan teknologi modern dan menggunakan arsitektur full-stack dengan React.js untuk frontend dan Python Pyramid untuk backend.

## ✨ Fitur Utama

### 🔐 **Sistem Autentikasi**
- Login dengan JWT (JSON Web Token)
- Session management yang aman
- Proteksi route untuk keamanan data
- Toggle visibility password untuk kemudahan input

### 📊 **Dashboard Keuangan**
- **Ringkasan Finansial**: Tampilan overview pemasukan, pengeluaran, dan saldo
- **Grafik Pie Chart**: Visualisasi distribusi keuangan
- **Grafik Trend Harian**: Line chart pengeluaran 7 hari terakhir
- **Smart Color Coding**: Indikator visual untuk status keuangan

### 💳 **Manajemen Transaksi**
- Tambah, edit, dan hapus transaksi
- Kategorisasi otomatis transaksi
- Filter berdasarkan jenis (pemasukan/pengeluaran)
- Konfirmasi dialog untuk aksi penting
- Form validation yang komprehensif

### 🏷️ **Manajemen Kategori**
- CRUD operations untuk kategori kustom
- Interface drag-and-drop friendly
- Pengelompokan transaksi berdasarkan kategori
- Visual indicators dengan warna-warna menarik

### 🎨 **UI/UX Modern**
- **Responsive Design**: Optimal di desktop, tablet, dan mobile
- **Gradient Theme**: Pink-purple gradient yang elegan
- **Interactive Elements**: Hover effects dan smooth transitions
- **Card-based Layout**: Design modern dengan shadow effects
- **Loading States**: Feedback visual untuk semua operasi
- **Empty States**: Panduan user-friendly saat belum ada data

## 🛠️ Dependensi dan Library

### **Backend (Python/Pyramid)**
```txt
pyramid==2.0.2          # Web framework utama
waitress==2.1.2         # WSGI server untuk production
pyramid_tm==2.5         # Transaction manager
SQLAlchemy==1.4.46      # ORM untuk database operations
pyramid_debugtoolbar    # Development debugging tools
pyramid_retry==2.1.1    # Retry mechanism untuk reliability
webtest==3.0.0          # Testing framework
PyJWT==2.8.0           # JSON Web Token untuk autentikasi
```

### **Frontend (React.js)**
```json
{
  "dependencies": {
    "react": "^18.2.0",           // Core React library
    "react-dom": "^18.2.0",       // React DOM renderer
    "react-router-dom": "^6.20.0", // Client-side routing
    "axios": "^1.6.2",            // HTTP client untuk API calls
    "recharts": "^2.15.3",        // Chart library untuk visualisasi
    "react-scripts": "5.0.1"      // Build tools dan configuration
  },
  "devDependencies": {
    "tailwindcss": "^3.4.1",      // Utility-first CSS framework
    "autoprefixer": "^10.4.21",   // CSS vendor prefixing
    "postcss": "^8.5.3"           // CSS transformation tool
  }
}
```

## 🏗️ Arsitektur Sistem

### **Overview Arsitektur**
```
┌─────────────────┐    HTTP/REST API    ┌──────────────────┐
│   Frontend      │◄──────────────────► │    Backend       │
│   (React.js)    │    Port 3000        │   (Python)       │
│   Port 3000     │                     │   Port 6543      │
└─────────────────┘                     └──────────────────┘
                                                │
                                                ▼
                                        ┌──────────────────┐
                                        │    Database      │
                                        │   (SQLite)       │
                                        │   budget.db      │
                                        └──────────────────┘
```

### **Backend Architecture (Python Pyramid)**

#### **📁 Struktur Backend**
```
backend/
├── app/
│   ├── __init__.py          # Konfigurasi aplikasi Pyramid
│   ├── auth.py              # JWT authentication system
│   ├── routes.py            # URL routing configuration
│   ├── models/
│   │   ├── __init__.py      # Database model definitions
│   │   ├── user.py          # User model
│   │   ├── category.py      # Category model
│   │   └── transaction.py   # Transaction model
│   └── views/
│       ├── __init__.py      # View configurations
│       ├── category_api.py  # Category CRUD endpoints
│       └── transaction_api.py # Transaction CRUD endpoints
├── development.ini          # Development configuration
├── production.ini           # Production configuration
├── requirements.txt         # Python dependencies
├── setup.py                # Package setup configuration
└── budget.db               # SQLite database file
```

#### **🔧 Backend Components**

1. **Database Layer (SQLAlchemy ORM)**
   - **User Model**: Sistem autentikasi pengguna
   - **Category Model**: Kategori transaksi yang dapat dikustomisasi
   - **Transaction Model**: Data transaksi keuangan dengan foreign key relationships

2. **API Layer (RESTful Endpoints)**
   - **Authentication API**: `/api/login`, `/api/logout`
   - **Categories API**: `/api/categories` (GET, POST, PUT, DELETE)
   - **Transactions API**: `/api/transactions` (GET, POST, PUT, DELETE)

3. **Security Layer**
   - **JWT Token Management**: Secure token generation dan validation
   - **CORS Configuration**: Cross-origin resource sharing untuk frontend
   - **Input Validation**: Server-side validation untuk semua endpoints

### **Frontend Architecture (React.js)**

#### **📁 Struktur Frontend**
```
frontend/
├── public/
│   ├── index.html           # HTML template utama
│   └── favicon.ico          # Application icon
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── ProtectedRoute.jsx
│   │   └── Navbar.jsx
│   ├── contexts/            # React Context untuk state management
│   │   ├── AppContext.js    # Global application state
│   │   └── AuthContext.js   # Authentication state
│   ├── pages/               # Page-level components
│   │   ├── Login.jsx        # Login page dengan password toggle
│   │   ├── Dashboard.jsx    # Dashboard dengan charts
│   │   ├── Categories.jsx   # Category management
│   │   └── Transactions.jsx # Transaction management
│   ├── hooks/               # Custom React hooks
│   ├── utils/               # Utility functions
│   ├── config.js            # API configuration
│   ├── App.jsx              # Main application component
│   └── index.js             # Application entry point
├── package.json             # Dependencies dan scripts
└── tailwind.config.js       # Tailwind CSS configuration
```

#### **⚛️ Frontend Components**

1. **State Management**
   - **AuthContext**: User authentication state dan JWT token management
   - **AppContext**: Global state untuk categories, transactions, dan UI state

2. **Routing System**
   - **React Router**: Client-side routing dengan protected routes
   - **Route Protection**: Authentication-based access control

3. **UI Components**
   - **Responsive Design**: Mobile-first approach dengan Tailwind CSS
   - **Interactive Charts**: Recharts library untuk data visualization
   - **Modern UI Elements**: Gradient themes, hover effects, loading states

## 🚀 Cara Menjalankan Aplikasi

### **Prerequisites**
- Python 3.8+ 
- Node.js 16+
- npm atau yarn

### **Setup Backend**
```bash
# 1. Masuk ke direktori backend
cd backend

# 2. Install dependencies Python
pip install -r requirements.txt

# 3. Jalankan server backend
python -m pyramid.scripts.pserve development.ini --reload
```
Backend akan berjalan di: `http://localhost:6543`

### **Setup Frontend**
```bash
# 1. Masuk ke direktori frontend  
cd frontend

# 2. Install dependencies Node.js
npm install

# 3. Jalankan development server
npm start
```
Frontend akan berjalan di: `http://localhost:3000`

### **Login Credentials**
Gunakan salah satu akun demo berikut:
- **Username**: `admin` | **Password**: `admin123`
- **Username**: `demo` | **Password**: `demo123`

## 🎯 API Endpoints

### **Authentication**
- `POST /api/login` - User login dengan JWT token
- `POST /api/logout` - User logout

### **Categories**
- `GET /api/categories` - Ambil semua kategori
- `POST /api/categories` - Tambah kategori baru
- `PUT /api/categories/{id}` - Update kategori
- `DELETE /api/categories/{id}` - Hapus kategori

### **Transactions**
- `GET /api/transactions` - Ambil semua transaksi
- `POST /api/transactions` - Tambah transaksi baru
- `PUT /api/transactions/{id}` - Update transaksi
- `DELETE /api/transactions/{id}` - Hapus transaksi

## 🔒 Keamanan

- **JWT Authentication**: Token-based authentication untuk API security
- **CORS Protection**: Configured untuk mencegah unauthorized access
- **Input Validation**: Server-side dan client-side validation
- **SQL Injection Protection**: Menggunakan SQLAlchemy ORM untuk query safety
- **XSS Prevention**: React's built-in XSS protection

## 📱 Responsive Design

Aplikasi ini fully responsive dan optimal untuk:
- **Desktop**: Full feature experience dengan dual-chart layout
- **Tablet**: Adaptive layout dengan stacked components  
- **Mobile**: Touch-friendly interface dengan simplified navigation

## 🎨 Design System

- **Color Palette**: Pink-purple gradient theme (#ec4899, #8b5cf6, #6366f1)
- **Typography**: Modern font stack dengan proper hierarchy
- **Components**: Card-based design dengan consistent spacing
- **Animations**: Smooth 200ms transitions untuk semua interactions
- **Icons**: SVG icons untuk sharp rendering di semua devices

## 📈 Fitur Visualisasi Data

1. **Pie Chart**: Distribusi pemasukan vs pengeluaran
2. **Line Chart**: Trend pengeluaran harian (7 hari terakhir)
3. **Summary Cards**: Visual indicators dengan gradient backgrounds
4. **Interactive Tooltips**: Hover information dengan formatted currency
5. **Empty States**: User-friendly messaging ketika belum ada data

---

*💡 Budget Tracker - Kelola Keuangan dengan Mudah dan Modern!*

1. Python 3.11+
2. Node.js 19+
3. PostgreSQL 16+ (perlu diinstall dan running)
4. Git (opsional)

## Informasi Tambahan

- Backend API tersedia di: http://localhost:6543/api
- Frontend tersedia di: http://localhost:3000
