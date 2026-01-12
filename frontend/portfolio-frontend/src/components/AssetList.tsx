import type { Asset } from "../App";

interface AssetListProps {
  assets: Asset[];
  onSelectAsset: (id: number) => void;
}

export default function AssetList({ assets, onSelectAsset }: AssetListProps) {
  if (!assets.length) return <p>No assets yet.</p>;

  return (
    <ul className="space-y-2 mb-6">
      {assets.map((asset) => (
        <li
          key={asset.id}
          className="border p-2 cursor-pointer hover:bg-gray-100"
          onClick={() => onSelectAsset(asset.id)}
        >
          {asset.name} ({asset.symbol}) — {asset.type}
        </li>
      ))}
    </ul>
  );
}
