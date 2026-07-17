(function ($) {
    "use strict";
    
    // BUG-06 FIX: Dropdown on mouse hover — use CSS-class toggle instead of triggering click
    // to prevent Bootstrap's own click handler toggling the dropdown closed on hover+click.
    $(document).ready(function () {
        function toggleNavbarMethod() {
            if ($(window).width() > 992) {
                $('.navbar .dropdown')
                  .on('mouseover.hoverMenu', function () {
                    $(this).addClass('show');
                    $(this).find('.dropdown-menu').addClass('show');
                  })
                  .on('mouseout.hoverMenu', function () {
                    $(this).removeClass('show');
                    $(this).find('.dropdown-menu').removeClass('show');
                  });
            } else {
                $('.navbar .dropdown').off('mouseover.hoverMenu mouseout.hoverMenu');
            }
        }
        toggleNavbarMethod();
        $(window).resize(toggleNavbarMethod);

        // Move form above the image on mobile in service pages
        const quoteForm = document.getElementById("quoteForm");
        const target = document.querySelector(".services-mobile-form-target");
        if (quoteForm && target) {
            const formCol = quoteForm.closest('.col-lg-5');
            const originalParent = formCol ? formCol.parentElement : null;

            function moveServicesForm() {
                if (formCol && originalParent) {
                    if ($(window).width() < 768) {
                        if (!target.contains(formCol)) {
                            target.appendChild(formCol);
                        }
                    } else {
                        if (!originalParent.contains(formCol)) {
                            originalParent.appendChild(formCol);
                        }
                    }
                }
            }
            moveServicesForm();
            $(window).resize(moveServicesForm);
        }
    });


    // Date and time picker
    $('.date').datetimepicker({
        format: 'L'
    });
    $('.time').datetimepicker({
        format: 'LT'
    });
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Price carousel
    $(".price-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        margin: 45,
        dots: false,
        loop: true,
        nav : true,
        navText : [
            '<i class="bi bi-arrow-left"></i>',
            '<i class="bi bi-arrow-right"></i>'
        ],
        responsive: {
            0:{
                items:1
            },
            992:{
                items:2
            },
            1200:{
                items:3
            }
        }
    });


    // Team carousel
    $(".team-carousel, .related-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        margin: 45,
        dots: false,
        loop: true,
        nav : true,
        navText : [
            '<i class="bi bi-arrow-left"></i>',
            '<i class="bi bi-arrow-right"></i>'
        ],
        responsive: {
            0:{
                items:1
            },
            992:{
                items:2
            }
        }
    });


    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        items: 1,
        dots: true,
        loop: true,
    });

    // BUG-05 FIX: Dynamic Navbar Active State — exact segment matching prevents false positives
    $(window).on('load', function() {
        let path = window.location.pathname;
        if (path === '' || path === '/index.html' || path === '/index') {
            path = '/';
        }
        // Normalize: remove trailing slash except root
        if (path !== '/' && path.endsWith('/')) path = path.slice(0, -1);

        $('.navbar-nav a').each(function() {
            const href = $(this).attr('href');
            if (!href || href === '#') return;

            let cleanHref = href.replace(/^\.\.\//, '').replace(/\.html$/, '');
            if (cleanHref === 'index' || cleanHref === '/index') cleanHref = '/';
            if (!cleanHref.startsWith('/')) cleanHref = '/' + cleanHref;

            let match = false;
            if (cleanHref === '/' && path === '/') {
                match = true;
            } else if (cleanHref !== '/') {
                // Exact match or path starts with cleanHref followed by /
                match = path === cleanHref || path.startsWith(cleanHref + '/');
            }

            if (match) {
                $(this).addClass('active');
                $(this).closest('.dropdown').find('.nav-link').first().addClass('active');
            } else {
                $(this).removeClass('active');
            }
        });
    });
    
})(jQuery);


function toggleSOS() {
  const popup = document.getElementById("sos-popup");
  popup.style.display = popup.style.display === "block" ? "none" : "block";
}




/* ================= NAME + COUNTRY DATA ================= */

const regions = [
  {
    country: "India",
    cities: ["Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad", "Pune", "Kochi"],
    maleNames: ["Rahul", "Amit", "Suresh", "Vikram", "Rohit", "Ankit"],
    femaleNames: ["Priya", "Neha", "Anjali", "Kavita", "Pooja", "Sneha"]
  },
  {
    country: "UAE",
    cities: ["Dubai", "Abu Dhabi", "Sharjah", "Ajman"],
    maleNames: ["Mohammed", "Ahmed", "Hassan", "Omar", "Yusuf"],
    femaleNames: ["Aisha", "Fatima", "Zainab", "Maryam", "Noor"]
  },
  {
    country: "Saudi Arabia",
    cities: ["Riyadh", "Jeddah", "Dammam"],
    maleNames: ["Abdullah", "Khalid", "Fahad", "Salman", "Nasser"],
    femaleNames: ["Reem", "Huda", "Laila", "Amal", "Sara"]
  },
  {
    country: "USA",
    cities: ["New York", "Los Angeles", "Chicago", "Houston", "Miami"],
    maleNames: ["John", "Michael", "David", "James", "Robert"],
    femaleNames: ["Emily", "Jessica", "Sarah", "Ashley", "Olivia"]
  },
  {
    country: "UK",
    cities: ["London", "Manchester", "Birmingham"],
    maleNames: ["Oliver", "Harry", "Jack", "George"],
    femaleNames: ["Amelia", "Isla", "Sophia", "Charlotte"]
  }
];

/* ================= HELPER FUNCTIONS ================= */

function maskName(name) {
  if (name.length <= 3) return name[0] + "***";
  return name.substring(0, 3) + "***";
}

function getRandomItem(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

/* ================= SOCIAL PROOF FUNCTION ================= */

function showSocialProof() {
  const box = document.getElementById("social-proof");
  const text = document.getElementById("proof-text");
  if (!box || !text) return;

  const region = getRandomItem(regions);
  const gender = Math.random() > 0.5 ? "male" : "female";

  const name = gender === "male"
    ? getRandomItem(region.maleNames)
    : getRandomItem(region.femaleNames);

  const city = getRandomItem(region.cities);

  text.innerHTML = `
    <strong>${maskName(name)}</strong> from 
    <strong>${city}</strong> just requested a free quotation
  `;

  box.classList.remove("hidden");

  setTimeout(() => {
    box.classList.add("hidden");
  }, 5000);
}

/* ================= AUTO RUN ================= */

// BUG-08 FIX: Only run social proof if the element exists; clear interval if it doesn't
setTimeout(function() {
  const box = document.getElementById("social-proof");
  if (!box) return;
  showSocialProof();
  setInterval(showSocialProof, 18000);
}, 6000);



// BUG-04 FIX: Guard against null element on pages that don't have #countrySearch
function filterCountries() {
    const input = document.getElementById("countrySearch");
    if (!input) return;
    const filter = input.value.toLowerCase().trim();
    const cards = document.querySelectorAll(".country-card");

    cards.forEach(card => {
        const text = card.innerText.toLowerCase();
        const col = card.closest(".col-lg-3, .col-md-4, .col-sm-6");
        if (col) col.style.display = text.includes(filter) ? "" : "none";
    });
}

// Local development helper: Service Worker to handle extensionless URLs on VS Code Live Server
if ('serviceWorker' in navigator && (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')) {
    navigator.serviceWorker.register('/sw.js')
        .then(function() {
            console.log('Local URL Router Service Worker registered successfully.');
        })
        .catch(function(err) {
            console.error('Service Worker registration failed:', err);
        });
}





