import { useState } from "react";
import { useAppContext } from "../contexts/AppContext";

export default function Categories() {
  const { categories, addCategory, updateCategory, deleteCategory } = useAppContext();
  const [form, setForm] = useState({ nama: "" });
  const [editingId, setEditingId] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (editingId) {
      await updateCategory(editingId, form);
      setEditingId(null);
    } else {
      await addCategory(form);
    }
    setForm({ nama: "" });
  };

  const handleEdit = (cat) => {
    setForm({ nama: cat.nama });
    setEditingId(cat.id);
  };

  return (
    <div className="p-6 bg-pink-50 min-h-screen">
      <h2 className="text-2xl font-bold text-pink-600 mb-4">Kelola Kategori</h2>

      <form onSubmit={handleSubmit} className="flex gap-2 mb-6">
        <input
            type="text"
            value={form.nama}
            onChange={(e) => setForm({ nama: e.target.value })}
            className="border border-pink-300 focus:ring-2 focus:ring-pink-400 p-2 rounded w-full"
            placeholder="Nama kategori"
            required
        />
        <button
            type="submit"
            className="bg-pink-600 hover:bg-pink-700 text-white px-4 rounded text-sm whitespace-nowrap"
            style={{ height: "42px" }}
        >
            {editingId ? "Simpan" : "Tambah"}
        </button>
        </form>

      <ul className="space-y-2">
        {categories.map((cat) => (
          <li
            key={cat.id}
            className="flex justify-between items-center bg-white border border-pink-200 p-3 rounded shadow-sm"
          >
            <span className="text-pink-800 font-medium">{cat.nama}</span>
            <div className="space-x-2">
              <button
                onClick={() => handleEdit(cat)}
                className="bg-pink-400 hover:bg-pink-300 text-white px-3 py-1 rounded text-sm transition"
              >
                Edit
              </button>
              <button
                onClick={() => deleteCategory(cat.id)}
                className="bg-pink-600 hover:bg-pink-500 text-white px-3 py-1 rounded text-sm transition"
              >
                Hapus
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
