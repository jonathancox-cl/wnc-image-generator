#!/bin/bash
apt-get install -y fonts-dejavu fonts-crosextra-caladea || true
pip install -r requirements.txt
#!/bin/bash
apt-get update && apt-get install -y \
  libjpeg-dev \
    zlib1g-dev \
      libpng-dev \
        fonts-dejavu \
          fonts-crosextra-caladea \
            || true
            pip install --upgrade pip
            pip install -r requirements.txt
