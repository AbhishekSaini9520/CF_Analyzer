import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { fetchRatingData, fetchRecommendedData, fetchDashboardData } from "../api";

export default function Home() {
  const [username, setUsername] = useState("");
  const navigate = useNavigate();

  const handleSubmit = () => {
    if (!username.trim()) return;

    fetchRatingData(username.trim());
    fetchRecommendedData(username.trim());
    fetchDashboardData(username.trim());

    navigate(`/dashboard/${username.trim()}`);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">

      <div className="bg-white p-8 rounded-xl shadow border w-[80vw] max-w-xl text-center">

        {/* Title */}
        <h1 className="text-2xl font-bold mb-4">
          Codeforces Analyzer
        </h1>

        <p className="text-gray-500 mb-6">
          Enter your username to analyze your performance
        </p>

        {/* Input */}
        <div className="flex gap-2">
          <input
            type="text"
            placeholder="Enter Codeforces handle..."
            className="flex-1 px-4 py-2 border rounded-lg outline-none focus:ring-2 focus:ring-blue-500"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
          />

          <button
            onClick={handleSubmit}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Analyze
          </button>
        </div>

      </div>
    </div>
  );
}