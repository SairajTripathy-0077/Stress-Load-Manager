export default function WorkloadCard({ facts }) {
  if (!facts) return null;

  return (
    <div style={{ border: "1px solid #ccc", padding: 12 }}>
      <h3>📊 Workload Summary</h3>
      <p>Assignments: {facts.assignments}</p>
      <p>Exams: {facts.exams}</p>
      <p>Events: {facts.events}</p>
      <p>Stress Level: {facts.stress_level}</p>
      <p>Workload Score: {facts.workload_score}</p>
    </div>
  );
}
