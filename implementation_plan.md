# Air Medical 24X7 — Full Website Audit & Restructuring Plan

## 1. Project Overview

| Metric | Value |
|---|---|
| Total HTML pages | **49** |
| Country pages | **30** (all in root) |
| Service pages | **11** (all in root) |
| Core pages | **8** (index, about, contact, country, blog, blog-detail, privacy, terms) |
| CSS files | 2 (`bootstrap.min.css` + `style.css`) |
| JS files | 3 (`main.js`, `blog.js`, `blog-detail.js`) |
| Libraries | Owl Carousel, jQuery 3.4, Bootstrap 5, Tempus Dominus, Waypoints, Easing |
| Backend | Supabase (appointments, blogs, comments tables) |
| Analytics | GTM + Google Ads conversion tracking (inconsistent) |
| Images | 57 files in `/img` |

---

## 2. Design System Analysis

### Color Palette (CSS `:root`)
```css
--primary: #1A346B;    /* Deep navy blue — used everywhere */
--secondary: #354F8E;  /* Medium blue — footer accents */
--light: #EFF5F9;      /* Ice blue background */
--dark: #1D2A4D;       /* Near-black navy */
```
**Additional hardcoded colors:**
- `#FB0F0C` — Red (SOS button, topbar background, email SOS link)
- `#25D366` — WhatsApp green (center button, mobile icon)
- `#008cff` / `#038eff` — Blue (call buttons)
- `#00ff5e` — Bright green (SOS WhatsApp link)
- `#f1f8ff` — Light blue (contact boxes, transport cards)

### Typography
- **Primary font**: `Roboto` (400, 700) — loaded from Google Fonts
- **Secondary font**: `Roboto Condensed` (400, 700)
- **Navbar font**: `Jost` (referenced in CSS but NOT loaded in `<head>`)
- **Font weights**: 500 (topbar), 600 (transport cards, WhatsApp btn), 700 (buttons, headings)

### Animations & Interactions
| Animation | Where Used |
|---|---|
| Navbar underline slide (`width: 0 → 100%`) | Desktop nav links on hover |
| Service card button reveal (`opacity: 0 → 1`) | Service items on hover |
| Country card lift (`translateY(-6px)`) | Country grid cards on hover |
| Social proof slide-in (`slideInLeft` keyframe) | Bottom-left notification popup |
| Back-to-top fade (`fadeIn/fadeOut`) | Scroll-triggered button |
| Box shadow on hover | All `.btn` elements |
| `0.3s – 0.5s` transitions | Most interactive elements |

### Layout System
- **Bootstrap 5** grid (`container`, `row`, `col-lg-*`)
- **Sticky navbar** with shadow
- **Hero**: Full-width with background image (`herorr.png`)
- **Mobile**: Hero text hidden, hero shrunk to 220px
- **Footer**: 4-column grid → stacks on mobile

---

## 3. Current File Structure (Flat)

```
root/
├── index.html                                    ← Homepage
├── about.html                                    ← About page
├── contact.html                                  ← Contact page
├── country.html                                  ← Country listing page
├── blog.html                                     ← Blog listing
├── blog-detail046d.html                          ← Blog detail
├── privacy-policy.html                           ← Legal
├── terms-and-conditions.html                     ← Legal
│
├── air-ambulance.html                            ← SERVICE
├── air-ambulance-charters.html                   ← SERVICE
├── commercial-airlines-medical-transfer-services.html ← SERVICE
├── commercial-flight-stretcher.html              ← SERVICE
├── ECMO-transfer.html                            ← SERVICE
├── flight-medical-escort-service.html            ← SERVICE
├── hospital-acceptance.html                      ← SERVICE
├── doctor-appointment.html                       ← SERVICE
├── second-opinion-services.html                  ← SERVICE
├── custom-medical-packages.html                  ← SERVICE
├── medical-tourism-services.html                 ← SERVICE
│
├── air-ambulance-afghanistan.html                ← COUNTRY (×30)
├── air-ambulance-albania.html                    ← ...
├── ... (28 more country pages)
│
├── css/
│   ├── bootstrap.min.css
│   └── style.css
├── js/
│   ├── main.js
│   ├── blog.js
│   └── blog-detail.js
├── lib/
│   ├── easing/
│   ├── owlcarousel/
│   ├── tempusdominus/
│   └── waypoints/
└── img/ (57 images)
```

---

## 4. Issues Found

### 🔴 Critical Issues

#### Issue 1: Flat Structure — 30 Country + 11 Service Pages Clutter Root
All 49 HTML files sit in the root directory. This makes navigation, maintenance, and SEO management painful. **Your instinct to reorganize is 100% correct.**

#### Issue 2: GTM Missing From 48 of 49 Pages
Google Tag Manager (`GTM-KG4BQ6SM`) is **only on `index.html`**. Every other page is invisible to your analytics.

#### Issue 3: Supabase API Key Exposed in Client-Side Code
The Supabase anon key is hardcoded in **7 different HTML files** and **2 JS files** — all independently. If you rotate keys, you need to update 9 places.

#### Issue 4: Zero Canonical Tags on All 30 Country Pages
None of the country pages have `<link rel="canonical">`. This risks duplicate content penalties from search engines.

#### Issue 5: Zero Schema.org Markup on All 30 Country Pages
Country pages have no structured data at all, while service pages mostly do.

### 🟡 Moderate Issues

#### Issue 6: Inconsistent Link Formats in `country.html`
Most links use relative format (`air-ambulance-afghanistan.html`) but **Botswana and Brazil** use absolute path format (`/air-ambulance-botswana`) — and those pages don't even exist as files.

#### Issue 7: `Jost` Font Referenced but Never Loaded
CSS references `font-family: 'Jost', sans-serif` for navbar, but the Google Fonts `<link>` only loads Roboto.

#### Issue 8: CSS Syntax Error on Line 18
`style.css` line 18 has a stray `row` text after the closing brace.

#### Issue 9: Duplicate Supabase SDK Loads
`index.html` loads `@supabase/supabase-js@2` CDN **twice** (line 745 and line 832), and creates two separate clients.

#### Issue 10: Inconsistent Canonical Tag Formats
Some pages use relative (`href="contact.html"`), some use full URL (`href="https://airmedical24x7.com/about.html"`), and one uses a different slug (`ECMO-transfer.html` → `href="ecmo-transfer"`).

### 🟢 Minor Issues

#### Issue 11: `blog-detail046d.html` — Odd Filename
Looks like a hash/cache-bust was appended to the filename. Should be `blog-detail.html`.

#### Issue 12: Massive Code Duplication
Every page has a full copy of: topbar, navbar, SOS button/popup, footer, and JS includes. ~200+ lines duplicated across 49 files.

---

## 5. Restructuring Proposal

### Your Idea: Country + Service Folders

> [!IMPORTANT]
> **I fully agree** with your approach. Here's my detailed recommendation:

### Proposed New Structure

```
root/
├── index.html
├── about.html
├── contact.html
├── blog.html
├── blog-detail.html                    ← renamed from blog-detail046d.html
├── privacy-policy.html
├── terms-and-conditions.html
│
├── countries/
│   ├── index.html                      ← moved from country.html
│   ├── afghanistan.html                ← cleaner names
│   ├── albania.html
│   ├── algeria.html
│   ├── ... (all 30 country pages)
│   └── uae.html
│
├── services/
│   ├── air-ambulance.html
│   ├── air-ambulance-charters.html
│   ├── commercial-airlines-medical-transfer.html
│   ├── commercial-flight-stretcher.html
│   ├── ecmo-transfer.html              ← lowercase fix
│   ├── flight-medical-escort.html
│   ├── hospital-acceptance.html
│   ├── doctor-appointment.html
│   ├── second-opinion.html
│   ├── custom-medical-packages.html
│   └── medical-tourism.html
│
├── css/
├── js/
├── lib/
└── img/
```

### What This Requires

When files move into subfolders, **all relative paths need updating**:

| Reference Type | Current Path | New Path (from `countries/` or `services/`) |
|---|---|---|
| CSS | `css/style.css` | `../css/style.css` |
| JS | `js/main.js` | `../js/main.js` |
| Images | `img/logo.png` | `../img/logo.png` |
| Libraries | `lib/owlcarousel/...` | `../lib/owlcarousel/...` |
| Nav links | `about.html` | `../about.html` |
| Service links | `air-ambulance.html` | `../services/air-ambulance.html` |
| Country links | `air-ambulance-afghanistan.html` | `../countries/afghanistan.html` |

> [!WARNING]
> **SEO Impact**: Moving URLs is a big deal. If this site is already indexed by Google at the current URLs (`airmedical24x7.com/air-ambulance-afghanistan.html`), we need to:
> 1. Set up **301 redirects** on the web server (via `.htaccess` or hosting config)
> 2. Update all **canonical tags** to the new URLs
> 3. Submit updated **sitemap.xml** to Google Search Console
>
> **If the site is NOT yet indexed** or is being rebuilt, this is less of a concern.

---

## 6. Additional Improvements to Bundle With Restructuring

If we're already touching every file, we should also fix:

1. **Add GTM to all pages** — copy the GTM snippet to every `<head>` and `<body>`
2. **Add canonical tags** to all 30 country pages
3. **Fix Jost font** — either load it or remove the reference
4. **Fix CSS syntax error** — remove stray `row` on line 18
5. **Centralize Supabase config** — single JS file with the client init
6. **Fix `blog-detail046d.html`** → rename to `blog-detail.html`
7. **Fix broken country links** (Botswana, Brazil) in `country.html`
8. **Remove duplicate Supabase SDK load** in `index.html`

---

## Open Questions

> [!IMPORTANT]
> **Q1: Is this site already live and indexed by Google?**
> If yes, we need 301 redirects. If no (or it's a staging copy), we can just restructure freely.

> [!IMPORTANT]  
> **Q2: Do you plan to add more country pages?**
> If yes, we could consider a template-based approach (single HTML page that loads content dynamically based on URL parameter), rather than having 30+ individual HTML files.

> [!IMPORTANT]
> **Q3: Should we also fix the other issues (GTM, SEO, Supabase centralization) during the restructuring, or tackle those separately?**

---

## Verification Plan

### Automated Tests
- Open every page locally and verify no broken CSS/JS/image links
- Check all internal navigation links work correctly
- Verify Supabase form submission still works on homepage

### Manual Verification
- Preview restructured site in browser
- Check mobile responsiveness on key pages
- Validate that country listing page links all resolve correctly
