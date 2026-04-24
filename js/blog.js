// Supabase is now initialized in js/config.js as window.supabaseClient
const supabaseClient = window.supabaseClient;

/***************** STATE *****************/
const PAGE_SIZE = 3;
let page = 0;
let expanded = false;

/***************** DOM *****************/
const blogList = document.getElementById("blog-list");
const loadMoreBtn = document.getElementById("load-more");

/***************** LOAD BLOGS *****************/
async function loadBlogs(reset = false) {
  if (!blogList || !loadMoreBtn) return;

  if (reset) {
    blogList.innerHTML = "";
    page = 0;
    expanded = false;
    loadMoreBtn.innerText = "Load More";
  }

  const from = page * PAGE_SIZE;
  const to = from + PAGE_SIZE - 1;

  const { data, error } = await supabaseClient
    .from("blogs")
    .select("*")
    .eq("status", "published")
    .order("created_at", { ascending: false })
    .range(from, to);

  if (error) {
    console.error("Supabase error:", error.message);
    return;
  }

  if (!data || data.length === 0) {
    loadMoreBtn.style.display = "none";
    return;
  }

  data.forEach(blog => {
    const blogCard = document.createElement("div");
    blogCard.className = "col-xl-4 col-lg-6";

    blogCard.innerHTML = `
      <div class="premium-card p-0 overflow-hidden h-100">
        <a href="blog-detail.html?slug=${blog.slug}" class="d-block">
          <img class="img-fluid w-100"
               src="${blog.featured_image || "img/airmedicallogo.png"}"
               alt="${blog.title}" style="height: 220px; object-fit: cover;">
        </a>
        <div class="p-4">
          <a class="h4 d-block mb-3 text-dark fw-bold"
             href="blog-detail.html?slug=${blog.slug}" style="text-decoration: none; line-height: 1.4;">
            ${blog.title}
          </a>
          <p class="m-0 text-muted" style="font-size: 14px; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden;">
            ${blog.excerpt || ""}
          </p>
        </div>
        <div class="mt-auto border-top p-4">
          <small class="text-primary fw-bold"><i class="far fa-user me-2"></i>${blog.author || "Air Medical 24X7"}</small>
        </div>
      </div>
    `;

    blogList.appendChild(blogCard);
  });

  // Toggle button text
  if (!expanded && data.length === PAGE_SIZE) {
    loadMoreBtn.style.display = "inline-block";
  } else {
    loadMoreBtn.style.display = "none";
  }
}

/***************** BUTTON CLICK *****************/
loadMoreBtn.addEventListener("click", () => {
  if (!expanded) {
    expanded = true;
    page++;
    loadBlogs();
    loadMoreBtn.innerText = "Show Less";
  } else {
    loadBlogs(true);
  }
});

/***************** INIT *****************/
document.addEventListener("DOMContentLoaded", () => {
  loadBlogs(true);
});
