import Navbar from "../components/Navbar";
import ProductTable from "../components/ProductTable";

export default function Dashboard() {
  return (
    <div>
      <Navbar />
      <div className="p-4">
        <h1 className="text-2xl font-bold mb-4">Products</h1>
        <ProductTable />
      </div>
    </div>
  );
}
