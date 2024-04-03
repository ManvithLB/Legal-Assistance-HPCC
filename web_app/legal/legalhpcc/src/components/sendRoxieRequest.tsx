import axios from "axios";

const flaskUrl = "http://localhost:5000/sendroxie";

const sendRoxieRequest = async (filteredKeywords) => {
  try {
    const keywordsString = filteredKeywords.join(", ");
    console.log(keywordsString);
    const payload = {
      keywords: keywordsString,
    };

    const response = await axios.post(flaskUrl, payload);
    console.log(response);
    return response.data;
  } catch (error) {
    console.error("Error sending request to Flask:", error);
    throw error; // You can handle the error appropriately in the component
  }
};

export default sendRoxieRequest;
