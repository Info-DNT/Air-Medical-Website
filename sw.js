self.addEventListener('install', event => {
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  
  // Only handle local requests
  if (url.origin === self.location.origin) {
    // Only handle document/page navigation requests
    if (event.request.mode === 'navigate') {
      const pathname = url.pathname;
      
      // Ignore root and files that already have an extension
      const lastSegment = pathname.substring(pathname.lastIndexOf('/') + 1);
      if (pathname !== '/' && !lastSegment.includes('.')) {
        // Strip trailing slash if present
        const cleanPath = pathname.endsWith('/') ? pathname.slice(0, -1) : pathname;
        
        let targetUrl;
        if (cleanPath === '/countries') {
          targetUrl = '/countries/index.html' + url.search;
        } else {
          targetUrl = cleanPath + '.html' + url.search;
        }
        
        event.respondWith(
          fetch(targetUrl).catch(() => fetch(event.request))
        );
      }
    }
  }
});
