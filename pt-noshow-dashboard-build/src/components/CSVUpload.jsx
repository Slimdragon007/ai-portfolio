import { useRef } from 'react';
import Papa from 'papaparse';

export default function CSVUpload({ onDataLoaded, onReset }) {
  const fileRef = useRef();

  const handleUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    Papa.parse(file, {
      header: true,
      skipEmptyLines: true,
      complete: (results) => {
        const rows = results.data.map((row, i) => {
          // Normalize column names (handle various CSV formats)
          const normalized = {};
          Object.entries(row).forEach(([key, val]) => {
            normalized[key.trim().toLowerCase().replace(/\s+/g, '_')] = val?.trim();
          });

          const date = normalized.date || normalized.appointment_date || '';
          const d = new Date(date);
          const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

          return {
            id: i + 1,
            date,
            dayOfWeek: isNaN(d) ? '' : dayNames[d.getDay()],
            time: normalized.time || normalized.appointment_time || normalized.time_slot || '',
            patientId: normalized.patient_id || normalized.patientid || normalized.patient || `P-${i}`,
            patientAge: parseInt(normalized.patient_age || normalized.age || '0') || 0,
            therapist: normalized.therapist || normalized.provider || normalized.doctor || 'Unknown',
            appointmentType: normalized.appointment_type || normalized.type || normalized.visit_type || 'General',
            insurance: normalized.insurance || normalized.insurance_type || normalized.payer || 'Unknown',
            visitNumber: parseInt(normalized.visit_number || normalized.visit_num || '1') || 1,
            status: normalizeStatus(normalized.status || normalized.appointment_status || ''),
            reminderSent: normalized.reminder_sent || normalized.reminder || 'Unknown',
          };
        }).filter(r => r.date);

        if (rows.length > 0) {
          onDataLoaded(rows);
        } else {
          alert('No valid records found. Make sure your CSV has a "date" column and a "status" column.');
        }
      },
      error: () => {
        alert('Error reading CSV file. Please check the format and try again.');
      }
    });
  };

  function normalizeStatus(raw) {
    const s = raw.toLowerCase();
    if (s.includes('no') && s.includes('show')) return 'No-Show';
    if (s.includes('late') && s.includes('cancel')) return 'Late Cancel';
    if (s.includes('cancel')) return 'Cancelled';
    if (s.includes('attend') || s.includes('complet') || s.includes('kept') || s.includes('show')) return 'Attended';
    return raw || 'Unknown';
  }

  return (
    <div className="csv-upload">
      <input
        ref={fileRef}
        type="file"
        accept=".csv"
        onChange={handleUpload}
        style={{ display: 'none' }}
      />
      <button className="upload-btn" onClick={() => fileRef.current.click()}>
        Upload Your CSV
      </button>
      <button className="reset-btn" onClick={onReset}>
        Reset to Sample Data
      </button>
    </div>
  );
}
