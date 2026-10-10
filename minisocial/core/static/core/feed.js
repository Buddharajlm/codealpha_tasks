const feedEl = document.getElementById("feed");
const postForm = document.getElementById("post-form");
const contentEl = document.getElementById("post-content");
const countEl = document.getElementById("char-count");

async function loadFeed() {
  const res = await fetch("/api/posts/");
  if (!res.ok) return;
  const data = await res.json();
  feedEl.replaceChildren();
  if (data.posts.length === 0) {
    feedEl.textContent = "No posts yet. Be the first!";
    return;
  }
  data.posts.forEach((p) => feedEl.append(renderPost(p)));
}

contentEl.addEventListener("input", () => {
  countEl.textContent = `${contentEl.value.length} / 280`;
});

postForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  showError("");
  const { ok, data } = await postJSON("/api/posts/", { content: contentEl.value });
  if (ok) {
    contentEl.value = "";
    countEl.textContent = "0 / 280";
    loadFeed();
  } else {
    showError(data.error || "Something went wrong.");
  }
});

loadFeed();