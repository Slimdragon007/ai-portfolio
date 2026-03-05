import { useMemo } from 'react';

export default function KPICards({ data, dateRange }) {
  const metrics = useMemo(() => {
    const filtered = dateRange
      ? data.filter(r => r.date >= dateRange.start && r.date <= dateRange.end)
      : data;

    const total = filtered.length;
    const noShows = filtered.filter(r => r.status === 'No-Show').length;
    const cancellations = filtered.filter(r => r.status === 'Cancelled').length;
    const lateCancels = filtered.filter(r => r.status === 'Late Cancel').length;
    const attended = filtered.filter(r => r.status === 'Attended').length;

    const noShowRate = total > 0 ? ((noShows / total) * 100).toFixed(1) : 0;
    const cancelRate = total > 0 ? (((cancellations + lateCancels) / total) * 100).toFixed(1) : 0;
    const attendRate = total > 0 ? ((attended / total) * 100).toFixed(1) : 0;

    // Estimated revenue lost (avg PT visit = $150)
    const revenueLost = (noShows + lateCancels) * 150;

    return { total, noShows, cancellations, lateCancels, attended, noShowRate, cancelRate, attendRate, revenueLost };
  }, [data, dateRange]);

  const cards = [
    { label: 'Total Appointments', value: metrics.total.toLocaleString(), color: '#6366f1' },
    { label: 'No-Show Rate', value: `${metrics.noShowRate}%`, sub: `${metrics.noShows} no-shows`, color: '#ef4444' },
    { label: 'Cancellation Rate', value: `${metrics.cancelRate}%`, sub: `${metrics.cancellations + metrics.lateCancels} cancelled`, color: '#f59e0b' },
    { label: 'Attendance Rate', value: `${metrics.attendRate}%`, sub: `${metrics.attended} attended`, color: '#10b981' },
    { label: 'Est. Revenue Lost', value: `$${metrics.revenueLost.toLocaleString()}`, sub: 'from no-shows + late cancels', color: '#ef4444' },
  ];

  return (
    <div className="kpi-grid">
      {cards.map((card) => (
        <div key={card.label} className="kpi-card">
          <div className="kpi-indicator" style={{ backgroundColor: card.color }} />
          <div className="kpi-label">{card.label}</div>
          <div className="kpi-value" style={{ color: card.color }}>{card.value}</div>
          {card.sub && <div className="kpi-sub">{card.sub}</div>}
        </div>
      ))}
    </div>
  );
}
