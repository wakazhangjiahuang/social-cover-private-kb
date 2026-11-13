FROM node:24-alpine
WORKDIR /app
COPY public ./public
COPY lib/cover/runtime.mjs ./lib/cover/runtime.mjs
COPY standalone ./standalone
ENV STUDIO_HOST=0.0.0.0 PORT=29012 STUDIO_DATA_DIR=/data
RUN mkdir -p /data && chown node:node /data
USER node
VOLUME ["/data"]
EXPOSE 29012
CMD ["node", "standalone/server.mjs"]
