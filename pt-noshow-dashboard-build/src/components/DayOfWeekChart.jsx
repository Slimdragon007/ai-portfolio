import { useMemo } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell
} from 'recharts';

export default function DayOfWeekChart({ data }) {
  const chartData = useMemo(() => {
    const days = { Mon: { total: 0, noShows: 0 }, Tue: { total: 0, noShows: 0 }, Wed: { total: 0, noShows: 0 }, Thu: { total: 0, noShows: 0 }, Fri: { total: 0, noShows: 0 } };

    data.forEach(r => {
      if (days[r.dayOfWeek]) {
        days[r.dayOfWeek].total++;
        if (r.status === 'No-Show') days[r.dayOfWeek].noShows++;
      }
    });

    return Object.entries(days).map(([day, counts]) => ({
      day,
      'No-Show Rate': counts.total > 0 ? Number(((counts.noShows / counts.total) * 100).toFixed(1)) : 0,
    }));
  }, [data]);

  const getBarColor = (rate) => {
    if (rate >= 20) return '#ef4444';
    if (rate >= 15) return '#f59e0b';
    return '#10b981';
  };

  return (
    <div className="chart-card">
      <h3>No-Show Rate by Day of Week</h3>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={chartData} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis dataKey="day" tick={{ fontSize: 13, fill: '#6b6b6b' }} />
          <YAxis tick={{ fontSize: 12, fill: '#6b6b6b' }} unit="%" />
          <Tooltip
            contentStyle={{ borderRadius: 8, border: '1px solid #e5e5e5', fontSize: 13 }}
            formatter={(value) => [`${value}%`, 'No-Show Rate']}
          />
          <Bar dataKey="No-Show Rate" radius={[6, 6, 0, 0]} maxBarSize={60}>
            {chartData.map((entry, index) => (
              <Cell key={index} fill={getBarColor(entry['No-Show Rate'])} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
