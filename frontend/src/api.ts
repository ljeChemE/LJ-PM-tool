const API_URL = import.meta.env.VITE_API_URL as string;

export type ProjectStatus = "in_progress" | "completed";
export type TaskStatus = "todo" | "in_progress" | "done";

export type Project = {
  id: number;
  name: string;
  status: ProjectStatus;
};

export type Task = {
  id: number;
  title: string;
  project_id: number;
  deadline: string;
  status: TaskStatus;
  carried_over_count: number;
};

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) {
    throw new Error(
      `${options?.method ?? "GET"} ${path} failed: ${response.status}`,
    );
  }
  return response.json() as Promise<T>;
}

export const api = {
  getProjects: () => request<Project[]>("/projects"),
  getTasksForProject: (projectId: number) =>
    request<Task[]>(`/projects/${projectId}/tasks`),

  getTodaysTasks: () => request<Task[]>("/tasks/today"),
  createTask: (payload: {
    title: string;
    project_id: number;
    deadline?: string;
  }) =>
    request<Task>("/tasks", { method: "POST", body: JSON.stringify(payload) }),
  updateTask: (
    id: number,
    payload: Partial<Pick<Task, "status" | "deadline" | "title">>,
  ) =>
    request<Task>(`/tasks/${id}`, {
      method: "PATCH",
      body: JSON.stringify(payload),
    }),
};
