import { useState } from "react";
import type { LotCreate } from "../types/lot";


// LotForm.tsx
interface Props {
  assetId: number;
  onLotAdded?: () => void; // ✅ optional callback for after adding a lot
}

export default function LotForm({ assetId, onLotAdded }: Props) {
  const [quantity, setQuantity] = useState("");
  const [price, setPrice] = useState("");
  const [currency, setCurrency] = useState("USD");
  const [boughtAt, setBoughtAt] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const payload: LotCreate = {
      asset_id: assetId,
      quantity: Number(quantity),
      price: Number(price),
      currency,
      bought_at: boughtAt ? new Date(boughtAt).toISOString() : null,
    };

    try {
      await fetch("http://127.0.0.1:8000/lots/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      setQuantity("");
      setPrice("");
      setBoughtAt(null);

      if (onLotAdded) onLotAdded(); // ✅ trigger refresh
    } catch (err: unknown) {
      if (err instanceof Error) alert("Failed to add lot: " + err.message);
      else alert("Failed to add lot: unknown error");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mt-6 p-4 border rounded">
      <h3 className="text-lg font-semibold mb-2">Add Lot</h3>

      <input
        className="border p-2 mr-2"
        type="number"
        step="any"
        placeholder="Quantity"
        value={quantity}
        onChange={(e) => setQuantity(e.target.value)}
        required
      />
      <input
        className="border p-2 mr-2"
        type="number"
        step="any"
        placeholder="Price"
        value={price}
        onChange={(e) => setPrice(e.target.value)}
        required
      />
      <input
        className="border p-2 mr-2"
        placeholder="Currency"
        value={currency}
        onChange={(e) => setCurrency(e.target.value)}
      />
      <input
        className="border p-2 mr-2"
        type="date"
        value={boughtAt ?? ""}
        onChange={(e) => setBoughtAt(e.target.value || null)}
      />

      <button className="bg-green-600 text-white px-4 py-2 rounded">
        Add Lot
      </button>
    </form>
  );
}
