const profileUsername = document.body.dataset.profile;
const bioEl = document.getElementById("bio");
const bioForm = document.getElementById("bio-form");
const bioInput = document.getElementById("bio-input");
const bioCount = document.getElementById("bio-count");
const editBtn = document.getElementById("edit-bio-btn");
const postsEl = document.getElementById("profile-posts");
let postsCount = 0;

const followBtn = document.getElementById("follow-btn");

function setFollowButton(isFollowing) {
  followBtn.textContent = isFollowing ? "Following ✓" : "Follow";
  followBtn.classList.toggle("following", isFollowing);
}

function updatePostsCount(delta) {
  postsCount += delta;
  document.getElementById("posts-count").textContent = postsCount;
  if (postsCount === 0) postsEl.textContent = "No posts yet.";
}

function showBio(text) {
  bioEl.textContent = text || "No bio yet.";
  bioEl.classList.toggle("empty", !text);
}

async function loadProfile() {
  const res = await fetch(`/api/users/${encodeURIComponent(profileUsername)}/`);
  if (!res.ok) {
    document.getElementById("profile-name").textContent = "User not found";
    return;
  }
  const p = await res.json();

  document.getElementById("avatar").textContent = p.username[0].toUpperCase();
  document.getElementById("profile-name").textContent = "@" + p.username;
  document.getElementById("joined").textContent =
    "Joined " + new Date(p.joined).toLocaleDateString();
  document.getElementById("followers-count").textContent = p.followers_count;
  document.getElementById("following-count").textContent = p.following_count;
  showBio(p.bio);
  bioInput.value = p.bio;

    if (p.is_me) {
    editBtn.hidden = false;
  } else {
    followBtn.hidden = false;
    setFollowButton(p.is_following);
  }

  postsCount = p.posts_count;
  document.getElementById("posts-count").textContent = postsCount;
  postsEl.replaceChildren();
  if (p.posts.length === 0) postsEl.textContent = "No posts yet.";
  p.posts.forEach((post) => postsEl.append(renderPost(post, () => updatePostsCount(-1))));
}

editBtn.addEventListener("click", () => {
  bioForm.hidden = false;
  editBtn.hidden = true;
  bioEl.hidden = true;
  bioCount.textContent = `${bioInput.value.length} / 160`;
  bioInput.focus();
});

document.getElementById("bio-cancel").addEventListener("click", () => {
  bioForm.hidden = true;
  editBtn.hidden = false;
  bioEl.hidden = false;
  showError("");
});

bioInput.addEventListener("input", () => {
  bioCount.textContent = `${bioInput.value.length} / 160`;
});

bioForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  showError("");
  const res = await fetch("/api/users/me/", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({ bio: bioInput.value }),
  });
  const data = await res.json().catch(() => ({}));
  if (res.ok) {
    showBio(data.bio);
    bioForm.hidden = true;
    editBtn.hidden = false;
    bioEl.hidden = false;
  } else {
    showError(data.error || "Could not save bio.");
  }
});

followBtn.addEventListener("click", async () => {
  showError("");
  const { ok, data } = await postJSON(
    `/api/users/${encodeURIComponent(profileUsername)}/follow/`
  );
  if (ok) {
    setFollowButton(data.following);
    document.getElementById("followers-count").textContent = data.followers_count;
  } else {
    showError(data.error || "Could not update follow.");
  }
});

loadProfile();