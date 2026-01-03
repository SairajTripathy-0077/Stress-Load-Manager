import IngestForm from "./components/IngestForm";
import AskAI from "./components/AskAi.jsx";
import { useState } from "react";
import LiveData from "./components/LiveData.jsx";

import "./styles/app.css";
import "./styles/card.css";
import "./styles/form.css";

export default function App() {
  const [refreshKey, setRefreshKey] = useState(0);

  function refresh() {
    setRefreshKey(k => k + 1);
  }
  return (
    <div className="app">
      <h1>Stress Load Manager</h1>

      <div className="card">
        <div className="card-title">Add Workload</div>
        <IngestForm onIngest= {refresh} />
      </div>

      <div className="card">
        <div className="card-title">Live Workload Data</div>
        <LiveData refreshKey={refreshKey} />
      </div>

      <hr />

      <div className="card">
        <div className="card-title">AI Planner</div>
        <AskAI />
      </div>
    </div>
  );
}
