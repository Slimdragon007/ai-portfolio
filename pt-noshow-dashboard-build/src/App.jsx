import { useState, useMemo } from 'react';
import { sampleData } from './data/sampleData';
import KPICards from './components/KPICards';
import TrendChart from './components/TrendChart';
import DayOfWeekChart from './components/DayOfWeekChart';
import TimeSlotChart from './components/TimeSlotChart';
import TherapistChart from './components/TherapistChart';
import AppointmentTypeChart from './components/AppointmentTypeChart';
import InsuranceChart from './components/InsuranceChart';
import ReminderImpact from './components/ReminderImpact';
import DataTable from './components/DataTable';
import CSVUpload from './components/CSVUpload';
import Filters from './components/Filters';
import './App.css';

export default function App() {
  const [rawData, setRawData] = useState(sampleData);
  const [isCustomData, setIsCustomData] = useState(false);
  const [filters, setFilters] = useState({});

  const filteredData = useMemo(() => {
    let rows = rawData;
    if (filters.startDate) rows = rows.filter(r => r.date >= filters.startDate);
    if (filters.endDate) rows = rows.filter(r => r.date <= filters.endDate);
    if (filters.therapist && filters.therapist !== 'All') rows = rows.filter(r => r.therapist === filters.therapist);
    if (filters.appointmentType && filters.appointmentType !== 'All') rows = rows.filter(r => r.appointmentType === filters.appointmentType);
    if (filters.insurance && filters.insurance !== 'All') rows = rows.filter(r => r.insurance === filters.insurance);
    return rows;
  }, [rawData, filters]);

  const dateRange = useMemo(() => {
    if (filteredData.length === 0) return null;
    const dates = filteredData.map(r => r.date).sort();
    return { start: dates[0], end: dates[dates.length - 1] };
  }, [filteredData]);

  const handleDataLoaded = (data) => {
    setRawData(data);
    setIsCustomData(true);
    setFilters({});
  };

  const handleReset = () => {
    setRawData(sampleData);
    setIsCustomData(false);
    setFilters({});
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <div>
            <h1>PT No-Show Dashboard</h1>
            <p className="header-sub">
              {isCustomData ? 'Viewing uploaded data' : 'Viewing sample data (Sep 2025 - Feb 2026)'}
              {' · '}{filteredData.length.toLocaleString()} appointments
            </p>
          </div>
          <CSVUpload onDataLoaded={handleDataLoaded} onReset={handleReset} />
        </div>
      </header>

      <main className="dashboard">
        <Filters data={rawData} filters={filters} onChange={setFilters} />
        <KPICards data={filteredData} dateRange={dateRange} />

        <section className="chart-row">
          <TrendChart data={filteredData} />
        </section>

        <section className="chart-row two-col">
          <DayOfWeekChart data={filteredData} />
          <TimeSlotChart data={filteredData} />
        </section>

        <section className="chart-row two-col">
          <TherapistChart data={filteredData} />
          <AppointmentTypeChart data={filteredData} />
        </section>

        <section className="chart-row two-col">
          <InsuranceChart data={filteredData} />
          <ReminderImpact data={filteredData} />
        </section>

        <section className="chart-row">
          <DataTable data={filteredData} />
        </section>
      </main>

      <footer className="app-footer">
        <p>PT No-Show Dashboard · Built by <a href="https://michaelhaslim.github.io/ai-portfolio" target="_blank" rel="noopener noreferrer">FlowstateAI</a></p>
      </footer>
    </div>
  );
}
