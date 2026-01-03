import IngestForm from "./components/IngestForm";
import AskAI from "./components/AskAi.jsx";
import { useState } from "react";
import LiveData from "./components/LiveData.jsx";

export default function App() {
  const [refreshKey, setRefreshKey] = useState(0);

  function refresh() {
    setRefreshKey(k => k + 1);
  }
  return (
    <div style={{ padding: 20 }}>
      <h2>Stress Load Manager</h2>
      <IngestForm onIngest= {refreshKey} />
      <LiveData refreshKey={refreshKey} />
      <hr />
      <AskAI />
    </div>
  );
}
