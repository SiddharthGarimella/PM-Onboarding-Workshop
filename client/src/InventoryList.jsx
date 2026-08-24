import React, { useState, useEffect } from "react";

const API_URL = "http://localhost:3001/inventory";

export default function InventoryList() {
  const [inventory, setInventory] = useState([]);
  const [form, setForm] = useState({ name: "", category: "", quantity: "", status: "Available" });

  function fetchInventory() {
    fetch(API_URL)
      .then((res) => res.json())
      .then((data) => setInventory(data));
  }

  useEffect(() => {
    fetchInventory();
  }, []);

  function handleSubmit(e) {
    e.preventDefault();
    fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...form, quantity: Number(form.quantity) }),
    }).then(() => {
      fetchInventory();
      setForm({ name: "", category: "", quantity: "", status: "Available" });
    });
  }

  return (
    <div>
      <table>
        <tbody>
          {inventory.map((item) => (
            <tr key={item.id}>
              <td>{item.name}</td>
              <td>{item.category}</td>
              <td>{item.quantity}</td>
              <td>{item.status}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <form onSubmit={handleSubmit}>
        <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="Name" />
        <input value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })} placeholder="Category" />
        <input value={form.quantity} onChange={(e) => setForm({ ...form, quantity: e.target.value })} placeholder="Quantity" />
        <select value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}>
          <option value="Available">Available</option>
          <option value="Unavailable">Unavailable</option>
        </select>
        <button type="submit">Add item</button>
      </form>
    </div>
  );
}

