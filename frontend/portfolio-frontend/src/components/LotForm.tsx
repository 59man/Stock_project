import { useState } from "react";

interface LotFormProps {
  assetId: number;
}

export default function LotForm({ assetId }: LotFormProps) {
  const [quantity, setQuantity] = useState<number>(0);
  const [price, setPrice] = useState<number>(0);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const res = await fetch(`http://127.0.0.1:8000/lots/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          asset_id: assetId,
          quantity,
          price,
        }),
      });

      if (!res.ok) throw new Error("Failed to add lot");

      setQuantity(0);
      setPrice(0);
      alert("Lot added!");
    } catch (error) {
      console.error(error);
      alert("Failed to add lot. Check backend!");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-2">
      <h2 className="text-2xl font-bold mb-2">Add Lot</h2>
      <input
        type="number"
        value={quantity}
        onChange={(e) => setQuantity(parseFloat(e.target.value))}
        placeholder="Quantity"
        className="border p-2 w-full"
      />
      <input
        type="number"
        value={price}
        onChange={(e) => setPrice(parseFloat(e.target.value))}
        placeholder="Price"
        className="border p-2 w-full"
      />
      <button type="submit" className="bg-green-500 text-white px-4 py-2 rounded">
        Add Lot
      </button>
    </form>
  );
}
