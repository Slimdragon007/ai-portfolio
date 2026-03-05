import { useMemo } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend
} from 'recharts';

export default function TherapistChart({ data }) {
  const chartData = useMemo(() => {
    const therapists = {};
    data.forEach(r => {
      if (!therapists[r.therapist]) {
        therapists[r.therapist] = { total: 0, attended: 0, noShows: 0, cancelled: 0 };
      }
      therapists[r.therapist].total++;
      if (r.status === 'Attended') therapists[r.therapist].attended++;
      if (r.status === 'No-Show') therapists[r.therapist].noShows++;
      if (r.status === 'Cancelled' || r.status === 'Late Cancel') therapists[r.therapist].cancelled++;
    });

    return Object.entries(therapists)
      .sort(([, a], [, b]) => (b.noShows / b.total) - (a.noShows / a.total))
      .map(([name, counts]) => ({
        name,
        'Attended': Number(((counts.attended / counts.total) * 100).toFixed(1)),
        'No-Show': Number(((counts.noShows / counts.total) * 100).toFixed(1)),
        'Cancelled': Number(((counts.cancelled / counts.total) * 100).toFixed(1)),
        totalAppts: counts.total,
      }));
  }, [data]);

  return (
    <div className="chart-card">
      <h3>Status Breakdown by Therapist</h3>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={chartData} layout="vertical" margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis type="number" unit="%" tick={{ fontSize: 12, fill: '#6b6b6b' }} />
          <YAxis type="category" dataKey="name" tick={{ fontSize: 12, fill: '#6b6b6b' }} width={100} />
          <Tooltip
            contentStyle={{ borderRadius: 8, border: '1px solid #e5e5e5', fontSize: 13 }}
            formatter={(value, name, props) => [`${value}%`, name]}
          />
          <Legend wrapperStyle={{ fontSize: 13 }} />
          <Bar dataKey="Attended" stackId="a" fill="#10b981" radius={[0, 0, 0, 0]} />
          <Bar dataKey="No-Show" stackId="a" fill="#ef4444" />
          <Bar dataKey="Cancelled" stackId="a" fill="#f59e0b" radius={[0, 6, 6, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
