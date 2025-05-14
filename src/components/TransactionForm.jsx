import { useState, useEffect } from "react";
import { useAppContext } from "../contexts/AppContext";

export default function TransactionForm({ editingData, cancelEdit }) {
  const isEditing = Boolean(editingData);
  const { categories, addTransaction, updateTransaction } = useAppContext();

  const [form, setForm] = useState(editingData || {
    kategori_id: "",
    jumlah: "",
    jenis: "pengeluaran",
    deskripsi: "",
    tanggal: "",
  });

  useEffect(() => {
    if (editingData) {
      setForm(editingData);
    }
  }, [editingData]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (isEditing) {
      await updateTransaction(editingData.id, form);
      cancelEdit();
    } else {
      await addTransaction(form);
    }

    setForm({
      kategori_id: "",
      jumlah: "",
      jenis: "pengeluaran",
      deskripsi: "",
      tanggal: "",
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 p-4 border rounded shadow bg-white mb-6">
      <div>
        <label className="block font-medium">Deskripsi</label>
        <input
          name="deskripsi"
          value={form.deskripsi}
          onChange={handleChange}
          className="w-full border p-2 rounded"
          required
        />
      </div>

      <div>
        <label className="block font-medium">Kategori</label>
        <select
          name="kategori_id"
          value={form.kategori_id}
          onChange={handleChange}
          className="w-full border p-2 rounded"
          required
        >
          <option value="">Pilih Kategori</option>
          {categories.map((cat) => (
            <option key={cat.id} value={cat.id}>
              {cat.nama}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label className="block font-medium">Jumlah</label>
        <input
          type="number"
          name="jumlah"
          value={form.jumlah}
          onChange={handleChange}
          className="w-full border p-2 rounded"
          required
        />
      </div>

      <div>
        <label className="block font-medium">Jenis</label>
        <select
          name="jenis"
          value={form.jenis}
          onChange={handleChange}
          className="w-full border p-2 rounded"
        >
          <option value="pemasukan">Pemasukan</option>
          <option value="pengeluaran">Pengeluaran</option>
        </select>
      </div>

      <div>
        <label className="block font-medium">Tanggal</label>
        <input
          type="date"
          name="tanggal"
          value={form.tanggal}
          onChange={handleChange}
          className="w-full border p-2 rounded"
          required
        />
      </div>

      <button
        type="submit"
        className="bg-pink-600 hover:bg-pink-700 text-white"
      >
        {isEditing ? "Simpan Perubahan" : "Tambah Transaksi"}
      </button>
      {isEditing && (
        <button
          type="button"
          onClick={cancelEdit}
          className="ml-2 bg-gray-400 text-white px-4 py-2 rounded"
        >
          Batal
        </button>
      )}
    </form>
  );
}
