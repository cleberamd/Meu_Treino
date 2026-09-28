const CACHE_NAME = "5-essenciais-cache-v1";
const ASSETS_TO_CACHE = [
  "./",
  "./index.html",
  "./manifest.json"
];

// Instalação do Service Worker e Cache dos Arquivos
self.addEventListener("install", (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
});

// Ativação e Limpeza de Caches Antigos
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Interceptando Requisições (Estratégia: Cache First com fallback para Network)
self.addEventListener("fetch", (event) => {
  // Ignora requisições que não sejam GET (como POSTs e extensões)
  if (event.request.method !== "GET") return;

  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      // Retorna do cache se encontrar
      if (cachedResponse) {
        return cachedResponse;
      }
      // Se não, busca na rede
      return fetch(event.request).then((networkResponse) => {
        // Salva a nova resposta no cache para usos futuros
        return caches.open(CACHE_NAME).then((cache) => {
          cache.put(event.request, networkResponse.clone());
          return networkResponse;
        });
      });
    }).catch(() => {
      // Em caso de falha completa (offline e não tem no cache),
      // opcionalmente poderia retornar uma página offline padrão aqui.
    })
  );
});
