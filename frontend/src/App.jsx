import { useEffect, useState } from "react";
import Chat from "./components/Chat";

import "./styles/global.css";
import "./styles/dashboard.css";

export default function App() {
  const [theme, setTheme] = useState("dark");
  const [collapsed, setCollapsed] = useState(true);

  useEffect(() => {
    document.body.setAttribute("data-theme", theme);
  }, [theme]);

  return (
    <div className="app-layout">
      {/* SIDEBAR */}
      <aside className={`sidebar ${collapsed ? "collapsed" : ""}`}>
        {/* Sidebar header with toggle */}
        <div className="sidebar-header">
          {!collapsed && <h3>📊 Activity</h3>}

         <button
  className={`collapse-btn ${!collapsed ? "expanded" : ""}`}
  onClick={() => setCollapsed(!collapsed)}
  aria-label="Toggle sidebar"
>
  <span />
  <span />
  <span />
</button>
        </div>

        {!collapsed && (
          <>
            <div className="sidebar-section">
              <p className="sidebar-title">Recent Actions</p>
              <ul>
                <li> Dataset uploaded</li>
                <li> Asked: Business overview</li>
                <li> Viewed demand trend</li>
              </ul>
            </div>

            <div className="sidebar-section">
              <p className="sidebar-title">Suggested</p>
              <ul>
                <li>Should I increase inventory?</li>
                <li>Explain decision simply</li>
              </ul>
            </div>
          </>
        )}
      </aside>

      {/* MAIN DASHBOARD */}
      <main className="dashboard">
        <div className="header">
          <div>
            <h1>Agentic Data Analysis Assistant</h1>
            <p>Chat with your data using Data Analysis Agents</p>
          </div>

          <button
            className="theme-toggle"
            onClick={() =>
              setTheme(theme === "dark" ? "light" : "dark")
            }
          >
            {theme === "dark" ? "☀️ Light Mode" : "🌙 Dark Mode"}
          </button>
        </div>

        <Chat />
      </main>
    </div>
  );
}