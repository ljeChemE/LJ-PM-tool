import { NavLink, Route, Routes } from "react-router-dom";
import "./App.css";
import DashboardView from "./DashboardView";
import ProjectPage from "./ProjectPage";
import TodayView from "./TodayView";

function App() {
  return (
    <main>
      <nav className="view-nav">
        <NavLink
          to="/"
          end
          className={({ isActive }) => (isActive ? "active" : undefined)}
        >
          Today
        </NavLink>
        <NavLink
          to="/dashboard"
          className={({ isActive }) => (isActive ? "active" : undefined)}
        >
          Dashboard
        </NavLink>
      </nav>

      <Routes>
        <Route path="/" element={<TodayView />} />
        <Route path="/dashboard" element={<DashboardView />} />
        <Route path="/projects/:projectId" element={<ProjectPage />} />
      </Routes>
    </main>
  );
}

export default App;
