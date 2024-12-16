"use client";

import { useState, useEffect } from "react";
import axios from "axios";
import ProductView from "./ProductView";

interface Product {
  id: number;
  brand: string;
  model: string;
  main_cat: string;
  sub_cat: string;
}

export default function ProductTable() {
  const [products, setProducts] = useState<Product[]>([]);
  const [error, setError] = useState("");
  const [selectedProductId, setSelectedProductId] = useState<number | null>(null);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/products")
      .then((response) => setProducts(response.data))
      .catch(() => setError("Failed to fetch products"));
  }, []);

  if (error) {
    return <p className="text-red-500">{error}</p>;
  }

  if (selectedProductId) {
    return <ProductView id={selectedProductId} onClose={() => setSelectedProductId(null)} />;
  }

  return (
    <div className="p-6 bg-gray-900 min-h-screen text-white">
      <h2 className="text-3xl font-bold mb-6">Product List</h2>
      <table className="w-full mt-4 border-collapse border border-gray-700">
        <thead>
          <tr className="bg-gray-800 text-white">
            <th className="border border-gray-700 px-4 py-2 text-left">ID</th>
            <th className="border border-gray-700 px-4 py-2 text-left">Brand</th>
            <th className="border border-gray-700 px-4 py-2 text-left">Model</th>
            <th className="border border-gray-700 px-4 py-2 text-left">Main Category</th>
            <th className="border border-gray-700 px-4 py-2 text-left">Sub Category</th>
            <th className="border border-gray-700 px-4 py-2 text-left">Actions</th>
          </tr>
        </thead>
        <tbody>
          {products.map((product) => (
            <tr key={product.id} className="hover:bg-gray-800">
              <td className="border border-gray-700 px-4 py-2">{product.id}</td>
              <td className="border border-gray-700 px-4 py-2">{product.brand}</td>
              <td className="border border-gray-700 px-4 py-2">{product.model}</td>
              <td className="border border-gray-700 px-4 py-2">{product.main_cat}</td>
              <td className="border border-gray-700 px-4 py-2">{product.sub_cat}</td>
              <td className="border border-gray-700 px-4 py-2">
                <button
                  onClick={() => setSelectedProductId(product.id)}
                  className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  View
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
