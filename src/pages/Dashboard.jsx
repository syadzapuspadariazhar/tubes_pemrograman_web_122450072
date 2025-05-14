import { useEffect, useState } from "react";
import { useAppContext } from "../contexts/AppContext";
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from "recharts";

export default function Dashboard() {
  const { transactions } = useAppContext();
  const [summary, setSummary] = useState({
    pemasukan: 0,
    pengeluaran: 0,
    saldo: 0,
  });

  useEffect(() => {
    const pemasukan = transactions
      .filter((t) => t.jenis === "pemasukan")
      .reduce((sum, t) => sum + Number(t.jumlah), 0);

    const pengeluaran = transactions
      .filter((t) => t.jenis === "pengeluaran")
      .reduce((sum, t) => sum + Number(t.jumlah), 0);

    const saldo = pemasukan - pengeluaran;

    setSummary({ pemasukan, pengeluaran, saldo });
  }, [transactions]);

  const chartData = [
    { name: "Pemasukan", value: summary.pemasukan },
    { name: "Pengeluaran", value: summary.pengeluaran },
  ];

  const COLORS = ["#34D399", "#F87171"]; // green, red

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6 text-pink-700">Dashboard Keuangan</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-white shadow-md p-4 rounded-xl border border-pink-100">
          <h2 className="text-lg font-medium text-pink-700">Pemasukan</h2>
          <p className="text-green-600 text-2xl font-bold mt-1">
            Rp {summary.pemasukan.toLocaleString()}
          </p>
        </div>
        <div className="bg-white shadow-md p-4 rounded-xl border border-pink-100">
          <h2 className="text-lg font-medium text-pink-700">Pengeluaran</h2>
          <p className="text-red-600 text-2xl font-bold mt-1">
            Rp {summary.pengeluaran.toLocaleString()}
          </p>
        </div>
        <div className="bg-white shadow-md p-4 rounded-xl border border-pink-100">
          <h2 className="text-lg font-medium text-pink-700">Saldo</h2>
          <p className="text-blue-600 text-2xl font-bold mt-1">
            Rp {summary.saldo.toLocaleString()}
          </p>
        </div>
      </div>

      <div className="bg-white shadow-md p-4 rounded-xl border border-pink-100">
        <h2 className="text-lg font-medium text-pink-700 mb-4">Distribusi Keuangan</h2>
        <div className="w-full h-[300px]">
          <ResponsiveContainer>
            <PieChart>
              <Pie
                data={chartData}
                cx="50%"
                cy="50%"
                outerRadius={100}
                dataKey="value"
                label={({ name, percent }) =>
                  `${name}: ${(percent * 100).toFixed(0)}%`
                }
              >
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index]} />
                ))}
              </Pie>
              <Tooltip formatter={(value) => `Rp ${value.toLocaleString()}`} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
