import { useMemo } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell
} from 'recharts';

export default function TimeSlotChart({ data }) {
  const chartData = useMemo(() => {
    const slots = {};
    data.forEach(r => {
      if (!slots[r.time]) slots[r.time] = { total: 0, noShows: 0 };
      slots[r.time].total++;
      if (r.status === 'No-Show') slots[r.time].noShows++;
    });

    const order = ['8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM'];
    return order.filter(t => slots[t]).map(time => ({
      time,
      'No-Show Rate': Number(((slots[time].noShows / slots[time].total) * 100).toFixed(1)),
      count: slots[time].noShows,
    }));
  }, [data]);

  const getBarColor = (rate) => {
    if (rate >= 20) return '#ef4444';
    if (rate >= 15) return '#f59e0b';
    return '#10b981';
  };

  return (
    <div className="chart-card">
      <h3>No-Show Rate by Time Slot</h3>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={chartData} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis dataKey="time" tick={{ fontSize: 11, fill: '#6b6b6b' }} />
          <YAxis tick={{ fontSize: 12, fill: '#6b6b6b' }} unit="%" />
          <Tooltip
            contentStyle={{ borderRadius: 8, border: '1px solid #e5e5e5', fontSize: 13 }}
            formatter={(value, name, props) => [`${value}% (${props.payload.count} no-shows)`, 'No-Show Rate']}
          />
          <Bar dataKey="No-Show Rate" radius={[6, 6, 0, 0]} maxBarSize={50}>
            {chartData.map((entry, index) => (
              <Cell key={index} fill={getBarColor(entry['No-Show Rate'])} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
