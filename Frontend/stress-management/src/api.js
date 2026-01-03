const BASE_URL = "http://127.0.0.1:8000";

export async function ingestData(payload) {
  const res = await fetch(`${BASE_URL}/ingest`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  return res.json();
}

export async function askAI(question) {
  const res = await fetch(`${BASE_URL}/query/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question })
  });
  return res.json();
}

export async function fetchAllData() {
  const res = await fetch(`${BASE_URL}/data/all`);
  return res.json();
}

export async function deleteItem(category, index) {
  const res = await fetch(`${BASE_URL}/data/delete`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      category,
      index
    })
  });

  return res.json();
}

export async function updateItem(category, index, updatedData) {
  const res = await fetch("http://127.0.0.1:8000/data/update", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      category,
      index,
      title: updatedData.title,
      due_in_days: updatedData.due_in_days
    })
  });

  return res.json();
}
