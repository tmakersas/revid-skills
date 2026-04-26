/**
 * Tiny shared client for the Revid Public API v3.
 * All TS examples in this folder import from here.
 */

const API = "https://www.revid.ai/api/public/v3";

function key(): string {
  const k = process.env.REVID_API_KEY;
  if (!k) throw new Error("REVID_API_KEY not set");
  return k;
}

export type RenderResponse =
  | { success: 1; pid: string; workflow: string; endpoint: string; docs?: unknown }
  | { success: 0; error: string };

export type StatusResponse = {
  pid: string;
  status: "queued" | "rendering" | "ready" | "failed";
  progress?: number;
  videoUrl?: string;
  thumbnailUrl?: string;
  durationSeconds?: number;
  creditsUsed?: number;
  error?: string;
};

export async function render(payload: unknown): Promise<string> {
  const res = await fetch(`${API}/render`, {
    method: "POST",
    headers: { "Content-Type": "application/json", key: key() },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status} from /render`);
  const body = (await res.json()) as RenderResponse;
  if (body.success !== 1) throw new Error(`render failed: ${body.error}`);
  return body.pid;
}

export async function waitFor(
  pid: string,
  opts: { timeoutMs?: number } = {},
): Promise<StatusResponse> {
  const timeoutMs = opts.timeoutMs ?? 600_000;
  const deadline = Date.now() + timeoutMs;
  let delayMs = 5000;
  while (Date.now() < deadline) {
    const res = await fetch(`${API}/status?pid=${encodeURIComponent(pid)}`, {
      headers: { key: key() },
    });
    if (!res.ok) throw new Error(`HTTP ${res.status} from /status`);
    const body = (await res.json()) as StatusResponse;
    process.stdout.write(`  pid=${pid} status=${body.status} progress=${body.progress ?? 0}\n`);
    if (body.status === "ready") return body;
    if (body.status === "failed") throw new Error(body.error ?? "render failed");
    await new Promise((r) => setTimeout(r, delayMs));
    if ((body.progress ?? 0) > 30) delayMs = 8000;
  }
  throw new Error(`pid ${pid} not ready after ${timeoutMs} ms`);
}

export async function estimateCredits(payload: unknown): Promise<unknown> {
  const res = await fetch(`${API}/calculate-credits`, {
    method: "POST",
    headers: { "Content-Type": "application/json", key: key() },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status} from /calculate-credits`);
  return res.json();
}
