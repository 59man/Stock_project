import { useState, useEffect } from "react";
import AssetList from "./components/AssetList";
import AssetForm from "./components/AssetForm";
import LotForm from "./components/LotForm";

// Match backend schema
export interface Asset {
  id: number;
  name: string;
  symbol: string;
  isin: string;
  type: string;
  provider: string;
  currency: string;
}

function App() {
  const [assets, setAssets] = useState<Asset[]>([]);
  const [selectedAssetId, setSelectedAssetId] = useState<number | null>(null);

  // Fetch assets from backend
  const fetchAssets = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/assets/");
      const data = await res.json();
      setAssets(data);
    } catch (error) {
      console.error("Failed to fetch assets:", error);
    }
  };

  useEffect(() => {
  let isMounted = true; // ✅ track if component is mounted

  const fetchAssets = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/assets/");
      if (!res.ok) throw new Error("Failed to fetch assets");
      const data: Asset[] = await res.json();

      if (isMounted) { // ✅ only set state if still mounted
        setAssets(data);
      }
    } catch (err) {
      console.error(err);
    }
  };

  fetchAssets();

  return () => {
    isMounted = false; // cleanup
  };
}, []);


  const handleSelectAsset = (id: number) => {
    setSelectedAssetId(id);
  };

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-4xl font-bold mb-6 text-center text-blue-400">
        Portfolio Manager
      </h1>

      <AssetForm onAssetAdded={fetchAssets} />

      <AssetList assets={assets} onSelectAsset={handleSelectAsset} />

      {selectedAssetId && <LotForm assetId={selectedAssetId} />}
    </div>
  );
}

export default App;
