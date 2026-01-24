import { useState } from "react";
import type { Asset } from "../types/asset";

interface Props {
  assets: Asset[];
  onSelectAsset: (id: number) => void;
  onAssetsUpdated: () => void;
}

export default function AssetList({
  assets,
  onSelectAsset,
  onAssetsUpdated,
}: Props) {
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editName, setEditName] = useState("");
  const [editSymbol, setEditSymbol] = useState("");
  const [editCurrency, setEditCurrency] = useState("");

  const startEdit = (asset: Asset) => {
    setEditingId(asset.id);
    setEditName(asset.name);
    setEditSymbol(asset.symbol ?? "");
    setEditCurrency(asset.currency ?? "");
  };

  const cancelEdit = () => {
    setEditingId(null);
  };

  const saveEdit = async (id: number) => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/assets/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: editName,
          symbol: editSymbol || null,
          currency: editCurrency || null,
        }),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Failed to update asset");
      }

      setEditingId(null);
      onAssetsUpdated();
    } catch (err: unknown) {
      if (err instanceof Error) {
        alert(err.message);
      }
    }
  };

  const deleteAsset = async (id: number) => {
    if (!confirm("Delete this asset?")) return;

    try {
      const res = await fetch(`http://127.0.0.1:8000/assets/${id}`, {
        method: "DELETE",
      });

      if (!res.ok) throw new Error("Delete failed");
      onAssetsUpdated();
    } catch {
      alert("Failed to delete asset");
    }
  };

  return (
    <div className="mt-6">
      <h3 className="text-lg font-semibold mb-2">Assets</h3>

      <ul>
        {assets.map((asset) => (
          <li
            key={asset.id}
            className="border-b py-2 flex items-center justify-between"
          >
            {editingId === asset.id ? (
              <div className="flex gap-2">
                <input
                  className="border p-1"
                  value={editName}
                  onChange={(e) => setEditName(e.target.value)}
                />
                <input
                  className="border p-1"
                  value={editSymbol}
                  onChange={(e) => setEditSymbol(e.target.value)}
                />
                <input
                  className="border p-1"
                  value={editCurrency}
                  onChange={(e) => setEditCurrency(e.target.value)}
                />

                <button
                  className="bg-green-600 text-white px-2 rounded"
                  onClick={() => saveEdit(asset.id)}
                >
                  Save
                </button>

                <button
                  className="bg-gray-400 text-white px-2 rounded"
                  onClick={cancelEdit}
                >
                  Cancel
                </button>
              </div>
            ) : (
              <>
                <span
                  className="cursor-pointer text-blue-600"
                  onClick={() => onSelectAsset(asset.id)}
                >
                  {asset.name} ({asset.symbol}) [{asset.currency}]
                </span>

                <div className="flex gap-2">
                  <button
                    className="bg-yellow-500 text-white px-2 rounded"
                    onClick={() => startEdit(asset)}
                  >
                    Edit
                  </button>

                  <button
                    className="bg-red-600 text-white px-2 rounded"
                    onClick={() => deleteAsset(asset.id)}
                  >
                    Delete
                  </button>
                </div>
              </>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
