FROM node:21-alpine

WORKDIR /usr/src/app

# https://github.com/imagemin/optipng-bin/issues/97
ENV CPPFLAGS="-DPNG_ARM_NEON_OPT=0"
# https://stackoverflow.com/questions/69692842/error-message-error0308010cdigital-envelope-routinesunsupported
ENV NODE_OPTIONS="--openssl-legacy-provider"

# RUN apk add --no-cache python
RUN apk add --no-cache libpng-dev
COPY package.json package-lock.json ./
RUN apk add --no-cache --virtual .gyp \
        make \
        g++ \
        autoconf automake file g++ libtool make nasm \
        # python \
    && npm ci \
    && apk del .gyp \
    && rm package.json package-lock.json

COPY . .

ENTRYPOINT ["npm", "run"]