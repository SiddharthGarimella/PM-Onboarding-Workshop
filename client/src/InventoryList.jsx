import React from "react";

const inventory = [
  { id: 1, name: "Arduino Kit", category: "Hardware", quantity: 5, status: "Available" },
  { id: 2, name: "Figma License", category: "Software", quantity: 20, status: "Available" },
  { id: 3, name: "Soldering Iron", category: "Hardware", quantity: 0, status: "Unavailable" },
  { id: 4, name: "Raspberry Pi 4", category: "Hardware", quantity: 8, status: "Available" },
  { id: 5, name: "Adobe Creative Cloud", category: "Software", quantity: 3, status: "Available" },
];

function StatusBadge({ status }) {
  const isAvailable = status === "Available";
  return (
    <span
      style={{
        padding: "4px 10px",
        borderRadius: "999px",
        fontSize: "13px",
        fontWeight: 500,
        color: isAvailable ? "#0F6E56" : "#993C1D",
        backgroundColor: isAvailable ? "#E1F5EE" : "#FAECE7",
      }}
    >
      {status}
    </span>
  );
}

export default function InventoryList() {
  return (
    <div style={{ maxWidth: 720, margin: "0 auto", padding: "24px", fontFamily: "sans-serif" }}>
      <h2 style={{ fontWeight: 500, marginBottom: "4px" }}>Open Project inventory</h2>
      <p style={{ color: "#5F5E5A", marginTop: 0, marginBottom: "20px" }}>
        {inventory.length} items on file
      </p>

      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ textAlign: "left", borderBottom: "1px solid #D3D1C7" }}>
            <th style={{ padding: "10px 8px" }}>Name</th>
            <th style={{ padding: "10px 8px" }}>Category</th>
            <th style={{ padding: "10px 8px" }}>Quantity</th>
            <th style={{ padding: "10px 8px" }}>Status</th>
          </tr>
        </thead>
        <tbody>
          {inventory.map((item) => (
            <tr key={item.id} style={{ borderBottom: "1px solid #F1EFE8" }}>
              <td style={{ padding: "10px 8px", fontWeight: 500 }}>{item.name}</td>
              <td style={{ padding: "10px 8px", color: "#5F5E5A" }}>{item.category}</td>
              <td style={{ padding: "10px 8px" }}>{item.quantity}</td>
              <td style={{ padding: "10px 8px" }}>
                <StatusBadge status={item.status} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
