import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { API_BASE, fetchRecommendedData } from "../api";

export default function Recommended() {
  const { username } = useParams(); 

  const [problems, setProblems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProblems = async () => {
      try {
        const data = await fetchRecommendedData(username);

        if (data.error) {
          setError(data.error);
        } else {
          setProblems(data);
        }
      } catch (err) {
        console.error("Error fetching problems:", err);
        setError("Failed to connect to the server. Make sure the backend is running.");
      } finally {
        setLoading(false);
      }
    };

    fetchProblems();
  }, [username]);


  return (
    <div className="w-full flex justify-center mt-6">

      <div className="w-[80vw] bg-white rounded-xl shadow border p-6 max-w-7xl space-y-6">

        {/* Title */}
        <h2 className="text-xl font-semibold mb-4">
          📚 Recommended Problems
        </h2>

        {loading ? (
          <p className="text-gray-500">Loading problems...</p>
        ) : problems.length === 0 ? (
          <p className="text-gray-500">No recommendations available.</p>
        ) : (
          <div className="space-y-4">

            {problems.map((problem, index) => (
              <div
                key={index}
                className="p-4 border rounded-lg hover:shadow-sm transition"
              >
                {/* Problem Name */}
                <a
                  href={problem.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 font-medium hover:underline"
                >
                  {problem.name}
                </a>

                {/* Difficulty */}
                <p className="text-sm text-gray-500 mt-1">
                  Difficulty:{" "}
                  <span className="font-medium text-gray-700">
                    {problem.rating}
                  </span>
                </p>

                {/* Tags */}
                <div className="flex flex-wrap gap-2 mt-2">
                  {problem.tags.map((tag, i) => (
                    <span
                      key={i}
                      className="text-xs px-2 py-1 bg-gray-100 rounded-md"
                    >
                      {tag}
                    </span>
                  ))}
                </div>

              </div>
            ))}

          </div>
        )}

      </div>
    </div>
  );
}