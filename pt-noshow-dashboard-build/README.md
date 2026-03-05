# PT No-Show Dashboard

Analytics dashboard for tracking and reducing physical therapy appointment no-shows. Visualizes patterns by day, time, therapist, appointment type, and insurance to help clinics take action.

**Live:** [slimdragon007.github.io/pt-noshow-dashboard](https://slimdragon007.github.io/pt-noshow-dashboard)

## Features

- 5 KPI cards: total appointments, no-show rate, cancellation rate, attendance rate, estimated revenue lost
- Weekly trend line chart (no-shows, cancellations, attendance over time)
- No-show breakdown by day of week, time slot, therapist, appointment type, and insurance
- Reminder impact analysis (with vs. without reminders)
- Sortable, filterable appointment records table with pagination
- CSV upload: bring your own clinic data
- Global filters: date range, therapist, appointment type, insurance
- Fully responsive (mobile, tablet, desktop)

## CSV Format

Upload a CSV with these columns (flexible naming):

| Column | Accepted Names |
|--------|---------------|
| Date | `date`, `appointment_date` |
| Time | `time`, `appointment_time`, `time_slot` |
| Patient ID | `patient_id`, `patientId`, `patient` |
| Therapist | `therapist`, `provider`, `doctor` |
| Type | `appointment_type`, `type`, `visit_type` |
| Insurance | `insurance`, `insurance_type`, `payer` |
| Status | `status`, `appointment_status` |
| Reminder | `reminder_sent`, `reminder` |

Status values mapped automatically: "No Show", "Cancelled", "Late Cancel", "Attended/Completed/Kept".

## Stack

- React 19 + Vite 7
- Recharts (charts)
- PapaParse (CSV parsing)
- GitHub Pages (deployment)

## Development

```bash
npm install
npm run dev
```

## Deployment

Pushes to `main` auto-deploy via GitHub Actions to GitHub Pages.

---

Built by [FlowstateAI](https://michaelhaslim.github.io/ai-portfolio)
