import { useEffect, useState } from "react";
import { fetchAllData, deleteItem, updateItem } from "../api";

export default function LiveData({refreshKey}) {
  const [data, setData] = useState({
    assignments: [],
    exams: [],
    events: []
  });

  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState({ title: "", due_in_days: 0 });

  const loadData = async () => {
    const result = await fetchAllData();
    setData(result);
  };

  useEffect(() => {
    loadData();
  }, [refreshKey]);

  const startEdit = (category, index, item) => {
    setEditing({ category, index });
    setForm({
      title: item.title,
      due_in_days: item.due_in_days
    });
  };

  const cancelEdit = () => {
    setEditing(null);
  };

  const saveEdit = async () => {
    if (!editing) return;

    await updateItem(editing.category, editing.index, form);
    setEditing(null);
    await loadData(); // force sync from backend
  };
  const renderSection = (title, category, items) => (
    <div className="section">
      <h3>{title}</h3>

      {items.map((item, index) => {
        const isEditing =
          editing &&
          editing.category === category &&
          editing.index === index;

        return (
          <div className="card" key={index}>
            {isEditing ? (
              <div className="edit-box">
                <input
                  value={form.title}
                  onChange={(e) =>
                    setForm({ ...form, title: e.target.value })
                  }
                  placeholder="Title"
                />

                <input
                  type="number"
                  value={form.due_in_days}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      due_in_days: Number(e.target.value)
                    })
                  }
                />

                <div className="actions">
                  <button onClick={saveEdit}>Save</button>
                  <button onClick={cancelEdit}>Cancel</button>
                </div>
              </div>
            ) : (
              <>
                <div>
                  <strong>{item.title}</strong>
                  <p>Due in {item.due_in_days} days</p>
                </div>

                <div className="actions">
                  <button onClick={() => startEdit(category, index, item)}>
                    Edit
                  </button>
                  <button
                    className="delete"
                    onClick={async () => {
                      await deleteItem(category, index);
                      loadData();
                    }}
                  >
                    Delete
                  </button>
                </div>
              </>
            )}
          </div>
        );
      })}
    </div>
  );

  return (
    <div className="live-data">
      <h2>📊 Live Data Preview</h2>
      {renderSection("Assignments", "assignments", data.assignments)}
      {renderSection("Exams", "exams", data.exams)}
      {renderSection("Events", "events", data.events)}
    </div>
  );
}
