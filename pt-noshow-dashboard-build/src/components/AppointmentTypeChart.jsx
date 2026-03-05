import { useMemo } from 'react';
import {
  PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend
} from 'recharts';

const COLORS = ['#6366f1', '#ef4444', '#f59e0b', '#10b981', '#8b5cf6'];

export default function AppointmentTypeChart({ data }) {
  const chartData = useMemo(() => {
    const types = {};
    data.forEach(r => {
      if (!types[r.appointmentType]) types[r.appointmentType] = { total: 0, noShows: 0 };
      types[r.appointmentType].total++;
      if (r.status === 'No-Show') types[r.appointmentType].noShows++;
    });

    return Object.entries(types)
      .map(([type, counts]) => ({
        name: type,
        noShowRate: Number(((counts.noShows / counts.total) * 100).toFixed(1)),
        noShows: counts.noShows,
        total: counts.total,
      }))
      .sort((a, b) => b.noShowRate - a.noShowRate);
  }, [data]);

  return (
    <div className="chart-card">
      <h3>No-Show Rate by Appointment Type</h3>
      <ResponsiveContainer width="100%" height={280}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            outerRadius={100}
            innerRadius={55}
            dataKey="noShows"
            nameKey="name"
            label={({ name, noShowRate }) => `${name}: ${noShowRate}%`}
            labelLine={{ stroke: '#ccc' }}
          >
            {chartData.map((entry, index) => (
              <Cell key={index} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{ borderRadius: 8, border: '1px solid #e5e5e5', fontSize: 13 }}
            formatter={(value, name, props) => [
              `${props.payload.noShowRate}% (${value} of ${props.payload.total})`,
              'No-Show Rate'
            ]}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
