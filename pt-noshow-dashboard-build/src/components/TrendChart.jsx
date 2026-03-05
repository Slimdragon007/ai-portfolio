import { useMemo } from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend
} from 'recharts';

export default function TrendChart({ data }) {
  const chartData = useMemo(() => {
    // Group by week
    const weeks = {};
    data.forEach(r => {
      const d = new Date(r.date);
      // Get Monday of the week
      const day = d.getDay();
      const diff = d.getDate() - day + (day === 0 ? -6 : 1);
      const monday = new Date(d.setDate(diff));
      const weekKey = monday.toISOString().split('T')[0];

      if (!weeks[weekKey]) {
        weeks[weekKey] = { total: 0, noShows: 0, cancellations: 0, attended: 0 };
      }
      weeks[weekKey].total++;
      if (r.status === 'No-Show') weeks[weekKey].noShows++;
      if (r.status === 'Cancelled' || r.status === 'Late Cancel') weeks[weekKey].cancellations++;
      if (r.status === 'Attended') weeks[weekKey].attended++;
    });

    return Object.entries(weeks)
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([week, counts]) => ({
        week: new Date(week).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
        'No-Show %': Number(((counts.noShows / counts.total) * 100).toFixed(1)),
        'Cancel %': Number(((counts.cancellations / counts.total) * 100).toFixed(1)),
        'Attendance %': Number(((counts.attended / counts.total) * 100).toFixed(1)),
      }));
  }, [data]);

  return (
    <div className="chart-card">
      <h3>Weekly Trends</h3>
      <ResponsiveContainer width="100%" height={320}>
        <LineChart data={chartData} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis dataKey="week" tick={{ fontSize: 12, fill: '#6b6b6b' }} interval="preserveStartEnd" />
          <YAxis tick={{ fontSize: 12, fill: '#6b6b6b' }} unit="%" />
          <Tooltip
            contentStyle={{ borderRadius: 8, border: '1px solid #e5e5e5', fontSize: 13 }}
            formatter={(value) => [`${value}%`]}
          />
          <Legend wrapperStyle={{ fontSize: 13 }} />
          <Line type="monotone" dataKey="No-Show %" stroke="#ef4444" strokeWidth={2} dot={false} />
          <Line type="monotone" dataKey="Cancel %" stroke="#f59e0b" strokeWidth={2} dot={false} />
          <Line type="monotone" dataKey="Attendance %" stroke="#10b981" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
