import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom"; // Import Link for navigation
import Navbar from "~/components/Navbar";
import { fetchAndParseBusinessDetails } from "~/utils/fetchBusinesses";

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

const Business: React.FC = () => {
  const [businesses, setBusinesses] = useState<Business[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const url = "http://localhost:8000/api/businesses"; // Replace with the actual endpoint if needed
        const data = await fetchAndParseBusinessDetails(url);
        setBusinesses(data);
        setLoading(false);
      } catch (err) {
        setError("Failed to fetch business data.");
        setLoading(false);
        console.error(err);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div className="flex justify-center items-center h-screen text-white">Loading...</div>;
  }

  if (error) {
    return <div className="flex justify-center items-center h-screen text-white">{error}</div>;
  }

  return (
    <div className="bg-black text-white min-h-screen">
      <Navbar />
      <div className="container mx-auto p-4">
        <h1 className="text-2xl font-bold mb-8 text-center">Businesses</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {businesses.map((business, index) => (
            <Link
              to={`/business/${encodeURIComponent(business.name)}`} // Navigate to /business/{name}
              key={index}
              className="block transform transition-transform hover:scale-105 focus:scale-105"
            >
              <div className="business-card p-6 border border-gray-700 rounded-lg shadow-lg bg-gray-800 hover:bg-gray-700 transition-colors">
                <h2 className="text-xl font-semibold mb-2">{business.name}</h2>
                <p className="text-gray-400 mb-4">{business.description}</p>
                <div className="business-details text-gray-300">
                  <p><strong>Owner:</strong> {business.owner}</p>
                  <p><strong>Email:</strong> {business.owner_mail}</p>
                  <p><strong>Phone:</strong> {business.owner_phone}</p>
                </div>
                {/* Conditionally render image if img_blob exists */}
                {business.img_blob && (
                  <div className="mt-4">
                    <img
                      src={business.img_blob}
                      alt={business.name}
                      className="w-full h-48 object-cover rounded-lg"
                      onError={(e) => {
                        // Hide the image if it fails to load
                        e.currentTarget.style.display = "none";
                      }}
                    />
                  </div>
                )}
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Business;