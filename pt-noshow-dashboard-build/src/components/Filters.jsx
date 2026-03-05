import { useMemo } from 'react';

export default function Filters({ data, filters, onChange }) {
  const options = useMemo(() => {
    const therapists = [...new Set(data.map(r => r.therapist))].sort();
    const types = [...new Set(data.map(r => r.appointmentType))].sort();
    const insurers = [...new Set(data.map(r => r.insurance))].sort();
    const dates = data.map(r => r.date).sort();
    const minDate = dates[0] || '';
    const maxDate = dates[dates.length - 1] || '';
    return { therapists, types, insurers, minDate, maxDate };
  }, [data]);

  return (
    <div className="filters-bar">
      <div className="filter-group">
        <label>Date Range</label>
        <div className="date-inputs">
          <input
            type="date"
            value={filters.startDate || options.minDate}
            min={options.minDate}
            max={options.maxDate}
            onChange={e => onChange({ ...filters, startDate: e.target.value })}
          />
          <span>to</span>
          <input
            type="date"
            value={filters.endDate || options.maxDate}
            min={options.minDate}
            max={options.maxDate}
            onChange={e => onChange({ ...filters, endDate: e.target.value })}
          />
        </div>
      </div>
      <div className="filter-group">
        <label>Therapist</label>
        <select value={filters.therapist || 'All'} onChange={e => onChange({ ...filters, therapist: e.target.value })}>
          <option value="All">All Therapists</option>
          {options.therapists.map(t => <option key={t} value={t}>{t}</option>)}
        </select>
      </div>
      <div className="filter-group">
        <label>Appointment Type</label>
        <select value={filters.appointmentType || 'All'} onChange={e => onChange({ ...filters, appointmentType: e.target.value })}>
          <option value="All">All Types</option>
          {options.types.map(t => <option key={t} value={t}>{t}</option>)}
        </select>
      </div>
      <div className="filter-group">
        <label>Insurance</label>
        <select value={filters.insurance || 'All'} onChange={e => onChange({ ...filters, insurance: e.target.value })}>
          <option value="All">All Insurance</option>
          {options.insurers.map(t => <option key={t} value={t}>{t}</option>)}
        </select>
      </div>
      <button className="filter-reset" onClick={() => onChange({})}>Clear Filters</button>
    </div>
  );
}
