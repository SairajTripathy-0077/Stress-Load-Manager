import { useState } from "react";
import { askAI } from "../api";
import WorkloadCard from "./WorkLoadCard";

export default function AskAI() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState(null);

  const submit = async () => {
    const res = await askAI(question);
    setResponse(res);
  };

  return (
    <div>
      <h3>🤖 Ask AI</h3>
      <input
        placeholder="Ask about your workload"
        value={question}
        onChange={e => setQuestion(e.target.value)}
      />
      <button onClick={submit}>Ask</button>


      {response && (
        <>
          <WorkloadCard facts={response.facts} />

          <h3>🧠 AI Advice</h3>
          <div style={{ whiteSpace: "pre-wrap", lineHeight: 1.6 }}>
            {response.answer}
          </div>
        </>
      )}
    </div>
  );
}
