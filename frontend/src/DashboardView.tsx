import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api, type Project, type Task } from "./api";

const STATUS_DOT: Record<Task["status"], string> = {
  todo: "○",
  in_progress: "◐",
  done: "●",
};

function ProjectColumn({
  project,
  tasks,
}: {
  project: Project;
  tasks: Task[];
}) {
  return (
    <Link to={`/projects/${project.id}`} className="project-column">
      <h3>#{project.name}</h3>
      <ul className="project-preview-list">
        {tasks.map((task) => (
          <li
            key={task.id}
            className={task.status === "done" ? "done" : undefined}
          >
            <span className="status-dot">{STATUS_DOT[task.status]}</span>{" "}
            {task.title}
          </li>
        ))}
        {tasks.length === 0 && <li className="empty">Nothing yet</li>}
      </ul>
    </Link>
  );
}

function DashboardView() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [tasksByProject, setTasksByProject] = useState<Record<number, Task[]>>(
    {},
  );
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      const fetchedProjects = await api.getProjects();
      setProjects(fetchedProjects);
      const entries = await Promise.all(
        fetchedProjects.map(
          async (p) => [p.id, await api.getTasksForProject(p.id)] as const,
        ),
      );
      setTasksByProject(Object.fromEntries(entries));
    }
    load().catch((e: unknown) => setError(String(e)));
  }, []);

  const active = projects.filter((p) => p.status === "in_progress");
  const completed = projects.filter((p) => p.status === "completed");

  return (
    <>
      <h1>Dashboard</h1>
      {error && <p className="error">{error}</p>}

      <h2>Active projects</h2>
      <div className="project-row">
        {active.map((project) => (
          <ProjectColumn
            key={project.id}
            project={project}
            tasks={tasksByProject[project.id] ?? []}
          />
        ))}
      </div>

      <h2>Completed projects</h2>
      <div className="project-row completed">
        {completed.map((project) => (
          <ProjectColumn
            key={project.id}
            project={project}
            tasks={tasksByProject[project.id] ?? []}
          />
        ))}
      </div>
    </>
  );
}

export default DashboardView;
