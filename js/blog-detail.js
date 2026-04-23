// Supabase is now initialized in js/config.js as window.supabaseClient
const supabaseClient = window.supabaseClient;

/***************** GLOBAL STATE *****************/
let currentBlogId = null;

/***************** URL PARAM *****************/
const params = new URLSearchParams(window.location.search);
const slug = params.get("slug");

/***************** DOM *****************/
const titleEl = document.getElementById("blog-title");
const imageEl = document.getElementById("blog-image");
const contentEl = document.getElementById("blog-content");

/***************** INIT *****************/
document.addEventListener("DOMContentLoaded", () => {
  loadBlog();
  loadCategories();
  loadRecentPosts();
  loadTags();
});

/***************** BLOG LOAD *****************/
async function loadBlog() {
  if (!slug) {
    titleEl.innerText = "Blog not found";
    return;
  }

  const { data, error } = await supabaseClient
    .from("blogs")
    .select("*")
    .eq("slug", slug)
    .eq("status", "published")
    .single();

  if (error || !data) {
    console.error(error);
    titleEl.innerText = "Blog not found";
    return;
  }

  titleEl.innerText = data.title;

  imageEl.src = data.featured_image || "img/airmedicallogo.png";
  imageEl.alt = data.title;

  contentEl.innerHTML = data.content;

  document.title = data.meta_title || data.title;
  document
    .querySelector('meta[name="description"]')
    ?.setAttribute(
      "content",
      data.meta_description || data.excerpt || ""
    );

  currentBlogId = data.id;

  updateViews(data.id, data.views || 0);
  loadComments(data.id);
}

/***************** VIEWS *****************/
async function updateViews(blogId, currentViews) {
  const newViews = currentViews + 1;

  await supabaseClient
    .from("blogs")
    .update({ views: newViews })
    .eq("id", blogId);

  const viewEl = document.getElementById("view-count");
  if (viewEl) viewEl.innerText = newViews;
}

/***************** COMMENTS + AIR MEDICAL 24X7 REPLY *****************/
async function loadComments(blogId) {
  const { data, error } = await supabaseClient
    .from("comments")
    .select("name, message, admin_reply, created_at")
    .eq("blog_id", blogId)
    .eq("status", "approved")
    .order("created_at", { ascending: false });

  if (error) {
    console.error(error);
    return;
  }

  const list = document.getElementById("comment-list");
  const heading = document.getElementById("comment-heading");
  const countEl = document.getElementById("comment-count");

  list.innerHTML = "";
  heading.innerText = `${data.length} Comments`;
  if (countEl) countEl.innerText = data.length;

  data.forEach(c => {
    const div = document.createElement("div");
    div.className = "mb-4";

    div.innerHTML = `
      <div class="mb-1">
        <strong>${c.name}</strong>
        <small class="text-muted">
          • ${new Date(c.created_at).toDateString()}
        </small>
      </div>

      <div class="mb-2">
        ${c.message}
      </div>

      ${
        c.admin_reply
          ? `
          <div style="
            margin-left: 15px;
            padding: 10px 12px;
            background: #f8f9fa;
            border-left: 3px solid #dc3545;
            font-size: 14px;
          ">
            <strong>Air Medical 24X7:</strong><br>
            ${c.admin_reply}
          </div>
        `
          : ""
      }
    `;

    list.appendChild(div);
  });
}

/***************** COMMENT SUBMIT *****************/
document
  .getElementById("comment-form")
  ?.addEventListener("submit", async (e) => {
    e.preventDefault();

    if (!currentBlogId) {
      alert("Blog not loaded");
      return;
    }

    const name = document.getElementById("comment-name").value.trim();
    const email = document.getElementById("comment-email").value.trim();
    const website = document.getElementById("comment-website").value.trim();
    const message = document.getElementById("comment-message").value.trim();

    if (!name || !message) {
      alert("Name and comment are required");
      return;
    }

    const { error } = await supabaseClient
      .from("comments")
      .insert({
        blog_id: currentBlogId,
        name,
        email,
        website,
        message,
        status: "pending"
      });

    if (error) {
      alert(error.message);
      return;
    }

    alert("Comment submitted for approval 🚀");
    e.target.reset();
  });

/***************** CATEGORIES *****************/
async function loadCategories() {
  const { data } = await supabaseClient
    .from("blogs")
    .select("category")
    .eq("status", "published");

  const container = document.getElementById("category-list");
  if (!container) return;

  container.innerHTML = "";

  [...new Set(data.map(b => b.category))].forEach(category => {
    container.innerHTML += `
      <a class="d-block mb-2"
         href="/blog?category=${encodeURIComponent(category)}">
        ${category}
      </a>
    `;
  });
}

/***************** RECENT POSTS *****************/
async function loadRecentPosts() {
  const { data } = await supabaseClient
    .from("blogs")
    .select("title, slug")
    .eq("status", "published")
    .order("created_at", { ascending: false })
    .limit(5);

  const container = document.getElementById("recent-posts");
  if (!container) return;

  container.innerHTML = "";

  data.forEach(post => {
    container.innerHTML += `
      <a class="d-block mb-2"
         href="/blog-detail.html?slug=${post.slug}">
        ${post.title}
      </a>
    `;
  });
}

/***************** TAG CLOUD *****************/
async function loadTags() {
  const { data } = await supabaseClient
    .from("blogs")
    .select("tags")
    .eq("status", "published");

  const container = document.getElementById("tag-cloud");
  if (!container) return;

  const tags = [...new Set(data.flatMap(b => b.tags || []))];

  container.innerHTML = tags
    .map(tag => `
      <a href="/blog?tag=${encodeURIComponent(tag)}"
         class="btn btn-primary btn-sm m-1">
        ${tag}
      </a>
    `)
    .join("");
}
