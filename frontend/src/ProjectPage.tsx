import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api, type Project, type Task, type TaskStatus } from "./api";

const COLUMNS: { status: TaskStatus; label: string }[] = [
  { status: "todo", label: "To Do" },
  { status: "in_progress", label: "In Progress" },
  { status: "done", label: "Done" },
];

function ProjectPage() {
  const { projectId } = useParams<{ projectId: string }>();
  const id = Number(projectId);

  const [project, setProject] = useState<Project | null>(null);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [error, setError] = useState<string | null>(null);

  async function refresh() {
    const [projects, projectTasks] = await Promise.all([
      api.getProjects(),
      api.getTasksForProject(id),
    ]);
    setProject(projects.find((p) => p.id === id) ?? null);
    setTasks(projectTasks);
  }

  // Only re-run when `id` changes, not on every render — `refresh` is
  // redefined each render, so including it in the deps below would loop.
  // (oxlint's exhaustive-deps warning on this line is a known false
  // positive for this pattern; harmless, doesn't fail `just lint`.)
  useEffect(() => {
    refresh().catch((e: unknown) => setError(String(e)));
  }, [id]);

  async function handleStatusChange(task: Task, status: TaskStatus) {
    try {
      await api.updateTask(task.id, { status });
      await refresh();
    } catch (err: unknown) {
      setError(String(err));
    }
  }

  return (
    <>
      <Link to="/dashboard" className="back-link">
        ← Dashboard
      </Link>
      <h1>#{project?.name ?? "…"}</h1>
      {project && (
        <p className="project-status">{project.status.replace("_", " ")}</p>
      )}
      {error && <p className="error">{error}</p>}

      <div className="kanban-columns">
        {COLUMNS.map((column) => (
          <div key={column.status} className="kanban-column">
            <h4>{column.label}</h4>
            {tasks
              .filter((task) => task.status === column.status)
              .map((task) => (
                <div key={task.id} className="kanban-card">
                  <p>{task.title}</p>
                  <select
                    value={task.status}
                    onChange={(e) =>
                      handleStatusChange(task, e.target.value as TaskStatus)
                    }
                  >
                    {COLUMNS.map((c) => (
                      <option key={c.status} value={c.status}>
                        {c.label}
                      </option>
                    ))}
                  </select>
                </div>
              ))}
          </div>
        ))}
      </div>
    </>
  );
}

export default ProjectPage;
