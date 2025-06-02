import { useState } from "react";
import { useAppContext } from "../contexts/AppContext";
import TransactionForm from "../components/TransactionForm";

export default function Transactions() {
  const { transactions, deleteTransaction, categories } = useAppContext();
  const [editingData, setEditingData] = useState(null);

  const getKategoriNama = (id) => {
    const found = categories.find((cat) => cat.id === id);
    return found ? found.nama : "-";
  };

  const formatTanggal = (tanggal) => {
    const date = new Date(tanggal);
    return date.toLocaleDateString("id-ID");
  };

  const totalPemasukan = transactions
    .filter((t) => t.jenis === "pemasukan")
    .reduce((sum, t) => sum + t.jumlah, 0);

  const totalPengeluaran = transactions
    .filter((t) => t.jenis === "pengeluaran")
    .reduce((sum, t) => sum + t.jumlah, 0);

  const saldo = totalPemasukan - totalPengeluaran;
  return (
    <div className="p-6 bg-gradient-to-br from-pink-50 via-purple-50 to-indigo-50 min-h-screen">
      {/* Header Section */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-pink-600 to-purple-600 mb-2 flex items-center">
          <svg className="w-10 h-10 mr-3 text-pink-600" fill="currentColor" viewBox="0 0 20 20">
            <path d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z" />
          </svg>
          Kelola Transaksi
        </h1>
        <p className="text-gray-600 text-lg">Tambah, edit, dan pantau semua transaksi keuangan Anda</p>
      </div>

      {/* Summary Cards */}
      <div className="grid md:grid-cols-3 gap-6 mb-8">
        {/* Total Pemasukan */}
        <div className="bg-gradient-to-br from-green-400 to-emerald-500 text-white p-6 rounded-xl shadow-lg transform hover:scale-105 transition-all duration-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-green-100 text-sm font-medium mb-1">Total Pemasukan</p>
              <h3 className="text-2xl font-bold">Rp{totalPemasukan.toLocaleString("id-ID")}</h3>
              <p className="text-green-100 text-xs mt-1">💰 Pendapatan</p>
            </div>
            <div className="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center">
              <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.293l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13a1 1 0 102 0V9.414l1.293 1.293a1 1 0 001.414-1.414z" clipRule="evenodd" />
              </svg>
            </div>
          </div>
        </div>

        {/* Total Pengeluaran */}
        <div className="bg-gradient-to-br from-red-400 to-rose-500 text-white p-6 rounded-xl shadow-lg transform hover:scale-105 transition-all duration-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-red-100 text-sm font-medium mb-1">Total Pengeluaran</p>
              <h3 className="text-2xl font-bold">Rp{totalPengeluaran.toLocaleString("id-ID")}</h3>
              <p className="text-red-100 text-xs mt-1">💸 Pengeluaran</p>
            </div>
            <div className="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center">
              <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v3.586L7.707 9.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L11 10.586V7z" clipRule="evenodd" />
              </svg>
            </div>
          </div>
        </div>

        {/* Saldo */}
        <div className={`bg-gradient-to-br ${saldo >= 0 ? 'from-blue-400 to-indigo-500' : 'from-orange-400 to-red-500'} text-white p-6 rounded-xl shadow-lg transform hover:scale-105 transition-all duration-200`}>
          <div className="flex items-center justify-between">
            <div>
              <p className={`${saldo >= 0 ? 'text-blue-100' : 'text-orange-100'} text-sm font-medium mb-1`}>Saldo Saat Ini</p>
              <h3 className="text-2xl font-bold">Rp{saldo.toLocaleString("id-ID")}</h3>
              <p className={`${saldo >= 0 ? 'text-blue-100' : 'text-orange-100'} text-xs mt-1`}>
                {saldo >= 0 ? '📈 Surplus' : '⚠️ Defisit'}
              </p>
            </div>
            <div className="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center">
              <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 6a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM4 14a1 1 0 100 2h12a1 1 0 100-2H4z" clipRule="evenodd" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      {/* Add/Edit Transaction Form */}
      <div className="bg-white rounded-xl shadow-lg p-6 mb-8 border border-pink-100">
        <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
          <svg className="w-6 h-6 mr-2 text-pink-500" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
          </svg>
          {editingData ? 'Edit Transaksi' : 'Tambah Transaksi Baru'}
        </h3>
        <TransactionForm
          editingData={editingData}
          cancelEdit={() => setEditingData(null)}
        />
      </div>

      {/* Transactions History */}
      <div className="bg-white rounded-xl shadow-lg border border-pink-100 overflow-hidden">
        <div className="bg-gradient-to-r from-pink-500 to-purple-600 px-6 py-4">
          <h2 className="text-xl font-semibold text-white flex items-center">
            <svg className="w-6 h-6 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
            </svg>
            Histori Transaksi ({transactions.length})
          </h2>
          <p className="text-pink-100 text-sm">Semua transaksi yang telah dicatat</p>
        </div>
        
        <div className="p-6">
          {transactions.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              <svg className="w-16 h-16 mx-auto mb-4 text-gray-300" fill="currentColor" viewBox="0 0 20 20">
                <path d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z" />
              </svg>
              <p className="text-xl font-semibold text-gray-400 mb-2">Belum ada transaksi</p>
              <p className="text-gray-400">Mulai tambahkan transaksi pertama Anda</p>
            </div>
          ) : (
            <div className="space-y-4">
              {transactions.map((t) => (
                <div
                  key={t.id}
                  className="bg-gradient-to-r from-pink-50 to-purple-50 border border-pink-200 p-5 rounded-lg hover:shadow-md transition-all duration-200 transform hover:-translate-y-1"
                >
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center mb-2">
                        <div className={`w-3 h-3 rounded-full mr-3 ${t.jenis === 'pemasukan' ? 'bg-green-400' : 'bg-red-400'}`}></div>
                        <h4 className="text-gray-800 font-semibold text-lg">{t.deskripsi}</h4>
                        <span className={`ml-2 px-2 py-1 rounded-full text-xs font-medium ${
                          t.jenis === 'pemasukan' 
                            ? 'bg-green-100 text-green-700' 
                            : 'bg-red-100 text-red-700'
                        }`}>
                          {t.jenis}
                        </span>
                      </div>
                      
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-2 text-sm text-gray-600">
                        <div className="flex items-center">
                          <svg className="w-4 h-4 mr-1 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z" />
                          </svg>
                          <span className="font-semibold">Rp{t.jumlah.toLocaleString("id-ID")}</span>
                        </div>
                        <div className="flex items-center">
                          <svg className="w-4 h-4 mr-1 text-purple-500" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
                          </svg>
                          <span>{getKategoriNama(t.kategori_id)}</span>
                        </div>
                        <div className="flex items-center">
                          <svg className="w-4 h-4 mr-1 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clipRule="evenodd" />
                          </svg>
                          <span>{formatTanggal(t.tanggal)}</span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex space-x-2 ml-4">
                      <button
                        onClick={() => setEditingData(t)}
                        className="bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 transform hover:scale-105 shadow-sm flex items-center"
                      >
                        <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                          <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                        </svg>
                        Edit
                      </button>
                      <button
                        onClick={() => {
                          if (window.confirm(`Apakah Anda yakin ingin menghapus transaksi "${t.deskripsi}"?`)) {
                            deleteTransaction(t.id);
                          }
                        }}
                        className="bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 transform hover:scale-105 shadow-sm flex items-center"
                      >
                        <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" clipRule="evenodd" />
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8 7a1 1 0 012 0v4a1 1 0 11-2 0V7zM12 7a1 1 0 012 0v4a1 1 0 11-2 0V7z" clipRule="evenodd" />
                        </svg>
                        Hapus
                      </button>
                    </div>
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
