import { useEffect, useState } from "react";

interface AssetPortfolioProps {
  assetId?: number;          // optional, if you want per-asset filtering later
  refreshFlag?: number;     // toggle to trigger refresh
}

interface PortfolioAsset {
  asset_id: number;
  name: string;
  symbol: string;
  quantity: number;
  invested: number;
  average_price: number;
  current_price: number;
  current_value: number;
  profit_loss: number;
  profit_loss_pct: number | null;
  currency: string;
}

interface PortfolioData {
  total_invested: number;
  total_value: number;
  total_profit_loss: number;
  total_profit_loss_pct: number | null;
  assets: PortfolioAsset[];
}

export default function AssetPortfolio({
  assetId,
  refreshFlag,
}: AssetPortfolioProps) {
  const [portfolio, setPortfolio] = useState<PortfolioData | null>(null);

  const fetchPortfolio = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/portfolio/");
      if (!res.ok) throw new Error("Failed to fetch portfolio");
      const data: PortfolioData = await res.json();
      setPortfolio(data);
    } catch (err) {
      console.error("Error fetching portfolio:", err);
    }
  };

  useEffect(() => {
    fetchPortfolio();
  }, [refreshFlag]);

  if (!portfolio) return <div>Loading portfolio...</div>;

  // Filter by assetId if provided
  const assets = assetId
    ? portfolio.assets.filter((a) => a.asset_id === assetId)
    : portfolio.assets;

  return (
    <div className="mt-6 p-4 border rounded">
      <h3 className="text-lg font-semibold mb-2">Portfolio</h3>

      <table className="w-full border-collapse">
        <thead>
          <tr className="border-b">
            <th className="text-left px-2 py-1">Asset</th>
            <th className="px-2 py-1">Qty</th>
            <th className="px-2 py-1">Avg Price</th>
            <th className="px-2 py-1">Current</th>
            <th className="px-2 py-1">Value</th>
            <th className="px-2 py-1">P/L</th>
            <th className="px-2 py-1">P/L %</th>
          </tr>
        </thead>
        <tbody>
          {assets.map((a) => (
            <tr key={a.asset_id} className="border-b">
              <td className="px-2 py-1">{a.name} ({a.symbol})</td>
              <td className="px-2 py-1">{a.quantity}</td>
              <td className="px-2 py-1">{a.average_price.toFixed(2)}</td>
              <td className="px-2 py-1">{a.current_price.toFixed(2)}</td>
              <td className="px-2 py-1">{a.current_value.toFixed(2)}</td>
              <td className={`px-2 py-1 ${a.profit_loss >= 0 ? "text-green-600" : "text-red-600"}`}>
                {a.profit_loss.toFixed(2)}
              </td>
              <td className={`px-2 py-1 ${a.profit_loss_pct && a.profit_loss_pct >= 0 ? "text-green-600" : "text-red-600"}`}>
                {a.profit_loss_pct ? a.profit_loss_pct.toFixed(2) + "%" : "-"}
              </td>
            </tr>
          ))}
        </tbody>
        <tfoot>
          <tr className="border-t font-semibold">
            <td className="px-2 py-1">Total</td>
            <td></td>
            <td></td>
            <td></td>
            <td className="px-2 py-1">{portfolio.total_value.toFixed(2)}</td>
            <td className="px-2 py-1">{portfolio.total_profit_loss.toFixed(2)}</td>
            <td className="px-2 py-1">{portfolio.total_profit_loss_pct?.toFixed(2)}%</td>
          </tr>
        </tfoot>
      </table>
    </div>
  );
}
