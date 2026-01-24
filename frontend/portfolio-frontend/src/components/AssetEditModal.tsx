import { useState } from "react";
import type { Asset } from "../types/asset";

interface Props {
  asset: Asset;
  onClose: () => void;
  onUpdated: (updatedAsset: Asset) => void;
}

export default function AssetEditModal({ asset, onClose, onUpdated }: Props) {
  const [name, setName] = useState(asset.name);
  const [symbol, setSymbol] = useState(asset.symbol ?? "");
  const [currency, setCurrency] = useState(asset.currency ?? "");

  const handleSave = async () => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/assets/${asset.id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, symbol, currency }),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Failed to update asset");
      }

      const updated: Asset = await res.json();
      onUpdated(updated);
      onClose();
    } catch (err: unknown) {
      if (err instanceof Error) alert("Error updating asset: " + err.message);
      else alert("Unknown error");
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white p-4 rounded w-96">
        <h3 className="text-lg font-semibold mb-2">Edit Asset</h3>

        <input
          className="border p-2 w-full mb-2"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Name"
        />

        <input
          className="border p-2 w-full mb-2"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
          placeholder="Symbol"
        />

        <input
          className="border p-2 w-full mb-2"
          value={currency}
          onChange={(e) => setCurrency(e.target.value)}
          placeholder="Currency"
        />

        <div className="flex justify-end gap-2 mt-2">
          <button
            className="bg-gray-400 text-white px-4 py-2 rounded"
            onClick={onClose}
          >
            Cancel
          </button>
          <button
            className="bg-blue-600 text-white px-4 py-2 rounded"
            onClick={handleSave}
          >
            Save
          </button>
        </div>
      </div>
    </div>
  );
}
