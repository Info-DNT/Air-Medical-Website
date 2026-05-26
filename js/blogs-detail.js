// Blogs & comments are fetched from window.blogsSupabaseClient configured in js/config.js
const supabaseClient = window.blogsSupabaseClient;

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
    titleEl.innerText = "Blogs not found";
    return;
  }

  if (slug === "air-ambulance-medical-evacuation-uae") {
    const localBlog = {
      title: "Air Ambulance & Medical Evacuation Services in UAE - Fast, Safe, and Trusted Medical Transport",
      featured_image: "img/air-ambulance-uae.jpg",
      content: `
<p class="lead">Medical emergencies do not give you time to think. A sudden cardiac event, a serious road accident, a health crisis while travelling — these situations need a response that is fast and medically sound. That is exactly what Air Ambulance & Medical Evacuation Services are built for. In the UAE, where patients may need to be moved quickly across emirates or airlifted internationally, having the right air medical partner already in mind is worth more than most people realise.</p>

<p>Whether in <strong>Dubai, Abu Dhabi, Sharjah, or Ras Al Khaimah</strong>, air ambulance services operate across the UAE to get patients to the right hospital before their condition gets worse.</p>

<h3 class="mt-4 text-primary">What Are Air Ambulance & Medical Evacuation Services?</h3>
<p>Air ambulance and medical evacuation services use medically equipped aircraft — fixed-wing planes or helicopters — to transport critically ill or injured patients to appropriate medical facilities, fast.</p>

<p>These services cover a wide range of critical care needs, including:</p>
<ul class="list-group list-group-flush mb-4">
    <li class="list-group-item bg-transparent border-0 ps-0"><i class="fas fa-check text-red me-2"></i><strong>Emergency evacuations</strong> from accident sites or remote areas.</li>
    <li class="list-group-item bg-transparent border-0 ps-0"><i class="fas fa-check text-red me-2"></i><strong>Inter-hospital transfers</strong> when patients require specialised care at tertiary centres.</li>
    <li class="list-group-item bg-transparent border-0 ps-0"><i class="fas fa-check text-red me-2"></i><strong>Repatriation flights</strong> to bring patients back home safely from abroad.</li>
    <li class="list-group-item bg-transparent border-0 ps-0"><i class="fas fa-check text-red me-2"></i><strong>Organ transport</strong> requiring absolute speed and logistics precision.</li>
    <li class="list-group-item bg-transparent border-0 ps-0"><i class="fas fa-check text-red me-2"></i><strong>Neonatal and pediatric transfers</strong> requiring specialised medical teams and incubators onboard.</li>
</ul>
<p>Each flight carries trained medical professionals — doctors, nurses, and paramedics — with ICU-level equipment to monitor and stabilise patients throughout the journey.</p>

<h3 class="mt-4 text-primary">Why Air Ambulance Services Are Critical in the UAE</h3>
<p>The UAE sees millions of expatriates, tourists, and business travellers every year. Medical emergencies do not care about timing or convenience — and road transport in a busy UAE city can cost precious minutes.</p>

<p>Here is why air ambulance services matter in the UAE:</p>
<div class="row g-4 my-3">
    <div class="col-md-6">
        <div class="premium-card h-100 p-4" style="background: #f8fafc; border: 1px solid rgba(0, 0, 0, 0.03); border-radius: 16px;">
            <h5 class="fw-bold text-dark"><i class="fas fa-bolt text-red me-2"></i>Speed</h5>
            <p class="mb-0 small text-muted">Air ambulances skip traffic entirely. Ground transport cannot compete in time-critical cases where every second counts.</p>
        </div>
    </div>
    <div class="col-md-6">
        <div class="premium-card h-100 p-4" style="background: #f8fafc; border: 1px solid rgba(0, 0, 0, 0.03); border-radius: 16px;">
            <h5 class="fw-bold text-dark"><i class="fas fa-globe-americas text-red me-2"></i>Long-Distance Coverage</h5>
            <p class="mb-0 small text-muted">The UAE is a global transfer hub. We connect patients headed to super-specialty hospitals in Europe, Asia, or the Americas.</p>
        </div>
    </div>
    <div class="col-md-6">
        <div class="premium-card h-100 p-4" style="background: #f8fafc; border: 1px solid rgba(0, 0, 0, 0.03); border-radius: 16px;">
            <h5 class="fw-bold text-dark"><i class="fas fa-heartbeat text-red me-2"></i>Advanced Onboard Care</h5>
            <p class="mb-0 small text-muted">Patients get hospital-level ICU treatment during the flight, including active monitoring, rather than basic stabilisation.</p>
        </div>
    </div>
    <div class="col-md-6">
        <div class="premium-card h-100 p-4" style="background: #f8fafc; border: 1px solid rgba(0, 0, 0, 0.03); border-radius: 16px;">
            <h5 class="fw-bold text-dark"><i class="fas fa-clock text-red me-2"></i>24/7 Availability</h5>
            <p class="mb-0 small text-muted">Medical emergencies happen at night, on weekends, and on holidays. Dedicated operations teams are on standby 24/7/365.</p>
        </div>
    </div>
</div>

<h3 class="mt-4 text-primary">How Air Medical 24X7 Delivers Trusted Medical Transport in UAE</h3>
<p>For Air Ambulance & Medical Evacuation Services in the UAE, Air Medical 24X7 is a provider worth knowing. Their team includes experienced flight doctors, nurses, and paramedics. Their aircraft are equipped for critical care, and they operate around the clock.</p>

<p>Their specialised services include:</p>
<ul>
    <li class="mb-2"><strong>Domestic Air Ambulance:</strong> Quick transfers across all UAE emirates (Dubai, Abu Dhabi, Sharjah, Ras Al Khaimah, Fujairah, Ajman, Umm Al Quwain).</li>
    <li class="mb-2"><strong>International Medical Evacuation:</strong> Safe transfers to and from the UAE globally.</li>
    <li class="mb-2"><strong>Bedside-to-Bedside Service:</strong> Full end-to-end coordination, including ground ambulance support at both ends.</li>
    <li class="mb-2"><strong>Critical Care Transfers:</strong> Fully configured ICU setups onboard advanced aircraft.</li>
    <li class="mb-2"><strong>Repatriation of Mortal Remains:</strong> Handled with utmost care, respect, and compliance with local regulations.</li>
</ul>

<h3 class="mt-4 text-primary">What to Expect During an Air Ambulance Flight</h3>
<p>Most families have never dealt with a medical evacuation before. Here is how the process works:</p>
<ol>
    <li class="mb-2"><strong>Initial Assessment</strong> — The medical team reviews the patient's condition and decides what transport setup is needed.</li>
    <li class="mb-2"><strong>Flight Planning</strong> — Route, aircraft type, and onboard equipment are confirmed based on patient requirements.</li>
    <li class="mb-2"><strong>Onboard Medical Care</strong> — Doctors and nurses manage vitals, medications, and any complications during the flight.</li>
    <li class="mb-2"><strong>Hospital Coordination</strong> — The receiving hospital is briefed ahead of arrival for immediate admission.</li>
    <li class="mb-2"><strong>Safe Handover</strong> — The patient is transferred directly to the destination medical team.</li>
</ol>
<p>The process is built around one goal: getting the patient to the right place in the right condition.</p>

<h3 class="mt-4 text-primary">Conclusion</h3>
<p>When time is short and the stakes are high, Air Ambulance & Medical Evacuation Services in the UAE give patients a real chance of getting the care they need. Whether the transfer is local or international, what matters is having a provider who responds fast, sends qualified medical staff, and gets the patient to the right hospital. Contact Air Medical 24X7 today — do not wait until an emergency to figure out your options.</p>
      `,
      meta_title: "Air Ambulance & Medical Evacuation Services in UAE | Air Medical 24X7",
      meta_description: "Emergency ICU air ambulance and medical evacuation services in the UAE. 24X7 bed-to-bed medical escort and patient repatriation. Call +971565542001.",
      excerpt: "Medical emergencies do not give you time to think. Discover how Air Ambulance & Medical Evacuation Services in the UAE provide fast, safe, and trusted critical care patient transfers.",
      views: 125,
      id: "uae-local-blog-id"
    };

    const sanitizedTitle = window.sanitize24X7(localBlog.title);
    titleEl.innerText = sanitizedTitle;
    imageEl.src = localBlog.featured_image;
    imageEl.alt = sanitizedTitle;
    contentEl.innerHTML = window.sanitize24X7(localBlog.content);
    document.title = window.sanitize24X7(localBlog.meta_title);
    document.querySelector('meta[name="description"]')?.setAttribute("content", window.sanitize24X7(localBlog.meta_description));
    
    currentBlogId = localBlog.id;
    const viewEl = document.getElementById("view-count");
    if (viewEl) viewEl.innerText = localBlog.views;

    loadComments(localBlog.id);
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
    titleEl.innerText = "Blogs not found";
    return;
  }

  const sanitizedTitle = window.sanitize24X7(data.title);
  titleEl.innerText = sanitizedTitle;

  imageEl.src = data.featured_image || "img/airmedicallogo.png";
  imageEl.alt = sanitizedTitle;

  contentEl.innerHTML = window.sanitize24X7(data.content);

  document.title = window.sanitize24X7(data.meta_title || data.title);
  document
    .querySelector('meta[name="description"]')
    ?.setAttribute(
      "content",
      window.sanitize24X7(data.meta_description || data.excerpt || "")
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

    const name = window.sanitize24X7(c.name);
    const message = window.sanitize24X7(c.message);
    const adminReply = window.sanitize24X7(c.admin_reply);

    div.innerHTML = `
      <div class="mb-1">
        <strong>${name}</strong>
        <small class="text-muted">
          • ${new Date(c.created_at).toDateString()}
        </small>
      </div>

      <div class="mb-2">
        ${message}
      </div>

      ${
        adminReply
          ? `
          <div style="
            margin-left: 15px;
            padding: 10px 12px;
            background: #f8f9fa;
            border-left: 3px solid #dc3545;
            font-size: 14px;
          ">
            <strong>Air Medical 24X7:</strong><br>
            ${adminReply}
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
         href="/blogs?category=${encodeURIComponent(category)}">
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

  // Prepend local UAE blog to recent posts list
  container.innerHTML += `
    <a class="d-block mb-2"
       href="/blogs-detail.html?slug=air-ambulance-medical-evacuation-uae">
      Air Ambulance & Medical Evacuation Services in UAE - Fast, Safe, and Trusted Medical Transport
    </a>
  `;

  data.forEach(post => {
    const title = window.sanitize24X7(post.title);
    container.innerHTML += `
      <a class="d-block mb-2"
         href="/blogs-detail.html?slug=${post.slug}">
        ${title}
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
      <a href="/blogs?tag=${encodeURIComponent(tag)}"
         class="btn btn-primary btn-sm m-1">
        ${tag}
      </a>
    `)
    .join("");
}
