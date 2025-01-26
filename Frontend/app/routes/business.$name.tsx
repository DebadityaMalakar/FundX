import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom"; // Import useParams to access the URL parameter
import Navbar from "~/components/Navbar";

// Define the Business interface
interface Business {
  name: string;
  description: string;
  owner: string;
  owner_mail: string;
  owner_phone: string;
  img_blob: string;
  img_type: string | null;
  upi_id: string; // This field is still part of the interface but won't be rendered
}

const BusinessDetail: React.FC = () => {
  const { name } = useParams<{ name: string }>(); // Extract the `name` parameter from the URL
  const [business, setBusiness] = useState<Business | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchBusinessDetail = async () => {
      try {
        const url = `http://localhost:8000/api/business/${encodeURIComponent(name || "")}`; // Fetch business by name
        const response = await fetch(url);

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        setBusiness(data);
        setLoading(false);
      } catch (err) {
        setError("Failed to fetch business details.");
        setLoading(false);
        console.error(err);
      }
    };

    fetchBusinessDetail();
  }, [name]);

  if (loading) {
    return <div className="flex justify-center items-center h-screen text-white">Loading...</div>;
  }

  if (error) {
    return <div className="flex justify-center items-center h-screen text-white">{error}</div>;
  }

  if (!business) {
    return <div className="flex justify-center items-center h-screen text-white">Business not found.</div>;
  }

  return (
    <div className="bg-black text-white min-h-screen">
      <Navbar />
      <div className="container mx-auto p-4">
        <Link to="/" className="text-gray-400 hover:text-white transition-colors">
          &larr; Back to Businesses
        </Link>
        <div className="mt-8">
          <h1 className="text-3xl font-bold mb-4">{business.name}</h1>
          <p className="text-gray-400 mb-6">{business.description}</p>
          <div className="business-details text-gray-300">
            <p><strong>Owner:</strong> {business.owner}</p>
            <p><strong>Email:</strong> {business.owner_mail}</p>
            <p><strong>Phone:</strong> {business.owner_phone}</p>
          </div>
          {/* Conditionally render image if img_blob exists */}
          {business.img_blob && (
            <div className="mt-6">
              <img
                src={business.img_blob}
                alt={business.name}
                className="w-full max-w-lg h-auto rounded-lg"
                onError={(e) => {
                  // Hide the image if it fails to load
                  e.currentTarget.style.display = "none";
                }}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default BusinessDetail;