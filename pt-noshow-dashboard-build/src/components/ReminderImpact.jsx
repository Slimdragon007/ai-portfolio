import { useMemo } from 'react';

export default function ReminderImpact({ data }) {
  const stats = useMemo(() => {
    const withReminder = data.filter(r => r.reminderSent === 'Yes');
    const withoutReminder = data.filter(r => r.reminderSent === 'No');

    const rateWith = withReminder.length > 0
      ? ((withReminder.filter(r => r.status === 'No-Show').length / withReminder.length) * 100).toFixed(1)
      : 0;
    const rateWithout = withoutReminder.length > 0
      ? ((withoutReminder.filter(r => r.status === 'No-Show').length / withoutReminder.length) * 100).toFixed(1)
      : 0;

    return { rateWith, rateWithout, countWith: withReminder.length, countWithout: withoutReminder.length };
  }, [data]);

  return (
    <div className="chart-card reminder-card">
      <h3>Reminder Impact</h3>
      <div className="reminder-comparison">
        <div className="reminder-stat">
          <div className="reminder-label">With Reminder</div>
          <div className="reminder-value green">{stats.rateWith}%</div>
          <div className="reminder-sub">no-show rate ({stats.countWith.toLocaleString()} appts)</div>
        </div>
        <div className="reminder-vs">vs</div>
        <div className="reminder-stat">
          <div className="reminder-label">Without Reminder</div>
          <div className="reminder-value red">{stats.rateWithout}%</div>
          <div className="reminder-sub">no-show rate ({stats.countWithout.toLocaleString()} appts)</div>
        </div>
      </div>
    </div>
  );
}
