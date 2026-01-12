import { useState } from "react";
import type { Asset } from "../types/asset";

interface AssetFormProps {
  onAssetAdded: () => void;
}

export default function AssetForm({ onAssetAdded }: AssetFormProps) {
  const [name, setName] = useState("");
  const [symbol, setSymbol] = useState("");
  const [isin, setIsin] = useState("");
  const [type, setType] = useState("");
  const [provider, setProvider] = useState("");
  const [currency, setCurrency] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const payload: Partial<Asset> = {
      name,
      symbol: symbol || "MANUAL",
      isin: isin || "",
      type: type || "manual",
      provider: provider || "manual",
      currency: currency || "USD",
    };

    try {
      const res = await fetch("http://127.0.0.1:8000/assets/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) throw new Error("Failed to add asset");

      onAssetAdded();

      // Reset form
      setName("");
      setSymbol("");
      setIsin("");
      setType("");
      setProvider("");
      setCurrency("");
    } catch (error) {
      console.error(error);
      alert("Failed to add asset. Check backend!");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-6 space-y-2">
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Name"
        required
        className="border p-2 w-full"
      />
      <input
        value={symbol}
        onChange={(e) => setSymbol(e.target.value)}
        placeholder="Symbol (optional)"
        className="border p-2 w-full"
      />
      <input
        value={isin}
        onChange={(e) => setIsin(e.target.value)}
        placeholder="ISIN (optional)"
        className="border p-2 w-full"
      />
      <input
        value={type}
        onChange={(e) => setType(e.target.value)}
        placeholder="Type (optional)"
        className="border p-2 w-full"
      />
      <input
        value={provider}
        onChange={(e) => setProvider(e.target.value)}
        placeholder="Provider (optional)"
        className="border p-2 w-full"
      />
      <input
        value={currency}
        onChange={(e) => setCurrency(e.target.value)}
        placeholder="Currency (optional)"
        className="border p-2 w-full"
      />
      <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
        Add Asset
      </button>
    </form>
  );
}
