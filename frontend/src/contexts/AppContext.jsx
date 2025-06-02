import { createContext, useContext, useEffect, useState, useCallback } from "react";
import axios from "axios";
import { API_URL, API_BASE_URL } from "../config";

const AppContext = createContext();

// Configure axios defaults
axios.defaults.headers.common["Content-Type"] = "application/json";
axios.defaults.headers.common["Accept"] = "application/json";
axios.defaults.timeout = 10000; // 10 seconds
axios.defaults.maxContentLength = 5 * 1024 * 1024; // 5MB
axios.defaults.maxBodyLength = 5 * 1024 * 1024; // 5MB

// Configure axios to handle CORS properly
axios.defaults.withCredentials = false;
axios.defaults.headers.common["X-Requested-With"] = "XMLHttpRequest";

// Add cache-busting to all requests
axios.interceptors.request.use(
  (config) => {
    // Add cache-busting parameter to prevent browser caching issues
    if (config.method === 'get') {
      config.params = { 
        ...config.params, 
        _t: new Date().getTime() 
      };
    }
    console.log(`🚀 Request: ${config.method.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error("❌ Request error:", error);
    return Promise.reject(error);
  }
);

// Add a response interceptor for debugging and error handling
axios.interceptors.response.use(
  (response) => {
    console.log(`✅ Response from ${response.config.url}:`, response.status);
    return response;
  },
  (error) => {
    if (error.response) {
      // Server responded with an error status
      console.error(`❌ Server error (${error.response.status}):`, error.response.data);
    } else if (error.request) {
      // Request was made but no response received
      console.error("❌ Network error - No response received:", error.message);
      if (error.code === 'ERR_NETWORK') {
        console.warn('Network error detected - Backend server might be down');
      }
    } else {
      // Something else happened
      console.error("❌ Error:", error.message);
    }
    return Promise.reject(error);
  }
);

export const AppProvider = ({ children }) => {
  const [transactions, setTransactions] = useState([]);
  const [categories, setCategories] = useState([]);
  const [backendStatus, setBackendStatus] = useState({ isOnline: true, lastChecked: null });

  // Check backend status
  const checkBackendStatus = useCallback(async () => {
    try {
      await axios.get(`${API_URL}/categories`, { timeout: 3000 });
      setBackendStatus({ isOnline: true, lastChecked: new Date() });
      return true;
    } catch (err) {
      setBackendStatus({ isOnline: false, lastChecked: new Date() });
      return false;
    }
  }, []);
  // ========== TRANSAKSI ==========
  const fetchTransactions = async () => {
    try {
      const res = await axios.get(`${API_URL}/transactions`);
      setTransactions(res.data);
      return { success: true, data: res.data };
    } catch (err) {
      console.error("Gagal fetch transaksi:", err);
      
      if (err.code === 'ERR_NETWORK') {
        console.warn("Koneksi ke server backend gagal. Pastikan server backend berjalan.");
      }
      
      return { success: false, message: "Gagal mengambil data transaksi" };
    }
  };
  const addTransaction = async (data) => {
    try {
      const response = await axios.post(`${API_URL}/transactions`, data);
      console.log("Transaction added:", response.data);
      fetchTransactions();
      return { success: true, message: "Transaksi berhasil ditambahkan" };
    } catch (err) {
      console.error("Gagal tambah transaksi:", err);
        let errorMessage = "Terjadi kesalahan saat menambahkan transaksi";
      
      if (err.code === 'ERR_NETWORK') {
        errorMessage = `Tidak dapat terhubung ke server. Pastikan server backend berjalan di ${API_BASE_URL}`;
        checkBackendStatus();
      }
      
      return { success: false, message: errorMessage };
    }
  };
  const updateTransaction = async (id, data) => {
    try {
      const response = await axios.put(`${API_URL}/transactions/${id}`, data);
      console.log("Transaction updated:", response.data);
      fetchTransactions();
      return { success: true, message: "Transaksi berhasil diupdate" };
    } catch (err) {
      console.error("Gagal update transaksi:", err);
        let errorMessage = "Terjadi kesalahan saat mengupdate transaksi";
      
      if (err.code === 'ERR_NETWORK') {
        errorMessage = `Tidak dapat terhubung ke server. Pastikan server backend berjalan di ${API_BASE_URL}`;
        checkBackendStatus();
      }
      
      return { success: false, message: errorMessage };
    }
  };

  const deleteTransaction = async (id) => {
    try {
      await axios.delete(`${API_URL}/transactions/${id}`);
      fetchTransactions();
    } catch (err) {
      console.error("Gagal hapus transaksi:", err);
    }
  };

  // ========== KATEGORI ==========
  const fetchCategories = async () => {
    try {
      const res = await axios.get(`${API_URL}/categories`);
      setCategories(res.data);
      return { success: true, data: res.data };
    } catch (err) {
      console.error("Gagal fetch kategori:", err);
      
      if (err.code === 'ERR_NETWORK') {
        console.warn("Koneksi ke server backend gagal. Pastikan server backend berjalan.");
      }
      
      return { success: false, message: "Gagal mengambil data kategori" };    }
  };
    const addCategory = async (data) => {
    try {
      console.log("Mengirim data kategori:", data);
      
      // Make sure data is valid
      if (!data || !data.nama) {
        throw new Error("Data kategori tidak valid");
      }
      
      // Send the request with timeout and retry logic
      let retries = 2;
      let lastError = null;
      
      while (retries >= 0) {
        try {
          const response = await axios.post(`${API_URL}/categories`, data, {
            headers: { 'Content-Type': 'application/json' },
            timeout: 5000
          });
          console.log("Server response:", response.data);
          await fetchCategories();
          return { success: true, message: "Kategori berhasil ditambahkan" };
        } catch (error) {
          lastError = error;
          if (error.code !== 'ERR_NETWORK' || retries === 0) {
            throw error;
          }
          retries--;
          await new Promise(resolve => setTimeout(resolve, 1000)); // Wait 1 second before retry
          console.log(`Mencoba kembali... Sisa percobaan: ${retries}`);
        }
      }
      
      throw lastError;    } catch (err) {
      console.error("Gagal tambah kategori:", err);
      
      let errorMessage = "Terjadi kesalahan saat menambahkan kategori";
      
      if (err.code === 'ERR_NETWORK') {
        errorMessage = `Tidak dapat terhubung ke server. Pastikan server backend berjalan di ${API_BASE_URL}`;
        // Check backend status and update it
        checkBackendStatus();
      } else if (err.message && err.message.includes('CORS')) {
        errorMessage = "Error CORS: Server tidak mengizinkan permintaan dari browser. Coba refresh halaman atau restart server backend.";
      } else if (err.response) {
        // Server merespon dengan status error
        errorMessage = `Error ${err.response.status}: ${err.response.data?.message || "Terjadi kesalahan pada server"}`;
      }
      
      return { success: false, message: errorMessage };
    }
  };
  const updateCategory = async (id, data) => {
    try {
      const response = await axios.put(`${API_URL}/categories/${id}`, data);
      console.log("Update category response:", response.data);
      fetchCategories();
      return { success: true, message: "Kategori berhasil diupdate" };
    } catch (err) {
      console.error("Gagal update kategori:", err);
        let errorMessage = "Terjadi kesalahan saat mengupdate kategori";
      
      if (err.code === 'ERR_NETWORK') {
        errorMessage = `Tidak dapat terhubung ke server. Pastikan server backend berjalan di ${API_BASE_URL}`;
        checkBackendStatus();
      }
      
      return { success: false, message: errorMessage };
    }
  };

  const deleteCategory = async (id) => {
    try {
      await axios.delete(`${API_URL}/categories/${id}`);
      fetchCategories();
    } catch (err) {
      console.error("Gagal hapus kategori:", err);
    }
  };
  // Check backend status periodically
  useEffect(() => {
    // Initial check
    checkBackendStatus();
    
    // Set up interval for periodic checks
    const intervalId = setInterval(() => {
      checkBackendStatus();
    }, 30000); // Check every 30 seconds
    
    // Clean up interval on unmount
    return () => clearInterval(intervalId);
  }, [checkBackendStatus]);

  // ========== AUTO FETCH SAAT MOUNT ==========
  useEffect(() => {
    fetchTransactions();
    fetchCategories();
  }, []);
  return (
    <AppContext.Provider
      value={{
        transactions,
        categories,
        backendStatus,
        fetchTransactions,
        fetchCategories,
        addTransaction,
        updateTransaction,
        deleteTransaction,
        addCategory,
        updateCategory,
        deleteCategory,
        checkBackendStatus,
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

export const useAppContext = () => useContext(AppContext);
