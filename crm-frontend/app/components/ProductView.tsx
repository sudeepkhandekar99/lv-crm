"use client";

import { useEffect, useState } from "react";
import axios from "axios";

interface ProductDetails {
  id: number;
  code: string;
  main_cat: string;
  sub_cat: string;
  brand: string;
  model: string;
  housing_size: string | null;
  function: string | null;
  range: string | null;
  output: string | null;
  voltage: string | null;
  connection: string | null;
  material: string | null;
  images: string | null;
  pdf: string | null;
}

export default function ProductView({ id, onClose }: { id: number; onClose: () => void }) {
  const [product, setProduct] = useState<ProductDetails | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios
      .get(`http://127.0.0.1:8000/products/${id}`)
      .then((response) => setProduct(response.data))
      .catch(() => setError("Failed to fetch product details"))
      .finally(() => setLoading(false));
  }, [id]);

  const handleInputChange = (field: string, value: string) => {
    if (product) {
      setProduct({ ...product, [field]: value });
    }
  };

  const handleUpdate = () => {
    if (!product) return;

    axios
      .put(`http://127.0.0.1:8000/products/${id}`, product)
      .then((response) => alert("Product updated successfully"))
      .catch(() => alert("Failed to update product"));
  };

  if (loading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p className="text-red-500">{error}</p>;
  }

  return (
    <div className="p-6 bg-gray-900 text-white min-h-screen">
      <h2 className="text-3xl font-bold mb-6">Edit Product</h2>
      {product && (
        <div className="grid grid-cols-2 gap-6">
          {Object.entries(product).map(([key, value]) => (
            <div key={key}>
              <label className="block text-gray-300 text-sm font-medium mb-2 capitalize">
                {key.replace("_", " ")}
              </label>
              <input
                type="text"
                value={value ?? ""}
                onChange={(e) => handleInputChange(key, e.target.value)}
                className="w-full p-2 rounded bg-gray-800 text-white border border-gray-700 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                disabled={key === "id"}
              />
            </div>
          ))}
        </div>
      )}
      <div className="flex justify-between mt-6">
        <button
          onClick={onClose}
          className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700"
        >
          Back
        </button>
        <button
          onClick={handleUpdate}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Update
        </button>
      </div>
    </div>
  );
}
