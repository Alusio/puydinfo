var staticCacheName = "django-pwa-v0.4.3";

var filesToCache = [
    '/static/theme/css/font-awesome.min.css',
    '/static/theme/css/style.css',
    '/static/theme/css/bootstrap.min.css',
    '/static/favicon/favicon-2.ico',
    '/static/logo_puydinfo.png',
    '/static/new_theme/css/themify-icons.css',
    '/static/new_theme/css/flaticon.css',
    '/static/new_theme/vendors/fontawesome/css/all.min.css',
    '/static/new_theme/vendors/animate-css/animate.css',
    '/static/new_theme/vendors/popup/magnific-popup.css',
    '/static/js/loader/jquery.min.js',
    '/static/js/loader/pace.js',
    '/static/theme/js/jquery.min.js',
    '/static/theme/js/bootstrap.min.js',
    '/static/theme/js/jquery.stellar.min.js',
    '/static/theme/js/main.js',
    '/static/cookie/cookiealert.css',
    '/static/cookie/cookiealert.js',
    '/static/new_theme/vendors/fontawesome/webfonts/fa-brands-400.woff2',
    '/static/new_theme/vendors/fontawesome/webfonts/fa-brands-400.ttf',
    '/static/logo_app_192.png',
    'manifest.json',
    '/static/new_theme/vendors/fontawesome/webfonts/fa-solid-900.woff2',
    '/static/new_theme/vendors/fontawesome/webfonts/fa-solid-900.ttf',
    '/static/theme/css/timeline.css',
    '/static/js/idb.js',
    '/static/js/idbop.js',
    '/show/cinescenie',
    '/show/triomphe',
    '/show/vikings',
    '/show/oiseaux',
    '/show/lance',
    '/show/chevaliers',
    '/show/renaissance',
    '/show/panache',
    '/show/mousquetaire',
    '/show/orgues',
    '/show/perouse',
    '/show/verdun',
    '/show/royaume',
    '/offline/',
    '/index_off',
    '/mentions_legales'

];

// Cache on install
self.addEventListener("install", event => {
    this.skipWaiting();
    event.waitUntil(
        caches.open(staticCacheName)
            .then(cache => {
                return cache.addAll(filesToCache);
            })
    )
});

// Clear cache on activate
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(cacheName => (cacheName.startsWith("django-pwa-")))
                    .filter(cacheName => (cacheName !== staticCacheName))
                    .map(cacheName => caches.delete(cacheName))
            );
        })
    );
});

// Serve from Cache
self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                return response || fetch(event.request);
            })
            .catch(() => {
                return caches.match('/index_off');
            })
    );

});





