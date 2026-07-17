self.addEventListener('install', event => {
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  if (url.origin === self.location.origin && event.request.mode === 'navigate') {
    const pathname = url.pathname;
    const lastSegment = pathname.substring(pathname.lastIndexOf('/') + 1);

    if (pathname !== '/' && !lastSegment.includes('.')) {
      const cleanPath = pathname.endsWith('/') ? pathname.slice(0, -1) : pathname;
      const slug = cleanPath.substring(cleanPath.lastIndexOf('/') + 1);

      let targetUrl;

      const services = [
        "air-ambulance",
        "commercial-flight-stretcher",
        "flight-medical-escort-services",
        "hospital-acceptance",
        "doctor-appointment",
        "second-opinion-services",
        "ECMO-transfer",
        "commercial-airlines-medical-transfer-services",
        "air-ambulance-charters",
        "organ-transplant-assistance",
        "medical-tourism",
        "medical-travel-assistance",
        "home-health-care"
      ];

      if (cleanPath === '/countries') {
        // /countries → /countries.html
        targetUrl = '/countries.html' + url.search;
      } else if (services.includes(slug)) {
        // Service pages live in /services/ directory — NOT at root
        targetUrl = '/services/' + slug + '.html' + url.search;
      } else if (slug.startsWith('air-ambulance-') && slug !== 'air-ambulance-charters') {
        // Country pages live in /countries/ directory — NOT at root
        // e.g. /air-ambulance-india → /countries/air-ambulance-india.html
        targetUrl = '/countries/' + slug + '.html' + url.search;
      } else {
        // Root pages, etc. — append .html in place
        // e.g. /about-us → /about-us.html
        targetUrl = cleanPath + '.html' + url.search;
      }

      event.respondWith(
        fetch(targetUrl).catch(() => fetch(event.request))
      );
    }
  }
});
