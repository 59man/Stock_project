import { useEffect, useState, useCallback } from "react";
import type { LotResponse } from "../types/lot";

interface Props {
  assetId: number;
  refreshFlag?: number;
  onLotDeleted?: () => void;
}

export default function FetchLotsPerAsset({ assetId, refreshFlag, onLotDeleted }: Props) {
  const [lots, setLots] = useState<LotResponse[]>([]);

  // ✅ Wrap fetchLots in useCallback to satisfy dependency warning
  const fetchLots = useCallback(async () => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/lots/asset/${assetId}`);
      if (!res.ok) throw new Error("Failed to fetch lots");

      const data: LotResponse[] = await res.json();
      setLots(data);
    } catch (err: unknown) {
      if (err instanceof Error) console.error("Error fetching lots:", err.message);
      else console.error(err);
    }
  }, [assetId]); // ✅ dependency on assetId

  const handleDelete = async (lotId: number) => {
    if (!confirm("Are you sure you want to delete this lot?")) return;

    try {
      const res = await fetch(`http://127.0.0.1:8000/lots/${lotId}`, { method: "DELETE" });
      if (!res.ok) throw new Error("Failed to delete lot");

      setLots((prev) => prev.filter((l) => l.id !== lotId));

      if (onLotDeleted) onLotDeleted();
    } catch (err: unknown) {
      if (err instanceof Error) alert("Error deleting lot: " + err.message);
      else alert("Unknown error deleting lot");
    }
  };

  useEffect(() => {
    fetchLots();
  }, [fetchLots, refreshFlag]); // ✅ now fetchLots is stable

  if (!lots.length) return <p className="mt-2 text-gray-500">No lots for this asset.</p>;

  return (
    <table className="mt-4 w-full border-collapse border border-gray-300">
      <thead>
        <tr className="bg-gray-100">
          <th className="border px-2 py-1">ID</th>
          <th className="border px-2 py-1">Quantity</th>
          <th className="border px-2 py-1">Price</th>
          <th className="border px-2 py-1">Currency</th>
          <th className="border px-2 py-1">Bought At</th>
          <th className="border px-2 py-1">Actions</th>
        </tr>
      </thead>
      <tbody>
        {lots.map((lot) => (
          <tr key={lot.id} className="hover:bg-gray-50">
            <td className="border px-2 py-1">{lot.id}</td>
            <td className="border px-2 py-1">{lot.quantity}</td>
            <td className="border px-2 py-1">{lot.price}</td>
            <td className="border px-2 py-1">{lot.currency ?? "-"}</td>
            <td className="border px-2 py-1">
              {lot.bought_at ? new Date(lot.bought_at).toLocaleDateString() : "-"}
            </td>
            <td className="border px-2 py-1">
              <button
                className="bg-red-500 text-white px-2 py-1 rounded"
                onClick={() => handleDelete(lot.id)}
              >
                Delete
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
