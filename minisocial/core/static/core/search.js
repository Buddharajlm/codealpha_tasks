const searchInput = document.getElementById("user-search");
const resultsEl = document.getElementById("search-results");
let searchTimer;

searchInput.addEventListener("input", () => {
  clearTimeout(searchTimer);
  const q = searchInput.value.trim();
  if (!q) {
    resultsEl.replaceChildren();
    return;
  }
  // wait 250ms after the last keystroke so we don't send a request per letter
  searchTimer = setTimeout(async () => {
    const res = await fetch(`/api/users/search/?q=${encodeURIComponent(q)}`);
    if (!res.ok) return;
    const data = await res.json();
    resultsEl.replaceChildren();
    if (data.users.length === 0) {
      resultsEl.textContent = "No users found.";
      return;
    }
    data.users.forEach((u) => {
      const a = document.createElement("a");
      a.className = "search-item";
      a.href = "/u/" + encodeURIComponent(u.username) + "/";
      a.textContent = "@" + u.username + (u.is_following ? "  ·  following" : "");
      resultsEl.append(a);
    });
  }, 250);
});