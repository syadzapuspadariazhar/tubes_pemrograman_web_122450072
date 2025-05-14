import { useState } from "react";
import { useAppContext } from "../contexts/AppContext";
import TransactionForm from "../components/TransactionForm";

export default function Transactions() {
  const { transactions, deleteTransaction } = useAppContext();
  const [editingData, setEditingData] = useState(null);

  return (
    <div className="p-6 bg-pink-50 min-h-screen">
      <h1 className="text-3xl font-bold mb-6 text-pink-600">💸 Daftar Transaksi</h1>

      {/* Form Input */}
      <div className="bg-white p-4 rounded-lg shadow-md">
        <TransactionForm
          editingData={editingData}
          cancelEdit={() => setEditingData(null)}
        />
      </div>

      <div className="mt-10">
        <h2 className="text-2xl font-semibold mb-4 text-pink-500 border-b border-pink-300 pb-2">
          📝 Histori Transaksi
        </h2>
        {transactions.length === 0 ? (
          <p className="text-gray-500 italic">Belum ada transaksi.</p>
        ) : (
          <ul className="space-y-3">
            {transactions.map((t) => (
              <li
                key={t.id}
                className="bg-white p-4 rounded-lg shadow flex justify-between items-center"
              >
                <div>
                  <strong className="text-pink-700">{t.deskripsi}</strong>{" "}
                  - Rp{t.jumlah.toLocaleString("id-ID")}{" "}
                  <span className="italic text-sm text-gray-600">({t.jenis})</span>
                </div>
                <div className="space-x-2">
                  <button
                    onClick={() => setEditingData(t)}
                    className="bg-pink-400 hover:bg-pink-300 text-white px-3 py-1 rounded text-sm transition"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => deleteTransaction(t.id)}
                    className="bg-pink-600 hover:bg-pink-500 text-white px-3 py-1 rounded text-sm transition"
                  >
                    Hapus
                  </button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
