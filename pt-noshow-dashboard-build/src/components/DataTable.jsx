import { useState, useMemo } from 'react';

export default function DataTable({ data }) {
  const [page, setPage] = useState(0);
  const [sortField, setSortField] = useState('date');
  const [sortDir, setSortDir] = useState('desc');
  const [statusFilter, setStatusFilter] = useState('All');
  const pageSize = 25;

  const filtered = useMemo(() => {
    let rows = statusFilter === 'All' ? data : data.filter(r => r.status === statusFilter);
    rows = [...rows].sort((a, b) => {
      const aVal = a[sortField];
      const bVal = b[sortField];
      if (aVal < bVal) return sortDir === 'asc' ? -1 : 1;
      if (aVal > bVal) return sortDir === 'asc' ? 1 : -1;
      return 0;
    });
    return rows;
  }, [data, statusFilter, sortField, sortDir]);

  const pageCount = Math.ceil(filtered.length / pageSize);
  const rows = filtered.slice(page * pageSize, (page + 1) * pageSize);

  const handleSort = (field) => {
    if (sortField === field) {
      setSortDir(d => d === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDir('asc');
    }
    setPage(0);
  };

  const statusClass = (status) => {
    if (status === 'Attended') return 'status-attended';
    if (status === 'No-Show') return 'status-noshow';
    if (status === 'Cancelled') return 'status-cancelled';
    return 'status-latecancel';
  };

  return (
    <div className="table-card">
      <div className="table-header">
        <h3>Appointment Records</h3>
        <div className="table-controls">
          <select value={statusFilter} onChange={e => { setStatusFilter(e.target.value); setPage(0); }}>
            <option value="All">All Statuses</option>
            <option value="Attended">Attended</option>
            <option value="No-Show">No-Show</option>
            <option value="Cancelled">Cancelled</option>
            <option value="Late Cancel">Late Cancel</option>
          </select>
          <span className="table-count">{filtered.length.toLocaleString()} records</span>
        </div>
      </div>
      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              {['date', 'time', 'patientId', 'therapist', 'appointmentType', 'insurance', 'status'].map(field => (
                <th key={field} onClick={() => handleSort(field)} className="sortable">
                  {field === 'patientId' ? 'Patient' :
                   field === 'appointmentType' ? 'Type' :
                   field.charAt(0).toUpperCase() + field.slice(1)}
                  {sortField === field && (sortDir === 'asc' ? ' ↑' : ' ↓')}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map(r => (
              <tr key={r.id}>
                <td>{r.date}</td>
                <td>{r.time}</td>
                <td>{r.patientId}</td>
                <td>{r.therapist}</td>
                <td>{r.appointmentType}</td>
                <td>{r.insurance}</td>
                <td><span className={`status-badge ${statusClass(r.status)}`}>{r.status}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="table-pagination">
        <button onClick={() => setPage(p => Math.max(0, p - 1))} disabled={page === 0}>Previous</button>
        <span>Page {page + 1} of {pageCount}</span>
        <button onClick={() => setPage(p => Math.min(pageCount - 1, p + 1))} disabled={page >= pageCount - 1}>Next</button>
      </div>
    </div>
  );
}
