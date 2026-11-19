export const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? "")
  .trim()
  .replace(/\/+$/, "")
  .replace(/(?:\/api)+$/i, "");

export function apiUrl(path: string): string {
  const endpoint = path
    .trim()
    .replace(/\\/g, "/")
    .replace(/\/{2,}/g, "/")
    .replace(/^\/+|\/+$/g, "")
    .replace(/^(?:api\/?)+/i, "");
  return `${API_BASE_URL}/api${endpoint ? `/${endpoint}` : ""}`;
}

export async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(apiUrl(path));
  if (!response.ok) throw new Error(`API request failed: ${response.status}`);
  return response.json() as Promise<T>;
}
