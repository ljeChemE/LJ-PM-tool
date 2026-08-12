import { useEffect, useState, type FormEvent } from "react";
import { api, type Project, type Task, type TaskStatus } from "./api";

const STATUS_LABELS: Record<TaskStatus, string> = {
  todo: "To Do",
  in_progress: "In Progress",
  done: "Done",
};

function TodayView() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [title, setTitle] = useState("");
  const [projectId, setProjectId] = useState<number | "">("");
  const [deadline, setDeadline] = useState("");
  const [error, setError] = useState<string | null>(null);

  const projectsById = new Map(projects.map((p) => [p.id, p.name]));

  async function refreshTasks() {
    setTasks(await api.getTodaysTasks());
  }

  async function refreshProjects() {
    setProjects(await api.getProjects());
  }

  useEffect(() => {
    refreshProjects().catch((e: unknown) => setError(String(e)));
    refreshTasks().catch((e: unknown) => setError(String(e)));
  }, []);

  async function handleAddTask(e: FormEvent) {
    e.preventDefault();
    if (!title.trim() || projectId === "") return;
    try {
      await api.createTask({
        title: title.trim(),
        project_id: projectId,
        deadline: deadline || undefined,
      });
      setTitle("");
      setDeadline("");
      await refreshTasks();
    } catch (err: unknown) {
      setError(String(err));
    }
  }

  async function changeStatus(task: Task, status: TaskStatus) {
    try {
      await api.updateTask(task.id, { status });
      await refreshTasks();
    } catch (err: unknown) {
      setError(String(err));
    }
  }

  return (
    <>
      <h1>Today</h1>
      {error && <p className="error">{error}</p>}

      <form onSubmit={handleAddTask} className="inline-form">
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Task title"
          autoComplete="off"
        />
        <select
          value={projectId}
          onChange={(e) =>
            setProjectId(e.target.value ? Number(e.target.value) : "")
          }
        >
          <option value="">#project</option>
          {projects.map((p) => (
            <option key={p.id} value={p.id}>
              #{p.name}
            </option>
          ))}
        </select>
        <input
          type="date"
          value={deadline}
          onChange={(e) => setDeadline(e.target.value)}
        />
        <button type="submit">Add task</button>
      </form>

      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>Task</th>
            <th>Project</th>
            <th>Deadline</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {tasks.map((task) => (
            <tr
              key={task.id}
              className={task.status === "done" ? "done" : undefined}
            >
              <td>{task.id}</td>
              <td>
                {task.title}
                {task.carried_over_count > 0 && (
                  <span
                    className="carried-over"
                    title={`Carried over ${task.carried_over_count}x`}
                  >
                    {" "}
                    ↻{task.carried_over_count}
                  </span>
                )}
              </td>
              <td>#{projectsById.get(task.project_id) ?? "?"}</td>
              <td>{task.deadline}</td>
              <td>
                <select
                  value={task.status}
                  onChange={(e) =>
                    changeStatus(task, e.target.value as TaskStatus)
                  }
                >
                  {Object.entries(STATUS_LABELS).map(([value, label]) => (
                    <option key={value} value={value}>
                      {label}
                    </option>
                  ))}
                </select>
              </td>
            </tr>
          ))}
          {tasks.length === 0 && (
            <tr>
              <td colSpan={5}>Nothing on today&apos;s list.</td>
            </tr>
          )}
        </tbody>
      </table>
    </>
  );
}

export default TodayView;
