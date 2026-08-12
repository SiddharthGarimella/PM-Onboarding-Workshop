const express = require("express");
const cors = require("cors");

const app = express();
const PORT = 3001;

// Middleware
app.use(cors());        // allows the React app (different port) to call this server
app.use(express.json()); // parses incoming JSON request bodies into req.body

// "Database" — in-memory array, matches the Inventory Data Contract exactly.
// Resets every time the server restarts, per the module spec.
let inventory = [
  { id: 1, name: "Arduino Kit", category: "Hardware", quantity: 5, status: "Available" },
  { id: 2, name: "Figma License", category: "Software", quantity: 20, status: "Available" },
];

// Tracks the next id to hand out, so new items don't collide with existing ones.
let nextId = 3;

// GET /inventory — return all inventory items
app.get("/inventory", (req, res) => {
  res.json(inventory);
});

// POST /inventory — add a new inventory item
app.post("/inventory", (req, res) => {
  const { name, category, quantity, status } = req.body;

  const newItem = {
    id: nextId++,
    name,
    category,
    quantity,
    status,
  };

  inventory.push(newItem);

  res.json({ message: "item added successfully" });
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
