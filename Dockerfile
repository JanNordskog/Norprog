# syntax=docker/dockerfile:1.7
# ---- Stage 1: tiny build context (just to get a clean copy with --link semantics) ----
FROM alpine:3.20 AS prep
WORKDIR /site
COPY *.html robots.txt sitemap.xml llms.txt ./
COPY images ./images

# ---- Stage 2: nginx serves the static site ----
FROM nginx:1.27-alpine AS runtime

# Drop the default nginx config and use ours
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Site files
COPY --from=prep /site/ /usr/share/nginx/html/

# Run as non-root for better security (nginx alpine already supports this)
# The official image handles the user switch in entrypoint; we just expose 8080
EXPOSE 8080

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:8080/ || exit 1

LABEL org.opencontainers.image.title="Norprog" \
      org.opencontainers.image.description="Norprog — skreddersydde nettsider til norske bedrifter" \
      org.opencontainers.image.url="https://norprog.no" \
      org.opencontainers.image.source="https://github.com/jannordskog/norprog" \
      org.opencontainers.image.authors="Jan Nordskog <hei@norprog.no>" \
      org.opencontainers.image.licenses="Proprietary"

CMD ["nginx", "-g", "daemon off;"]
