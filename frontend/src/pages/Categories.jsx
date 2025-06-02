import { useState } from "react";
import { useAppContext } from "../contexts/AppContext";

export default function Categories() {
  const { categories, addCategory, updateCategory, deleteCategory } = useAppContext();
  const [form, setForm] = useState({ nama: "" });
  const [editingId, setEditingId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate input
    if (!form.nama || form.nama.trim() === "") {
      setError("Nama kategori tidak boleh kosong");
      return;
    }
    
    setIsLoading(true);
    setError(null);
    
    try {
      if (editingId) {
        const result = await updateCategory(editingId, form);
        if (!result.success) {
          setError(result.message);
        } else {
          setForm({ nama: "" });
          setEditingId(null);
        }
      } else {
        console.log("Mengirim data kategori:", form);
        const result = await addCategory(form);
        if (!result.success) {
          setError(result.message);
        } else {
          setForm({ nama: "" });
        }
      }
    } catch (err) {
      setError("Terjadi kesalahan: " + (err.message || "Unknown error"));
      console.error("Error in handleSubmit:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleEdit = (cat) => {
    setForm({ nama: cat.nama });
    setEditingId(cat.id);
  };

  const handleCancel = () => {
    setForm({ nama: "" });
    setEditingId(null);
  };

  return (
    <div className="p-6 bg-gradient-to-br from-pink-50 via-purple-50 to-indigo-50 min-h-screen">
      {/* Header Section */}
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-pink-600 to-purple-600 mb-2 flex items-center">
          <svg className="w-8 h-8 mr-3 text-pink-600" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
          </svg>
          Kelola Kategori
        </h2>
        <p className="text-gray-600">Atur kategori untuk mengorganisir transaksi Anda dengan lebih baik</p>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border-l-4 border-red-400 text-red-700 px-6 py-4 rounded-lg mb-6 flex justify-between items-start animate-fadeIn shadow-sm">
          <div className="flex">
            <svg className="w-5 h-5 mr-2 mt-0.5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <div>
              <span className="font-semibold">Error: </span>
              <span>{error}</span>
              {error.includes("Tidak dapat terhubung") && (
                <div className="text-sm mt-2 space-x-2">
                  <button 
                    onClick={() => window.location.reload()}
                    className="inline-flex items-center px-3 py-1 bg-red-100 hover:bg-red-200 text-red-700 rounded-md text-sm font-medium transition-colors"
                  >
                    🔄 Muat ulang halaman
                  </button>
                  <button 
                    onClick={() => {
                      if (window.confirm('Apakah Anda ingin menjalankan script diagnosa?')) {
                        alert('Buka terminal dan jalankan file diagnose-backend.ps1');
                      }
                    }}
                    className="inline-flex items-center px-3 py-1 bg-red-100 hover:bg-red-200 text-red-700 rounded-md text-sm font-medium transition-colors"
                  >
                    🔍 Jalankan diagnosa
                  </button>
                </div>
              )}
            </div>
          </div>
          <button 
            onClick={() => setError(null)} 
            className="text-red-400 hover:text-red-600 text-xl font-bold leading-none"
          >
            ×
          </button>
        </div>
      )}

      {/* Add/Edit Form */}
      <div className="bg-white rounded-xl shadow-lg p-6 mb-8 border border-pink-100">
        <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
          <svg className="w-5 h-5 mr-2 text-pink-500" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
          </svg>
          {editingId ? "Edit Kategori" : "Tambah Kategori Baru"}
        </h3>
        
        <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-3">
          <input
            type="text"
            value={form.nama}
            onChange={(e) => setForm({ nama: e.target.value })}
            className="flex-1 border border-pink-300 focus:ring-2 focus:ring-pink-400 focus:border-pink-400 p-3 rounded-lg placeholder-gray-400 transition-all duration-200"
            placeholder="Masukkan nama kategori (contoh: Makanan, Transportasi, Hiburan)"
            required
            disabled={isLoading}
          />
          <div className="flex gap-2">
            <button
              type="submit"
              className={`${
                isLoading 
                  ? 'bg-pink-400 cursor-not-allowed' 
                  : 'bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 transform hover:scale-105'
              } text-white px-6 py-3 rounded-lg font-medium transition-all duration-200 shadow-md whitespace-nowrap flex items-center`}
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Loading...
                </>
              ) : editingId ? (
                <>💾 Simpan</>
              ) : (
                <>➕ Tambah</>
              )}
            </button>
            {editingId && (
              <button
                type="button"
                onClick={handleCancel}
                className="bg-gray-400 hover:bg-gray-500 text-white px-6 py-3 rounded-lg font-medium transition-all duration-200 shadow-md transform hover:scale-105"
                disabled={isLoading}
              >
                ❌ Batal
              </button>
            )}
          </div>
        </form>
      </div>

      {/* Categories List */}
      <div className="bg-white rounded-xl shadow-lg border border-pink-100 overflow-hidden">
        <div className="bg-gradient-to-r from-pink-500 to-purple-600 px-6 py-4">
          <h3 className="text-xl font-semibold text-white flex items-center">
            <svg className="w-6 h-6 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
            </svg>
            Daftar Kategori ({categories.length})
          </h3>
        </div>
        
        <div className="p-6">
          {categories.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              <svg className="w-16 h-16 mx-auto mb-4 text-gray-300" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
              </svg>
              <p className="text-xl font-semibold text-gray-400 mb-2">Belum ada kategori</p>
              <p className="text-gray-400">Tambahkan kategori pertama Anda untuk mulai mengorganisir transaksi</p>
            </div>
          ) : (
            <div className="grid gap-4">
              {categories.map((cat, index) => (
                <div
                  key={cat.id}
                  className="flex justify-between items-center bg-gradient-to-r from-pink-50 to-purple-50 border border-pink-200 p-4 rounded-lg hover:shadow-md transition-all duration-200 transform hover:-translate-y-1"
                >
                  <div className="flex items-center">
                    <div className="w-4 h-4 bg-gradient-to-r from-pink-400 to-purple-500 rounded-full mr-4 flex-shrink-0"></div>
                    <div>
                      <span className="text-gray-800 font-semibold text-lg">{cat.nama}</span>
                      <p className="text-sm text-gray-500">Kategori #{index + 1}</p>
                    </div>
                  </div>
                  <div className="flex space-x-2">
                    <button
                      onClick={() => handleEdit(cat)}
                      className="bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 transform hover:scale-105 shadow-sm flex items-center"
                    >
                      <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                      </svg>
                      Edit
                    </button>
                    <button
                      onClick={() => {
                        if (window.confirm(`Apakah Anda yakin ingin menghapus kategori "${cat.nama}"?`)) {
                          deleteCategory(cat.id);
                        }
                      }}
                      className="bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 transform hover:scale-105 shadow-sm flex items-center"
                    >                      <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" clipRule="evenodd" />
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8 7a1 1 0 012 0v4a1 1 0 11-2 0V7zM12 7a1 1 0 012 0v4a1 1 0 11-2 0V7z" clipRule="evenodd" />
                      </svg>
                      Hapus
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
