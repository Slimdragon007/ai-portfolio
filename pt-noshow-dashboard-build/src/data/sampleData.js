// Sample PT clinic appointment data (6 months, realistic patterns)
// No-show rates in PT clinics typically run 10-25%

function generateSampleData() {
  const therapists = ['Dr. Rivera', 'Dr. Chen', 'Dr. Patel', 'Dr. Thompson'];
  const appointmentTypes = ['Initial Eval', 'Follow-Up', 'Post-Op Rehab', 'Sports Rehab', 'Manual Therapy'];
  const insuranceTypes = ['Blue Cross', 'Aetna', 'UnitedHealth', 'Medicare', 'Self-Pay', 'Cigna'];
  const timeSlots = ['8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM'];
  const statuses = ['Attended', 'No-Show', 'Cancelled', 'Late Cancel'];

  const records = [];
  const startDate = new Date('2025-09-01');
  const endDate = new Date('2026-03-01');

  // Weighted status selection (realistic distribution)
  function pickStatus(dayOfWeek, timeSlot, appointmentType) {
    const rand = Math.random();
    // Mondays and Fridays have higher no-show rates
    const dayBump = (dayOfWeek === 1 || dayOfWeek === 5) ? 0.06 : 0;
    // Early morning and late afternoon higher no-show
    const timeBump = (timeSlot === '8:00 AM' || timeSlot === '5:00 PM') ? 0.04 : 0;
    // Follow-ups have higher no-show than initial evals
    const typeBump = appointmentType === 'Follow-Up' ? 0.05 : appointmentType === 'Initial Eval' ? -0.03 : 0;

    const noShowThreshold = 0.15 + dayBump + timeBump + typeBump;
    const cancelThreshold = noShowThreshold + 0.08;
    const lateCancelThreshold = cancelThreshold + 0.05;

    if (rand < noShowThreshold) return 'No-Show';
    if (rand < cancelThreshold) return 'Cancelled';
    if (rand < lateCancelThreshold) return 'Late Cancel';
    return 'Attended';
  }

  let id = 1;
  const current = new Date(startDate);

  while (current < endDate) {
    const dayOfWeek = current.getDay();
    // Skip weekends
    if (dayOfWeek === 0 || dayOfWeek === 6) {
      current.setDate(current.getDate() + 1);
      continue;
    }

    // 20-30 appointments per day
    const dailyCount = Math.floor(Math.random() * 11) + 20;

    for (let i = 0; i < dailyCount; i++) {
      const therapist = therapists[Math.floor(Math.random() * therapists.length)];
      const type = appointmentTypes[Math.floor(Math.random() * appointmentTypes.length)];
      const insurance = insuranceTypes[Math.floor(Math.random() * insuranceTypes.length)];
      const time = timeSlots[Math.floor(Math.random() * timeSlots.length)];
      const status = pickStatus(dayOfWeek, time, type);
      const patientAge = Math.floor(Math.random() * 55) + 18;
      const visitNumber = Math.floor(Math.random() * 12) + 1;

      records.push({
        id: id++,
        date: current.toISOString().split('T')[0],
        dayOfWeek: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'][dayOfWeek],
        time,
        patientId: `PT-${String(Math.floor(Math.random() * 500) + 100).padStart(4, '0')}`,
        patientAge,
        therapist,
        appointmentType: type,
        insurance,
        visitNumber,
        status,
        reminderSent: Math.random() > 0.1 ? 'Yes' : 'No',
      });
    }

    current.setDate(current.getDate() + 1);
  }

  return records;
}

export const sampleData = generateSampleData();

export function parseCSVData(csvText) {
  // Maps CSV columns to our internal format
  return csvText;
}

export const CSV_HEADERS = [
  'date', 'dayOfWeek', 'time', 'patientId', 'patientAge',
  'therapist', 'appointmentType', 'insurance', 'visitNumber',
  'status', 'reminderSent'
];
