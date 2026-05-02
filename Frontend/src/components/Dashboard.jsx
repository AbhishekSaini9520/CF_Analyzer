import { useEffect, useState } from "react";
import Heatmap from "./Heatmap";
import { useParams } from "react-router-dom";
import { fetchDashboardData } from "../api";

const Dashboard = () => {
    const { username } = useParams();
    const [data, setData] = useState(null);

    const getCFColor = (rating) => {
        if (!rating) return "text-gray-400";

        if (rating < 1200) return "text-gray-500";
        if (rating < 1400) return "text-green-600";
        if (rating < 1600) return "text-cyan-500";
        if (rating < 1900) return "text-blue-600";
        if (rating < 2100) return "text-purple-600";
        if (rating < 2300) return "text-orange-500";
        if (rating < 2400) return "text-orange-600";
        if (rating < 2600) return "text-red-500";
        return "text-red-700";
    };

    useEffect(() => {
        const fetchDashboard = async () => {
            try {
                const data = await fetchDashboardData(username)
                setData(data);
            } catch (err) {
                console.error(err);
            }
        };

        fetchDashboard();
    }, []);

    if (!data) return <div className="p-6">Loading...</div>;

    const {
        user,
        stats,
        heatmap,
        difficulty_chart_path,
    } = data;

    return (
        <div className="w-full flex justify-center mt-6">
            <div className="w-[80vw] bg-white rounded-xl shadow border p-6 max-w-7xl space-y-6">
                {/* ===== HEADER ===== */}
                <div className="flex justify-between items-start mb-8">
                    <div>
                        <span className="text-xs bg-gray-200 px-3 py-1 rounded-full">
                            COMPETITIVE IDENTITY
                        </span>

                        <h1 className="text-5xl font-bold mt-4">
                            {user.name}
                        </h1>

                        <p className="text-blue-600 mt-1">@{user.handle}</p>

                        <div className="flex gap-10 mt-6 text-sm text-gray-600">
                            <div>
                                <p className="text-xs">CURRENT RATING</p>
                                <p className={`text-2xl font-semibold ${getCFColor(user.rating)}`}>
                                    {user.rating}
                                </p>
                            </div>
                            <div>
                                <p className="text-xs">GLOBAL RANK</p>
                                <p className={`font-semibold ${getCFColor(user.rating)}`}>
                                    {user.rank || "Unrated"}
                                </p>
                            </div>

                            <div>
                                <p className="text-xs">LOCATION</p>
                                <p>{user.location || "Not specified"}</p>
                            </div>

                            <div>
                                <p className="text-xs">INSTITUTION</p>
                                <p>{user.institution || "Not specified"}</p>
                            </div>
                        </div>
                    </div>

                    {/* Profile Image */}
                    <img
                        src={user.avatar}
                        alt="profile"
                        className="w-40 h-40 rounded-xl object-cover"
                    />
                </div>

                {/* ===== STATS CARDS ===== */}
                <div className="grid grid-cols-4 gap-4 mb-8">
                    <StatCard title="TOTAL SOLVED" value={stats.totalSolved} />
                    <StatCard title="SOLVED THIS YEAR" value={stats.solvedThisYear} />
                    <StatCard title="MAX STREAK" value={`${stats.maxStreak} days`} />
                    <StatCard title="CURRENT STREAK" value={`${stats.currentStreak} days`} />
                </div>

                {/* ===== HEATMAP ===== */}
                <div className="bg-white p-5 rounded-xl shadow mb-8">
                    <div className="flex justify-between mb-4">
                        <h2 className="font-semibold">
                            Submission Laboratory Activity
                        </h2>

                        <div className="flex items-center gap-1 text-xs text-gray-500">
                            <span>LESS</span>
                            <div className="flex gap-1">
                                <div className="w-3 h-3 bg-gray-200"></div>
                                <div className="w-3 h-3 bg-blue-200"></div>
                                <div className="w-3 h-3 bg-blue-400"></div>
                                <div className="w-3 h-3 bg-blue-600"></div>
                                <div className="w-3 h-3 bg-blue-900"></div>
                            </div>
                            <span>MORE</span>
                        </div>
                    </div>

                    <Heatmap data={heatmap} />
                </div>

                {/* ===== DIFFICULTY DISTRIBUTION ===== */}
                <div className="bg-white p-5 rounded-xl shadow">
                    <h2 className="font-semibold mb-4">
                        Problem Difficulty Distribution
                    </h2>

                    <img
                        src={`http://localhost:5000/${difficulty_chart_path}`}
                        alt="difficulty chart"
                        className="w-full object-contain"
                    />
                </div>
            </div>
        </div>
    );
};

const StatCard = ({ title, value }) => (
    <div className="bg-white p-4 rounded-xl shadow">
        <p className="text-xs text-gray-500">{title}</p>
        <p className="text-2xl font-semibold mt-2">{value}</p>
    </div>
);

export default Dashboard;