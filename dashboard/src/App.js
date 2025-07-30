import React, { useEffect, useState } from "react";
import {
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

const COLORS = ["#0088FE", "#FF8042"];

export default function Dashboard() {
  const [sessions, setSessions] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/api/sessions")
      .then((res) => res.json())
      .then((data) => setSessions(data))
      .catch((err) => console.error("Failed to fetch sessions", err));
  }, []);

  // ---- Pie Data (count of Human vs Bot) ----
  const pieData = [
    {
      name: "Human",
      value: sessions.filter((s) => s.prediction === "Human").length,
    },
    {
      name: "Bot",
      value: sessions.filter((s) => s.prediction === "Bot").length,
    },
  ];

  // ---- Line Chart Data (group bots by hour) ----
  const botSessions = sessions.filter((s) => s.prediction === "Bot");
  const hourlyCounts = {};
  botSessions.forEach((s) => {
    const hour =
      new Date(s.timestamp).getHours().toString().padStart(2, "0") + ":00";
    hourlyCounts[hour] = (hourlyCounts[hour] || 0) + 1;
  });
  const lineData = Object.entries(hourlyCounts)
    .map(([hour, count]) => ({
      name: hour,
      Fraud: count,
    }))
    .sort((a, b) => a.name.localeCompare(b.name));

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "linear-gradient(135deg, #f8fafc 0%, #e0e7ef 100%)",
        padding: "40px 0",
      }}
    >
      <div
        style={{
          maxWidth: 1100,
          margin: "0 auto",
          background: "#fff",
          borderRadius: 16,
          boxShadow: "0 4px 24px rgba(0,0,0,0.08)",
          padding: 32,
          position: "relative",
        }}
      >
        <h2 style={{ textAlign: "center", color: "#1a237e", marginBottom: 32 }}>
          📊 Ad Fraud Analytics Dashboard
        </h2>
        <a
          href="/"
          style={{
            position: "absolute",
            top: 24,
            left: 32,
            textDecoration: "none",
            color: "#1976d2",
            fontWeight: 500,
            background: "#e3f2fd",
            padding: "6px 16px",
            borderRadius: 6,
            fontSize: 15,
            boxShadow: "0 1px 4px rgba(0,0,0,0.04)",
          }}
        >
          &larr; Back to Home
        </a>

        {/* Charts */}
        <div
          style={{
            display: "flex",
            gap: 32,
            flexWrap: "wrap",
            justifyContent: "center",
          }}
        >
          <div>
            <h4 style={{ textAlign: "center" }}>Traffic Source</h4>
            <PieChart width={250} height={250}>
              <Pie
                data={pieData}
                cx={120}
                cy={120}
                innerRadius={50}
                outerRadius={80}
                fill="#8884d8"
                paddingAngle={5}
                dataKey="value"
                label
              >
                {pieData.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={COLORS[index % COLORS.length]}
                  />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </div>
          <div>
            <h4 style={{ textAlign: "center" }}>Fraudulent Clicks Over Time</h4>
            <LineChart width={350} height={250} data={lineData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Legend />
              <Line
                type="monotone"
                dataKey="Fraud"
                stroke="#ff1744"
                strokeWidth={2}
              />
            </LineChart>
          </div>
        </div>

        {/* Logs Section */}
        <div style={{ marginTop: 48 }}>
          <h4 style={{ color: "#37474f" }}>📝 Latest Click Logs</h4>
          <div
            style={{
              maxHeight: 300,
              overflowY: "auto",
              border: "1px solid #ccc",
              borderRadius: 8,
              padding: 16,
              marginTop: 8,
              backgroundColor: "#fafafa",
            }}
          >
            {sessions.length === 0 ? (
              <p>Loading logs...</p>
            ) : (
              sessions.map((s, idx) => (
                <div
                  key={idx}
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    padding: "8px 0",
                    borderBottom: "1px solid #e0e0e0",
                    fontSize: 15,
                    color: s.prediction === "Bot" ? "#d32f2f" : "#388e3c",
                  }}
                >
                  <span>{new Date(s.timestamp).toLocaleString()}</span>
                  <span>{s.session_id}</span>
                  <strong>{s.prediction}</strong>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}