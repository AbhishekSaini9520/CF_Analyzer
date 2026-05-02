import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { API_BASE, fetchRatingData } from "../api";

export default function RatingCard() {
  const { username } = useParams();

  const [rating, setRating] = useState(null);
  const [ratingImg, setRatingImg] = useState("");
  const [profileImg, setProfileImg] = useState("");
  const [pieImg, setPieImg] = useState("");
  const [barImg, setBarImg] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!username) return;

    const fetchData = async () => {
      try {
        const data = await fetchRatingData(username);

        if (data.error) {
          setError(data.error);
          return;
        }
        // console.log(data);
        setRating(data.rating);
        setRatingImg(API_BASE + data.rating_graph);
        setPieImg(API_BASE + data.pie_chart);
        setBarImg(API_BASE + data.bar_chart);
        setProfileImg(data.profile_img);
        // console.log(data.profile_img)
      } catch (err) {
        console.error(err);
        setError("Failed to connect to the server. Make sure the backend is running.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [username]);

  return (
    <div className="w-full flex justify-center mt-6">

      {loading ? (
        <div className="bg-white p-4 rounded-xl shadow border text-gray-500 w-[80vw] text-center">
          Loading dashboard...
        </div>
      ) : (
        <div className="bg-white p-6 rounded-xl shadow border w-[80vw] max-w-7xl space-y-6">

          {/* Title */}

          {/* Rating */}
          <div>
            <div className="flex grid grid-cols-2 gap-4">
              <div>
                <h2 className="text-xl font-semibold pb-2">
                  📊 Performance Dashboard
                </h2>
                <p className="text-sm text-gray-500">Current Rating</p>
                <p className="text-3xl font-bold text-blue-600">
                  {rating}
                </p>
              </div>

              <div className="w-32 ml-auto justify-self-end mr-10">
                <img src={profileImg} alt="Profile" />
              </div>
            </div>
          </div>

          {/* Rating Graph */}
          {ratingImg && (
            <div>
              <p className="text-sm text-gray-500 mb-2">Rating Trend</p>
              <img
                src={ratingImg}
                alt="Rating Graph"
                className="w-full rounded-lg border"
              />
            </div>
          )}

          {/* Pie Chart */}
          {pieImg && (
            <div className="w-full">
              <p className="text-sm text-gray-500 mb-2">Problem Distribution</p>
              <img
                src={pieImg}
                alt="Pie Chart"
                className="w-full h-auto block rounded-lg border"
              />
            </div>
          )}

          {/* Bar Chart */}
          {barImg && (
            <div>
              <p className="text-sm text-gray-500 mb-2">
                Topic Strength
              </p>
              <img
                src={barImg}
                alt="Bar Chart"
                className="w-full rounded-lg border"
              />
            </div>
          )}

        </div>
      )}

    </div>
  );
}