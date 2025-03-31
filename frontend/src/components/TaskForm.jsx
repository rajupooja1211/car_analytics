import { useState } from "react";
import './TaskForm.css';

export default function TaskForm({ onTaskCreated }) {
  const [startYear, setStartYear] = useState(2023);
  const [endYear, setEndYear] = useState(2025);
  const [companies, setCompanies] = useState("Toyota,Honda");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch("http://localhost:5001/tasks", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        filters: {
          start_year: Number(startYear),
          end_year: Number(endYear),
          companies: companies.split(",").map((c) => c.trim())
        }
      })
    });

    const data = await response.json();
    onTaskCreated(data.task_id);
  };

  return (
    <div className="task-form">
      <h2>Submit Task</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-row">
          <input
            type="number"
            value={startYear}
            onChange={(e) => setStartYear(e.target.value)}
            placeholder="Start Year"
          />
          <input
            type="number"
            value={endYear}
            onChange={(e) => setEndYear(e.target.value)}
            placeholder="End Year"
          />
          <input
            type="text"
            value={companies}
            onChange={(e) => setCompanies(e.target.value)}
            placeholder="Companies (comma-separated)"
          />
          <button type="submit">Submit</button>
        </div>
      </form>
    </div>
  );
  
}
