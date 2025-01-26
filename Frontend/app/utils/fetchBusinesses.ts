// util.ts

// Define the structure of a business object
interface Business {
    name: string;
    description: string;
    owner: string;
    owner_mail: string;
    owner_phone: string;
    img_blob: string;
    img_type: string | null;
    upi_id: string;
  }
  
  // Function to fetch and parse business details from the server
  export async function fetchAndParseBusinessDetails(url: string): Promise<Business[]> {
    try {
      // Fetch data from the server
      const response = await fetch(url);
  
      // Check if the response is OK (status code 200-299)
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
  
      // Parse the JSON data
      const data = await response.json();
  
      // Check if the 'businesses' key exists and is an array
      if (data.businesses && Array.isArray(data.businesses)) {
        // Map through the businesses array and return the details
        return data.businesses.map((business: Business) => ({
          name: business.name,
          description: business.description,
          owner: business.owner,
          owner_mail: business.owner_mail,
          owner_phone: business.owner_phone,
          img_blob: `${business.img_blob}`,
          img_type: business.img_type,
          upi_id: business.upi_id,
        }));
      } else {
        throw new Error("Invalid JSON structure: 'businesses' key not found or not an array");
      }
    } catch (error) {
      console.error("Error fetching or parsing data:", error);
      return [];
    }
  }
  
//   // Example usage
//   const url = "http://localhost:8000"; // Replace with the actual endpoint if needed
//   fetchAndParseBusinessDetails(url)
//     .then((businesses) => {
//       console.log("Fetched Business Details:", businesses);
//     })
//     .catch((error) => {
//       console.error("Error in example usage:", error);
//     });