import { useEffect, useState } from "react";
import { useAppContext } from "../contexts/AppContext";
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid } from "recharts";

export default function Dashboard() {
  const { transactions } = useAppContext();
  const [summary, setSummary] = useState({
    pemasukan: 0,
    pengeluaran: 0,
    saldo: 0,
  });
  const [dailyExpenses, setDailyExpenses] = useState([]);

  useEffect(() => {
    const pemasukan = transactions
      .filter((t) => t.jenis === "pemasukan")
      .reduce((sum, t) => sum + Number(t.jumlah), 0);

    const pengeluaran = transactions
      .filter((t) => t.jenis === "pengeluaran")
      .reduce((sum, t) => sum + Number(t.jumlah), 0);

    const saldo = pemasukan - pengeluaran;

    setSummary({ pemasukan, pengeluaran, saldo });

    // Calculate daily expenses for the chart
    const expensesByDate = {};
    transactions
      .filter((t) => t.jenis === "pengeluaran")
      .forEach((transaction) => {
        const date = new Date(transaction.tanggal).toLocaleDateString('id-ID', {
          day: '2-digit',
          month: '2-digit'
        });
        expensesByDate[date] = (expensesByDate[date] || 0) + Number(transaction.jumlah);
      });

    // Convert to array and sort by date
    const dailyData = Object.entries(expensesByDate)
      .map(([date, amount]) => ({ date, amount }))
      .sort((a, b) => {
        const dateA = new Date(a.date.split('/').reverse().join('-'));
        const dateB = new Date(b.date.split('/').reverse().join('-'));
        return dateA - dateB;
      })
      .slice(-7); // Show last 7 days

    setDailyExpenses(dailyData);
  }, [transactions]);

  const chartData = [
    { name: "Pemasukan", value: summary.pemasukan },
    { name: "Pengeluaran", value: summary.pengeluaran },
  ];

  const COLORS = ["#34D399", "#F87171"]; // green, red
  return (
    <div className="p-6 bg-gradient-to-br from-pink-50 via-purple-50 to-indigo-50 min-h-screen">
      {/* Header Section */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-pink-600 to-purple-600 mb-2 flex items-center">
          <svg className="w-10 h-10 mr-3 text-pink-600" fill="currentColor" viewBox="0 0 20 20">
            <path d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" />
          </svg>
          Dashboard Keuangan
        </h1>
        <p className="text-gray-600 text-lg">Ringkasan finansial dan analisis pengeluaran Anda</p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {/* Pemasukan Card */}
        <div className="bg-gradient-to-br from-green-400 to-emerald-500 text-white p-6 rounded-xl shadow-lg border border-green-200 transform hover:scale-105 transition-all duration-200">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold mb-1 flex items-center">
                <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.293l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13a1 1 0 102 0V9.414l1.293 1.293a1 1 0 001.414-1.414z" clipRule="evenodd" />
                </svg>
                Pemasukan
              </h2>
              <p className="text-3xl font-bold">
                Rp {summary.pemasukan.toLocaleString()}
              </p>
              <p className="text-green-100 text-sm mt-1">💰 Total pendapatan</p>
            </div>
            <div className="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center">
              <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
              </svg>
            </div>
          </div>
        </div>

        {/* Pengeluaran Card */}
        <div className="bg-gradient-to-br from-red-400 to-rose-500 text-white p-6 rounded-xl shadow-lg border border-red-200 transform hover:scale-105 transition-all duration-200">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold mb-1 flex items-center">
                <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v3.586L7.707 9.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L11 10.586V7z" clipRule="evenodd" />
                </svg>
                Pengeluaran
              </h2>
              <p className="text-3xl font-bold">
                Rp {summary.pengeluaran.toLocaleString()}
              </p>
              <p className="text-red-100 text-sm mt-1">💸 Total pengeluaran</p>
            </div>
            <div className="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center">
              <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                <path d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z" />
              </svg>
            </div>
          </div>
        </div>

        {/* Saldo Card */}
        <div className={`bg-gradient-to-br ${summary.saldo >= 0 ? 'from-blue-400 to-indigo-500' : 'from-orange-400 to-red-500'} text-white p-6 rounded-xl shadow-lg border ${summary.saldo >= 0 ? 'border-blue-200' : 'border-orange-200'} transform hover:scale-105 transition-all duration-200`}>
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold mb-1 flex items-center">
                <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Saldo
              </h2>
              <p className="text-3xl font-bold">
                Rp {summary.saldo.toLocaleString()}
              </p>
              <p className={`${summary.saldo >= 0 ? 'text-blue-100' : 'text-orange-100'} text-sm mt-1`}>
                {summary.saldo >= 0 ? '📈 Keuangan sehat' : '⚠️ Perlu perhatian'}
              </p>
            </div>
            <div className="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center">
              <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 6a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM4 14a1 1 0 100 2h12a1 1 0 100-2H4z" clipRule="evenodd" />
              </svg>
            </div>
          </div>
        </div>
      </div>      {/* Chart Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Pie Chart */}
        <div className="bg-white rounded-xl shadow-lg border border-pink-100 overflow-hidden">
          <div className="bg-gradient-to-r from-pink-500 to-purple-600 px-6 py-4">
            <h2 className="text-xl font-semibold text-white flex items-center">
              <svg className="w-6 h-6 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path d="M2 10a8 8 0 018-8v8h8a8 8 0 11-16 0z" />
                <path d="M12 2.252A8.014 8.014 0 0117.748 8H12V2.252z" />
              </svg>
              Distribusi Keuangan
            </h2>
            <p className="text-pink-100 text-sm">Perbandingan pemasukan dan pengeluaran</p>
          </div>
          
          <div className="p-6">
            {summary.pemasukan === 0 && summary.pengeluaran === 0 ? (
              <div className="text-center py-12 text-gray-500">
                <svg className="w-16 h-16 mx-auto mb-4 text-gray-300" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M2 10a8 8 0 018-8v8h8a8 8 0 11-16 0z" />
                  <path d="M12 2.252A8.014 8.014 0 0117.748 8H12V2.252z" />
                </svg>
                <p className="text-xl font-semibold text-gray-400 mb-2">Belum ada data transaksi</p>
                <p className="text-gray-400">Mulai tambahkan transaksi untuk melihat distribusi</p>
              </div>
            ) : (
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
                    <Tooltip 
                      formatter={(value) => [`Rp ${value.toLocaleString()}`, 'Jumlah']}
                      labelStyle={{ color: '#374151', fontWeight: 'bold' }}
                      contentStyle={{ 
                        backgroundColor: '#fff', 
                        border: '1px solid #e5e7eb',
                        borderRadius: '8px',
                        boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)'
                      }}
                    />
                    <Legend 
                      wrapperStyle={{ paddingTop: '20px' }}
                      iconType="circle"
                    />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            )}
          </div>
        </div>

        {/* Daily Expenses Chart */}
        <div className="bg-white rounded-xl shadow-lg border border-purple-100 overflow-hidden">
          <div className="bg-gradient-to-r from-purple-500 to-indigo-600 px-6 py-4">
            <h2 className="text-xl font-semibold text-white flex items-center">
              <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              Pengeluaran Harian
            </h2>
            <p className="text-purple-100 text-sm">Tren pengeluaran 7 hari terakhir</p>
          </div>
          
          <div className="p-6">
            {dailyExpenses.length === 0 ? (
              <div className="text-center py-12 text-gray-500">
                <svg className="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                <p className="text-xl font-semibold text-gray-400 mb-2">Belum ada pengeluaran</p>
                <p className="text-gray-400">Tambahkan transaksi pengeluaran untuk melihat tren</p>
              </div>
            ) : (
              <div className="w-full h-[300px]">
                <ResponsiveContainer>
                  <LineChart data={dailyExpenses}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                    <XAxis 
                      dataKey="date" 
                      tick={{ fontSize: 12, fill: '#64748b' }}
                      tickLine={{ stroke: '#cbd5e1' }}
                    />
                    <YAxis 
                      tick={{ fontSize: 12, fill: '#64748b' }}
                      tickLine={{ stroke: '#cbd5e1' }}
                      tickFormatter={(value) => `${(value / 1000).toFixed(0)}k`}
                    />
                    <Tooltip 
                      formatter={(value) => [`Rp ${value.toLocaleString()}`, 'Pengeluaran']}
                      labelFormatter={(label) => `Tanggal: ${label}`}
                      contentStyle={{
                        backgroundColor: '#fff',
                        border: '1px solid #e5e7eb',
                        borderRadius: '8px',
                        boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)'
                      }}
                    />
                    <Line 
                      type="monotone" 
                      dataKey="amount" 
                      stroke="#8b5cf6" 
                      strokeWidth={3}
                      dot={{ fill: '#8b5cf6', strokeWidth: 2, r: 6 }}
                      activeDot={{ r: 8, fill: '#7c3aed' }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
