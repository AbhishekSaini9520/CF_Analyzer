const Heatmap = ({ data }) => {
    const generateGrid = () => {
        const today = new Date();
        const start = new Date();
        start.setDate(today.getDate() - 364); 
        const days = [];

        for (let d = new Date(start); d <= today; d.setDate(d.getDate() + 1)) {
            const dateStr = d.toISOString().split("T")[0];

            days.push({
                date: dateStr,
                count: data[dateStr] || 0,
            });
        }

        return days;
    };

    const getColor = (count) => {
        if (count === 0) return "bg-gray-200";
        if (count < 3) return "bg-blue-200";
        if (count < 6) return "bg-blue-400";
        if (count < 10) return "bg-blue-600";
        return "bg-blue-900";
    };

    const days = generateGrid();

    return (
        <div className="overflow-x-auto">
            <div className="grid grid-rows-7 grid-flow-col gap-1">
                {days.map((day, i) => (
                    <div
                        key={i}
                        className={`w-3 h-3 rounded-sm ${getColor(day.count)}`}
                        title={`${day.date} - ${day.count}`}
                    />
                ))}
            </div>
        </div>
    );
};

export default Heatmap;