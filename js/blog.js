/***************** SUPABASE CONFIG *****************/
const supabaseUrl = "https://eiqpvuciihwmuznbsyob.supabase.co";
const supabaseKey =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVpcXB2dWNpaWh3bXV6bmJzeW9iIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU2MDY1MDcsImV4cCI6MjA4MTE4MjUwN30.fY2QZkNa1nUB1UQxmV8r97WTpB32ocIiVXaHo1coB-c";

const supabaseClient = supabase.createClient(supabaseUrl, supabaseKey);

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
      <div class="bg-light rounded overflow-hidden h-100">
        <img class="img-fluid w-100"
             src="${blog.featured_image || "img/airmedicallogo.png"}"
             alt="${blog.title}">
        <div class="p-4">
          <a class="h4 d-block mb-2"
             href="/blog-detail.html?slug=${blog.slug}">
            ${blog.title}
          </a>
          <p class="m-0">${blog.excerpt || ""}</p>
        </div>
        <div class="d-flex align-items-center border-top p-3">
          <img class="rounded-circle me-2"
               src="img/airmedicallogo.png"
               width="30" height="30">
          <small>
            ${blog.author || "Air Medical 24X7"} ·
            ${new Date(blog.created_at).toLocaleDateString()}
          </small>
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
