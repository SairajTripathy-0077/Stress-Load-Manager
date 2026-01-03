import { useState } from "react";
import { ingestData } from "../api";

export default function IngestForm({onIngest}) {
  const [type, setType] = useState("assignment");
  const [title, setTitle] = useState("");
  const [days, setDays] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    await ingestData({
      type,
      title,
      due_in_days: Number(days)
    });
    onIngest();
    setTitle("");
    setDays("");
  };

  return (
    <div>
      <h3>➕ Add Item</h3>
      <select value={type} onChange={e => setType(e.target.value)}>
        <option value="assignment">Assignment</option>
        <option value="exam">Exam</option>
        <option value="event">Event</option>
      </select>
      <input
        placeholder="Title"
        value={title}
        onChange={e => setTitle(e.target.value)}
      />
      <input
        placeholder="Due in days"
        type="number"
        value={days}
        onChange={e => setDays(e.target.value)}
      />
      <button onClick={submit}>Add</button>
    </div>
  );
}
