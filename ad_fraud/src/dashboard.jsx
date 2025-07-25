import React from "react";


import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  PieChart, Pie, Cell,
  LineChart, Line,
} from 'recharts';

const barData = [
  { name: 'Mon', Clicks: 400, Impressions: 2400 },
  { name: 'Tue', Clicks: 300, Impressions: 2210 },
  { name: 'Wed', Clicks: 200, Impressions: 2290 },
  { name: 'Thu', Clicks: 278, Impressions: 2000 },
  { name: 'Fri', Clicks: 189, Impressions: 2181 },
  { name: 'Sat', Clicks: 239, Impressions: 2500 },
  { name: 'Sun', Clicks: 349, Impressions: 2100 },
];

const pieData = [
  { name: 'Human', value: 700 },
  { name: 'Bot', value: 300 },
];
const COLORS = ['#0088FE', '#FF8042'];

const lineData = [
  { name: '00:00', Fraud: 2 },
  { name: '04:00', Fraud: 5 },
  { name: '08:00', Fraud: 3 },
  { name: '12:00', Fraud: 8 },
  { name: '16:00', Fraud: 6 },
  { name: '20:00', Fraud: 4 },
];

export default function Dashboard() {
  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #f8fafc 0%, #e0e7ef 100%)',
      padding: '40px 0',
    }}>
      <div style={{
        maxWidth: 1100,
        margin: '0 auto',
        background: '#fff',
        borderRadius: 16,
        boxShadow: '0 4px 24px rgba(0,0,0,0.08)',
        padding: 32,
        position: 'relative',
      }}>
        <h2 style={{ textAlign: 'center', color: '#1a237e', marginBottom: 32 }}>
          📊 Ad Fraud Analytics Dashboard
        </h2>
        <a href="/" style={{
          position: 'absolute',
          top: 24,
          left: 32,
          textDecoration: 'none',
          color: '#1976d2',
          fontWeight: 500,
          background: '#e3f2fd',
          padding: '6px 16px',
          borderRadius: 6,
          fontSize: 15,
          boxShadow: '0 1px 4px rgba(0,0,0,0.04)'
        }}>&larr; Back to Home</a>
        <div style={{ display: 'flex', gap: 32, flexWrap: 'wrap', justifyContent: 'center' }}>
          <div>
            <h4 style={{ textAlign: 'center' }}>Weekly Clicks & Impressions</h4>
            <BarChart width={350} height={250} data={barData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="Clicks" fill="#1976d2" />
              <Bar dataKey="Impressions" fill="#82ca9d" />
            </BarChart>
          </div>
          <div>
            <h4 style={{ textAlign: 'center' }}>Traffic Source</h4>
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
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </div>
          <div>
            <h4 style={{ textAlign: 'center' }}>Fraudulent Clicks Over Time</h4>
            <LineChart width={350} height={250} data={lineData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="Fraud" stroke="#ff1744" strokeWidth={2} />
            </LineChart>
          </div>
        </div>
      </div>
    </div>
  );
}