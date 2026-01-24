import { useState, useEffect, useCallback } from "react";
import AssetList from "./components/AssetList";
import AssetForm from "./components/AssetForm";
import LotForm from "./components/LotForm";
import FetchLotsPerAsset from "./components/Fetch_lots_per_asset";
import type { Asset } from "./types/asset";
import AssetPortfolio from "./components/AssetPortfolio";

function App() {
  const [assets, setAssets] = useState<Asset[]>([]);
  const [selectedAssetId, setSelectedAssetId] = useState<number | null>(null);
  const [lotsRefreshFlag, setLotsRefreshFlag] = useState(0);

  // -----------------------------
  // Fetch all assets
  // -----------------------------
  const fetchAssets = useCallback(async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/assets/");
      if (!res.ok) throw new Error("Failed to fetch assets");

      const data: Asset[] = await res.json();
      setAssets(data);
    } catch (err: unknown) {
      if (err instanceof Error) console.error(err.message);
      else console.error(err);
    }
  }, []);

  useEffect(() => {
    fetchAssets();
  }, [fetchAssets]);

  // -----------------------------
  // Handle selecting an asset
  // -----------------------------
  const handleSelectAsset = (id: number) => {
    setSelectedAssetId(id);
  };

  // -----------------------------
  // Handle deleting an asset
  // -----------------------------
  const handleDeleteAsset = async (assetId: number) => {
    if (!confirm("Are you sure you want to delete this asset?")) return;

    try {
      const res = await fetch(`http://127.0.0.1:8000/assets/${assetId}`, {
        method: "DELETE",
      });
      if (!res.ok) throw new Error("Failed to delete asset");

      // Refresh asset list
      await fetchAssets();

      // If deleted asset was selected, clear selection
      if (selectedAssetId === assetId) setSelectedAssetId(null);
    } catch (err: unknown) {
      if (err instanceof Error) alert("Error deleting asset: " + err.message);
      else alert("Unknown error deleting asset");
    }
  };

  // -----------------------------
  // Refresh lots after creation or deletion
  // -----------------------------
 const refreshLots = () => {
  setLotsRefreshFlag((v) => v + 1);
};

  return (
    <div className="max-w-5xl mx-auto p-4">
      <h1 className="text-4xl font-bold mb-6 text-center text-blue-500">
        Portfolio Manager
      </h1>

      {/* ---------------- Asset Form ---------------- */}
      <AssetForm onAssetAdded={fetchAssets} />

      {/* ---------------- Asset List ---------------- */}
     <AssetList
      assets={assets}
      onSelectAsset={handleSelectAsset}
      onAssetsUpdated={fetchAssets}
    />

      {/* ---------------- Lots Section ---------------- */}
      {selectedAssetId && (
        <div className="mt-6">
          <LotForm assetId={selectedAssetId} onLotAdded={refreshLots} />

          <FetchLotsPerAsset
            assetId={selectedAssetId}
            refreshFlag={lotsRefreshFlag}
            onLotDeleted={refreshLots}
          />
          <AssetPortfolio
            assetId={selectedAssetId}
            refreshFlag={lotsRefreshFlag}
            />
        </div>
      )}
    </div>
  );
}

export default App;
