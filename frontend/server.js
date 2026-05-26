import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { extname, join, normalize } from "node:path";

const port = Number(process.env.PORT || 4173);
const distDir = join(process.cwd(), "dist");

const contentTypes = {
  ".css": "text/css; charset=utf-8",
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".map": "application/json; charset=utf-8",
  ".png": "image/png",
  ".svg": "image/svg+xml",
  ".webp": "image/webp",
};

createServer(async (request, response) => {
  const requestedPath = new URL(request.url || "/", "http://localhost").pathname;
  const filePath = safeFilePath(requestedPath);
  const file = await readStaticFile(filePath);

  if (file) {
    response.writeHead(200, {
      "Content-Type": contentTypes[extname(filePath)] || "application/octet-stream",
      "Cache-Control": filePath.includes("/assets/") ? "public, max-age=31536000, immutable" : "no-cache",
    });
    response.end(file);
    return;
  }

  const indexFile = await readStaticFile(join(distDir, "index.html"));
  response.writeHead(indexFile ? 200 : 404, {
    "Content-Type": "text/html; charset=utf-8",
    "Cache-Control": "no-cache",
  });
  response.end(indexFile || "Not found");
}).listen(port, "0.0.0.0", () => {
  console.log(`frontend listening on 0.0.0.0:${port}`);
});

function safeFilePath(pathname) {
  const normalizedPath = normalize(decodeURIComponent(pathname)).replace(/^(\.\.[/\\])+/, "");
  const relativePath = normalizedPath === "/" ? "/index.html" : normalizedPath;
  return join(distDir, relativePath);
}

async function readStaticFile(filePath) {
  try {
    return await readFile(filePath);
  } catch {
    return null;
  }
}
