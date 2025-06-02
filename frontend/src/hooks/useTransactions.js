import { createContext, useContext, useEffect, useState } from "react";

const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const [transactions, setTransactions] = useState([]);
  const [categories, setCategories] = useState([]);

  useEffect(() => {
  }, []);

  const fetchTransactions = async () => {
  };

  const fetchCategories = async () => {
  };

  const addCategory = async (newCategory) => {
    const idBaru = categories.length + 1;
    const kategoriBaru = { ...newCategory, id: idBaru };
    setCategories([...categories, kategoriBaru]);
    console.log("Kategori ditambahkan:", kategoriBaru);
  };

  const deleteCategory = async (id) => {
    setCategories(categories.filter((cat) => cat.id !== id));
  };

  const updateCategory = async (id, updated) => {
    setCategories(categories.map((cat) => (cat.id === id ? { ...cat, ...updated } : cat)));
  };

  const addTransaction = async (data) => {
    const idBaru = transactions.length + 1;
    const transaksiBaru = { ...data, id: idBaru };
    setTransactions([...transactions, transaksiBaru]);
    console.log("Transaksi ditambahkan:", transaksiBaru);
  };

  const deleteTransaction = async (id) => {
    setTransactions(transactions.filter((t) => t.id !== id));
  };

  const updateTransaction = async (id, data) => {
    setTransactions(transactions.map((t) => (t.id === id ? { ...t, ...data } : t)));
  };

  return (
    <AppContext.Provider
      value={{
        transactions,
        categories,
        fetchTransactions,
        fetchCategories,
        addTransaction,
        updateTransaction,
        deleteTransaction,
        addCategory,
        updateCategory,
        deleteCategory,
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

export const useAppContext = () => useContext(AppContext);
