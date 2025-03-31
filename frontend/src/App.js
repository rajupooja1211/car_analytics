import { useState, useEffect } from "react";
import TaskForm from "./components/TaskForm";
import Charts from "./components/Charts";
import './App.css'; 

function App() {
  const [taskId, setTaskId] = useState(null);
  const [status, setStatus] = useState(null);
  const [analytics, setAnalytics] = useState(null);

  useEffect(() => {
    if (!taskId) return;

    const interval = setInterval(async () => {
      const res = await fetch(`http://localhost:5001/tasks/${taskId}`);
      const data = await res.json();
      setStatus(data.status);

      if (data.status === "completed") {
        clearInterval(interval);
        const analyticsRes = await fetch(`http://localhost:5001/analytics/${taskId}`);
        const analyticsData = await analyticsRes.json();
        setAnalytics(analyticsData);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [taskId]);

  return (
    <div style={{ padding: "2rem", fontFamily:"serif", textAlign:"center" }}>
      <h1>Car Sales Analytics</h1>
      <TaskForm onTaskCreated={setTaskId} />
      {taskId && <p><strong>Task ID:</strong> {taskId} — <strong>Status:</strong> {status}</p>}
      {analytics && <Charts analytics={analytics} />}
    </div>
  );
}

export default App;
