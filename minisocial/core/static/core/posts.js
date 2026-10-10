async function deletePost(id, element, onDeleted) {
  const res = await fetch(`/api/posts/${id}/`, {
    method: "DELETE",
    headers: { "X-CSRFToken": getCookie("csrftoken") },
  });
  if (res.ok) {
    element.remove();
    if (onDeleted) onDeleted();
  } else {
    showError("Could not delete that post.");
  }
}

function renderComment(comment, onCountChange) {
  const div = document.createElement("div");
  div.className = "comment";

  const author = document.createElement("a");
  author.className = "author";
  author.href = "/u/" + encodeURIComponent(comment.author) + "/";
  author.textContent = "@" + comment.author;

  const text = document.createElement("span");
  text.textContent = " " + comment.content;

  div.append(author, text);

  if (comment.is_mine) {
    const del = document.createElement("button");
    del.className = "link-btn";
    del.textContent = "Delete";
    del.addEventListener("click", async () => {
      const res = await fetch(`/api/comments/${comment.id}/`, {
        method: "DELETE",
        headers: { "X-CSRFToken": getCookie("csrftoken") },
      });
      if (res.ok) {
        const data = await res.json();
        div.remove();
        onCountChange(data.comment_count);
      } else {
        showError("Could not delete that comment.");
      }
    });
    div.append(del);
  }
  return div;
}

function renderPost(post, onDeleted) {
  const article = document.createElement("article");
  article.className = "post";
  article.dataset.id = post.id;

  // --- header ---
  const header = document.createElement("div");
  header.className = "post-header";

  const author = document.createElement("a");
  author.className = "author";
  author.href = "/u/" + encodeURIComponent(post.author) + "/";
  author.textContent = "@" + post.author;

  const time = document.createElement("span");
  time.className = "time";
  time.textContent = new Date(post.created_at).toLocaleString();

  header.append(author, time);

  // --- body ---
  const body = document.createElement("p");
  body.textContent = post.content;

  // --- action buttons: like, comments, delete ---
  const actions = document.createElement("div");
  actions.className = "post-actions";

  const likeBtn = document.createElement("button");
  likeBtn.className = "action-btn";
  function paintLike() {
    likeBtn.textContent = (post.liked_by_me ? "♥ " : "♡ ") + post.like_count;
    likeBtn.classList.toggle("liked", post.liked_by_me);
  }
  paintLike();
  likeBtn.addEventListener("click", async () => {
    const { ok, data } = await postJSON(`/api/posts/${post.id}/like/`);
    if (ok) {
      post.liked_by_me = data.liked;
      post.like_count = data.like_count;
      paintLike();
    }
  });

  const commentBtn = document.createElement("button");
  commentBtn.className = "action-btn";
  function paintCommentCount() {
    commentBtn.textContent = "💬 " + post.comment_count;
  }
  paintCommentCount();

  actions.append(likeBtn, commentBtn);

  if (post.is_mine) {
    const del = document.createElement("button");
    del.className = "link-btn";
    del.textContent = "Delete";
    del.addEventListener("click", () => deletePost(post.id, article, onDeleted));
    actions.append(del);
  }

  // --- comments section (hidden until you click the 💬 button) ---
  const section = document.createElement("div");
  section.className = "comments";
  section.hidden = true;

  const list = document.createElement("div");

  const form = document.createElement("form");
  form.className = "comment-form";
  const input = document.createElement("input");
  input.maxLength = 280;
  input.placeholder = "Write a comment...";
  const send = document.createElement("button");
  send.type = "submit";
  send.className = "small";
  send.textContent = "Send";
  form.append(input, send);

  section.append(list, form);

  function onCountChange(n) {
    post.comment_count = n;
    paintCommentCount();
  }

  let loaded = false;
  async function loadComments() {
    const res = await fetch(`/api/posts/${post.id}/comments/`);
    if (!res.ok) return;
    const data = await res.json();
    list.replaceChildren();
    data.comments.forEach((c) => list.append(renderComment(c, onCountChange)));
  }

  commentBtn.addEventListener("click", () => {
    section.hidden = !section.hidden;
    if (!section.hidden && !loaded) {
      loaded = true;
      loadComments();
    }
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;
    const { ok, data } = await postJSON(`/api/posts/${post.id}/comments/`, { content: text });
    if (ok) {
      input.value = "";
      onCountChange(data.comment_count);
      if (loaded) list.append(renderComment(data, onCountChange));
      else {
        loaded = true;
        loadComments();
      }
    } else {
      showError(data.error || "Could not add comment.");
    }
  });

  article.append(header, body, actions, section);
  return article;
}