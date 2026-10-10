function getCookie(name) {
  const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
  return match ? decodeURIComponent(match[2]) : null;
}

async function postJSON(url, body = {}) {
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify(body),
  });
  const data = await res.json().catch(() => ({}));
  return { ok: res.ok, data };
}

function showError(message) {
  const el = document.getElementById("error");
  if (el) el.textContent = message;
}

const registerForm = document.getElementById("register-form");
if (registerForm) {
  registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const { ok, data } = await postJSON("/api/register/", {
      username: document.getElementById("username").value,
      email: document.getElementById("email").value,
      password: document.getElementById("password").value,
    });
    if (ok) window.location.href = "/";
    else showError(data.error || "Something went wrong.");
  });
}

const loginForm = document.getElementById("login-form");
if (loginForm) {
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const { ok, data } = await postJSON("/api/login/", {
      username: document.getElementById("username").value,
      password: document.getElementById("password").value,
    });
    if (ok) window.location.href = "/";
    else showError(data.error || "Something went wrong.");
  });
}

const logoutBtn = document.getElementById("logout-btn");
if (logoutBtn) {
  logoutBtn.addEventListener("click", async () => {
    await postJSON("/api/logout/");
    window.location.href = "/login/";
  });
}