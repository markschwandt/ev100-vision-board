#!/usr/bin/env python3
"""
EV100 Vision Board — Image Self-Hosting Script
Downloads all 137 Pinterest images and rewrites index.html to use local paths.

Usage:
  python3 scripts/download_images.py

Then commit and push:
  git add images/ index.html
  git commit -m "self-host all vision board images"
  git push
"""

import requests
import os
import time
import sys

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Referer": "https://www.pinterest.com/",
    "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
}

IMAGES = [
    {"src":"https://i.pinimg.com/736x/47/c3/3e/47c33e25d4eec31fe42d289f63784978.jpg","dest":"images/immersive/immersive-01.jpg"},
    {"src":"https://i.pinimg.com/736x/02/12/b5/0212b57447dd7eb648d63970bc511525.jpg","dest":"images/immersive/immersive-02.jpg"},
    {"src":"https://i.pinimg.com/736x/65/9c/b4/659cb462700d67601b99304adce6a0f5.jpg","dest":"images/immersive/immersive-03.jpg"},
    {"src":"https://i.pinimg.com/736x/6e/9f/9a/6e9f9aee8ede0796c0dd24b738e316dd.jpg","dest":"images/immersive/immersive-04.jpg"},
    {"src":"https://i.pinimg.com/736x/5b/e8/b0/5be8b02014994ce7d21c4f9250e1d516.jpg","dest":"images/immersive/immersive-05.jpg"},
    {"src":"https://i.pinimg.com/736x/10/d4/50/10d450f0b5291c46406a14c5550c96b7.jpg","dest":"images/immersive/immersive-06.jpg"},
    {"src":"https://i.pinimg.com/736x/72/4d/e6/724de6a100b5d8137569123f1bc1bae9.jpg","dest":"images/immersive/immersive-07.jpg"},
    {"src":"https://i.pinimg.com/736x/f9/b9/09/f9b90933629f425d51d16d3990036b87.jpg","dest":"images/immersive/immersive-08.jpg"},
    {"src":"https://i.pinimg.com/736x/e5/48/41/e548419fe15819e3306a2a84f9661201.jpg","dest":"images/immersive/immersive-09.jpg"},
    {"src":"https://i.pinimg.com/736x/06/63/ac/0663ac00de66966ebffe8d4cd8b20521.jpg","dest":"images/immersive/immersive-10.jpg"},
    {"src":"https://i.pinimg.com/736x/95/6a/e3/956ae36f38fac4c2fda42dae42d24172.jpg","dest":"images/stage/stage-01.jpg"},
    {"src":"https://i.pinimg.com/736x/a5/b4/e3/a5b4e3a5a853cd901d4c08d07e1e315d.jpg","dest":"images/stage/stage-02.jpg"},
    {"src":"https://i.pinimg.com/736x/f6/fd/b6/f6fdb606f5d4b3570a63d81e1fc4e348.jpg","dest":"images/stage/stage-03.jpg"},
    {"src":"https://i.pinimg.com/736x/56/7b/6e/567b6e87457065e24d4cb7dbc0a52e8c.jpg","dest":"images/stage/stage-04.jpg"},
    {"src":"https://i.pinimg.com/736x/f4/09/de/f409dedc332942884710fe3f03aee3e6.jpg","dest":"images/stage/stage-05.jpg"},
    {"src":"https://i.pinimg.com/736x/aa/b8/68/aab8681820e399d2e9092572e734f3c1.jpg","dest":"images/stage/stage-06.jpg"},
    {"src":"https://i.pinimg.com/736x/bb/48/0a/bb480ae557d612df51633efea63b81ea.jpg","dest":"images/stage/stage-07.jpg"},
    {"src":"https://i.pinimg.com/736x/80/6e/95/806e9535618610d5691a844267aea73e.jpg","dest":"images/stage/stage-08.jpg"},
    {"src":"https://i.pinimg.com/736x/00/66/8a/00668a0123f06121f9de822675010f0d.jpg","dest":"images/stage/stage-09.jpg"},
    {"src":"https://i.pinimg.com/736x/73/15/27/731527fa80655604409331e100d56e58.jpg","dest":"images/stage/stage-10.jpg"},
    {"src":"https://i.pinimg.com/736x/1f/31/0e/1f310e918ddd6d3499d2dc4f603c424f.jpg","dest":"images/crowds/crowds-01.jpg"},
    {"src":"https://i.pinimg.com/736x/ec/fe/08/ecfe08c3017ee785447632ac271c1971.jpg","dest":"images/crowds/crowds-02.jpg"},
    {"src":"https://i.pinimg.com/736x/17/54/98/175498e1f0d0416f14a27432baa8c61b.jpg","dest":"images/crowds/crowds-03.jpg"},
    {"src":"https://i.pinimg.com/736x/53/3d/b3/533db3a193581bd0f59330724f4409c5.jpg","dest":"images/crowds/crowds-04.jpg"},
    {"src":"https://i.pinimg.com/736x/42/e6/fe/42e6fe1da36cefffc4566a0a1480067b.jpg","dest":"images/crowds/crowds-05.jpg"},
    {"src":"https://i.pinimg.com/736x/71/3d/00/713d00079ea8ed2f87760395e2593acd.jpg","dest":"images/crowds/crowds-06.jpg"},
    {"src":"https://i.pinimg.com/736x/92/58/f4/9258f4fc5920f7307f7ef1af22b64cb6.jpg","dest":"images/crowds/crowds-07.jpg"},
    {"src":"https://i.pinimg.com/736x/52/51/cc/5251cc4b4b648311626fd9a5f25fd16b.jpg","dest":"images/crowds/crowds-08.jpg"},
    {"src":"https://i.pinimg.com/736x/c4/46/35/c44635fd44fa4644f8243a02696fed29.jpg","dest":"images/brand/brand-01.jpg"},
    {"src":"https://i.pinimg.com/736x/2d/f2/d5/2df2d5a5a970779b01ce05985e4528e1.jpg","dest":"images/brand/brand-02.jpg"},
    {"src":"https://i.pinimg.com/736x/e6/59/c6/e659c6be668dc0d28b791158332f91d7.jpg","dest":"images/brand/brand-03.jpg"},
    {"src":"https://i.pinimg.com/736x/ef/83/83/ef8383117694097eeca5de727e016f99.jpg","dest":"images/brand/brand-04.jpg"},
    {"src":"https://i.pinimg.com/736x/63/57/15/6357154462c136688441055a280b5941.jpg","dest":"images/brand/brand-05.jpg"},
    {"src":"https://i.pinimg.com/736x/97/e6/bf/97e6bf17638d8c80cc0a3822fc3e2b62.jpg","dest":"images/brand/brand-06.jpg"},
    {"src":"https://i.pinimg.com/736x/d8/88/53/d888530c87c6794976d2825df47c6159.jpg","dest":"images/brand/brand-07.jpg"},
    {"src":"https://i.pinimg.com/736x/a6/7f/30/a67f302703e72eb2e1dd54ad510f6ff2.jpg","dest":"images/brand/brand-08.jpg"},
    {"src":"https://i.pinimg.com/736x/b9/59/82/b95982319a7f95944a6381d00f94ac1b.jpg","dest":"images/typography/typography-01.jpg"},
    {"src":"https://i.pinimg.com/736x/4b/4d/48/4b4d48741007cc8906033a2d41a1efae.jpg","dest":"images/typography/typography-02.jpg"},
    {"src":"https://i.pinimg.com/736x/f7/9f/c0/f79fc03df8104a825500366e1d95c0b3.jpg","dest":"images/typography/typography-03.jpg"},
    {"src":"https://i.pinimg.com/736x/e2/fc/89/e2fc89daa535fa6b8ba67a39c884834a.jpg","dest":"images/typography/typography-04.jpg"},
    {"src":"https://i.pinimg.com/736x/d3/b6/08/d3b60899b0daeacb92ba5317cf1bcec1.jpg","dest":"images/typography/typography-05.jpg"},
    {"src":"https://i.pinimg.com/736x/5b/bd/e6/5bbde61cbfd1a96922cade7522b3078d.jpg","dest":"images/typography/typography-06.jpg"},
    {"src":"https://i.pinimg.com/736x/47/97/5c/47975ca0b7906dd8121008a973f47bcc.jpg","dest":"images/typography/typography-07.jpg"},
    {"src":"https://i.pinimg.com/736x/54/f7/7d/54f77d848c49dac7d88d7cbdfb3b6581.jpg","dest":"images/typography/typography-08.jpg"},
    {"src":"https://i.pinimg.com/736x/a3/7f/a6/a37fa657c1166c27262242c40aca065c.jpg","dest":"images/performance/performance-01.jpg"},
    {"src":"https://i.pinimg.com/736x/e1/12/c6/e112c6c2faf141f56a725907fd42c033.jpg","dest":"images/performance/performance-02.jpg"},
    {"src":"https://i.pinimg.com/736x/fe/5b/c0/fe5bc0c5b4eaba16800e62ac8eefed2d.jpg","dest":"images/performance/performance-03.jpg"},
    {"src":"https://i.pinimg.com/736x/74/2b/84/742b84cd0f4e2d30b7d03662713bd63f.jpg","dest":"images/performance/performance-04.jpg"},
    {"src":"https://i.pinimg.com/736x/d9/24/64/d92464aed0360a941ff4b943a505075d.jpg","dest":"images/performance/performance-05.jpg"},
    {"src":"https://i.pinimg.com/736x/d0/f7/12/d0f71234ce4725d61478c4b6ffd8fe0d.jpg","dest":"images/performance/performance-06.jpg"},
    {"src":"https://i.pinimg.com/736x/1c/75/d8/1c75d813d259f41175c221cffe5966a9.jpg","dest":"images/performance/performance-07.jpg"},
    {"src":"https://i.pinimg.com/736x/d1/44/0f/d1440f4a603a6fde49f8fae0313efe45.jpg","dest":"images/performance/performance-08.jpg"},
    {"src":"https://i.pinimg.com/736x/89/8f/0e/898f0e8353d00d087200d83e0c3f38d8.jpg","dest":"images/spatial/spatial-01.jpg"},
    {"src":"https://i.pinimg.com/736x/23/1b/da/231bda250757512c0bee47b9780dac40.jpg","dest":"images/spatial/spatial-02.jpg"},
    {"src":"https://i.pinimg.com/736x/f5/03/ea/f503eaf1b17c911323aa488530903937.jpg","dest":"images/spatial/spatial-03.jpg"},
    {"src":"https://i.pinimg.com/736x/99/ff/1e/99ff1eaaba49bccaee988f10339d6d21.jpg","dest":"images/spatial/spatial-04.jpg"},
    {"src":"https://i.pinimg.com/736x/94/2b/c0/942bc08d489e309732f07e5ced42e373.jpg","dest":"images/spatial/spatial-05.jpg"},
    {"src":"https://i.pinimg.com/736x/aa/56/00/aa560047eef4e6a7dac926c6d6555c74.jpg","dest":"images/spatial/spatial-06.jpg"},
    {"src":"https://i.pinimg.com/736x/fd/be/f3/fdbef31283b00c8c25c9f36ef313399f.jpg","dest":"images/spatial/spatial-07.jpg"},
    {"src":"https://i.pinimg.com/736x/06/13/41/061341442661306353f221e924af95c0.jpg","dest":"images/spatial/spatial-08.jpg"},
    {"src":"https://i.pinimg.com/736x/c4/1d/57/c41d57ffae23a218bdc061a9f0fa43be.jpg","dest":"images/engineers/engineers-01.jpg"},
    {"src":"https://i.pinimg.com/736x/44/de/be/44debebd45c0216eb8f23726b3b35fc1.jpg","dest":"images/engineers/engineers-02.jpg"},
    {"src":"https://i.pinimg.com/736x/f0/4d/2c/f04d2cf3ab32096c786caf5616f5ec0f.jpg","dest":"images/engineers/engineers-03.jpg"},
    {"src":"https://i.pinimg.com/736x/0e/61/3e/0e613e1dd133cb9bea3799972a3e835a.jpg","dest":"images/engineers/engineers-04.jpg"},
    {"src":"https://i.pinimg.com/736x/60/05/c6/6005c63bfddbd002b20e3a64a8950f41.jpg","dest":"images/engineers/engineers-05.jpg"},
    {"src":"https://i.pinimg.com/736x/80/ed/67/80ed670e48220b56fdec623efec035a3.jpg","dest":"images/engineers/engineers-06.jpg"},
    {"src":"https://i.pinimg.com/736x/e3/59/60/e35960a76ce1733ff4d1e242f60eb112.jpg","dest":"images/engineers/engineers-07.jpg"},
    {"src":"https://i.pinimg.com/736x/9f/3f/65/9f3f65466ac9bad8f86c3d913091e2f7.jpg","dest":"images/engineers/engineers-08.jpg"},
    {"src":"https://i.pinimg.com/736x/63/4b/da/634bda273e6624921e90812b055a3a3d.jpg","dest":"images/community/community-01.jpg"},
    {"src":"https://i.pinimg.com/736x/9e/da/51/9eda512b6df846b0ec8cb5d967ead8c3.jpg","dest":"images/community/community-02.jpg"},
    {"src":"https://i.pinimg.com/736x/2a/cb/c3/2acbc3f32feafb6d334e4a6bc153a084.jpg","dest":"images/community/community-03.jpg"},
    {"src":"https://i.pinimg.com/736x/94/25/ab/9425abb8f5123f73d6c5674ca4b7771c.jpg","dest":"images/community/community-04.jpg"},
    {"src":"https://i.pinimg.com/736x/63/89/fb/6389fbccb2b4dffd992c0bc6f3185c3f.jpg","dest":"images/community/community-05.jpg"},
    {"src":"https://i.pinimg.com/736x/a1/32/c3/a132c355e2076150f6ba13fc92f32f69.jpg","dest":"images/community/community-06.jpg"},
    {"src":"https://i.pinimg.com/736x/6a/96/0b/6a960bf2a226b5762039294b92bcf331.jpg","dest":"images/community/community-07.jpg"},
    {"src":"https://i.pinimg.com/736x/95/ab/d4/95abd4636852f89b8b84804a408e5c51.jpg","dest":"images/community/community-08.jpg"},
    {"src":"https://i.pinimg.com/736x/60/9d/d2/609dd241b4982728d82b3c7a2c8a7f71.jpg","dest":"images/light/light-01.jpg"},
    {"src":"https://i.pinimg.com/736x/05/e5/d5/05e5d5a3d20db86b3e2570869ac43f9a.jpg","dest":"images/light/light-02.jpg"},
    {"src":"https://i.pinimg.com/736x/47/bb/7e/47bb7ea5f54190882e87d4263ba7d0f6.jpg","dest":"images/light/light-03.jpg"},
    {"src":"https://i.pinimg.com/736x/d2/84/66/d284661b94e55d81383e94b65639d22f.jpg","dest":"images/light/light-04.jpg"},
    {"src":"https://i.pinimg.com/736x/5c/44/58/5c4458053bfb496b7f4fbe291e2dabc1.jpg","dest":"images/light/light-05.jpg"},
    {"src":"https://i.pinimg.com/736x/c9/c3/d7/c9c3d7d366ecc7e5e9374cf5113ca75e.jpg","dest":"images/light/light-06.jpg"},
    {"src":"https://i.pinimg.com/736x/7b/72/f8/7b72f8827b5dac158f88c581f59d7923.jpg","dest":"images/light/light-07.jpg"},
    {"src":"https://i.pinimg.com/736x/84/67/88/846788f7262f28e65edf19c4e25a25f0.jpg","dest":"images/light/light-08.jpg"},
    {"src":"https://i.pinimg.com/736x/73/d4/9d/73d49dd8d71a4ba7936b65ee7fc8a253.jpg","dest":"images/anniversary/anniversary-01.jpg"},
    {"src":"https://i.pinimg.com/736x/9b/7c/63/9b7c63e9389f10718b9727ca8546365e.jpg","dest":"images/anniversary/anniversary-02.jpg"},
    {"src":"https://i.pinimg.com/736x/9d/fc/46/9dfc4632ffd7366b17cdbb37fd8c2590.jpg","dest":"images/anniversary/anniversary-03.jpg"},
    {"src":"https://i.pinimg.com/736x/7e/1c/8c/7e1c8cdc6a3d2d99c60df8ed88fd5515.jpg","dest":"images/anniversary/anniversary-04.jpg"},
    {"src":"https://i.pinimg.com/736x/f0/e4/73/f0e473b75a21ec2a8350c566a360ee20.jpg","dest":"images/anniversary/anniversary-05.jpg"},
    {"src":"https://i.pinimg.com/736x/8e/36/40/8e36401fce6e09e7e5126821b11e1d4d.jpg","dest":"images/anniversary/anniversary-06.jpg"},
    {"src":"https://i.pinimg.com/736x/99/2b/e6/992be6e30a5b5a4ca25996b9fca13575.jpg","dest":"images/anniversary/anniversary-07.jpg"},
    {"src":"https://i.pinimg.com/736x/b2/46/18/b2461872f92bf8655461c537874af14c.jpg","dest":"images/anniversary/anniversary-08.jpg"},
    {"src":"https://i.pinimg.com/736x/fc/2f/b0/fc2fb01e3857e8ee8a4b5f3c59ab7f9e.jpg","dest":"images/anniversary/anniversary-09.jpg"},
    {"src":"https://i.pinimg.com/736x/c6/72/7e/c6727e356b03488802e0d5ad5a5bc133.jpg","dest":"images/product/product-01.jpg"},
    {"src":"https://i.pinimg.com/736x/5b/45/fb/5b45fb82411e7b48041dfe4f922251dc.jpg","dest":"images/product/product-02.jpg"},
    {"src":"https://i.pinimg.com/736x/65/75/1e/65751ea5da8a8d024b8bf68116a406b0.jpg","dest":"images/product/product-03.jpg"},
    {"src":"https://i.pinimg.com/736x/e0/e8/18/e0e818eb3f6a8faab3f6b320ab616f72.jpg","dest":"images/product/product-04.jpg"},
    {"src":"https://i.pinimg.com/736x/27/f6/0d/27f60daa86a2bbaeac6ef46dd4489b60.jpg","dest":"images/product/product-05.jpg"},
    {"src":"https://i.pinimg.com/736x/0a/5b/1f/0a5b1fb7644d3a757748860b1953c9fa.jpg","dest":"images/product/product-06.jpg"},
    {"src":"https://i.pinimg.com/736x/e7/9e/75/e79e7566b04b0a71e0f95f2d5136d628.jpg","dest":"images/product/product-07.jpg"},
    {"src":"https://i.pinimg.com/736x/2f/cc/30/2fcc3023c83f54234d1019f9e4d47404.jpg","dest":"images/product/product-08.jpg"},
    {"src":"https://i.pinimg.com/736x/89/82/d7/8982d7531c2e3b7c8f6c05e5fbd6526a.jpg","dest":"images/product/product-09.jpg"},
    {"src":"https://i.pinimg.com/736x/8a/24/40/8a2440158da486149683b6dad58fe38f.jpg","dest":"images/product/product-10.jpg"},
    {"src":"https://i.pinimg.com/736x/48/f3/85/48f3854c9ea99ae7927f3179fd069b28.jpg","dest":"images/product/product-11.jpg"},
    {"src":"https://i.pinimg.com/736x/5d/36/a8/5d36a843b96295f2060a04190a8046e6.jpg","dest":"images/product/product-12.jpg"},
    {"src":"https://i.pinimg.com/736x/81/75/a7/8175a7140954ea4451e35842d656acd8.jpg","dest":"images/product/product-13.jpg"},
    {"src":"https://i.pinimg.com/736x/73/d7/d1/73d7d1548aa60ba0846b9b4940d415c6.jpg","dest":"images/product/product-14.jpg"},
    {"src":"https://i.pinimg.com/736x/61/ea/c4/61eac43723c000969af6c2e2569ff92e.jpg","dest":"images/product/product-15.jpg"},
    {"src":"https://i.pinimg.com/736x/4e/a9/f4/4ea9f41e2d2d2549a77e549cf6ffb56a.jpg","dest":"images/product/product-16.jpg"},
    {"src":"https://i.pinimg.com/736x/b4/a6/b6/b4a6b6aaf3b816fc5955d74b69de871b.jpg","dest":"images/experiential/experiential-01.jpg"},
    {"src":"https://i.pinimg.com/736x/6b/fa/14/6bfa141b0d42ba60144891dec453ce91.jpg","dest":"images/experiential/experiential-02.jpg"},
    {"src":"https://i.pinimg.com/736x/5d/66/ab/5d66ab4309b69bac91416ee2cacd3a65.jpg","dest":"images/experiential/experiential-03.jpg"},
    {"src":"https://i.pinimg.com/736x/85/cb/ed/85cbed8b5359e9166cda2ada8f28e274.jpg","dest":"images/experiential/experiential-04.jpg"},
    {"src":"https://i.pinimg.com/736x/b5/2e/71/b52e710d4acd715f0ea7418148259f5b.jpg","dest":"images/experiential/experiential-05.jpg"},
    {"src":"https://i.pinimg.com/736x/bd/9d/95/bd9d9569e1fe940fbdd6472492d43709.jpg","dest":"images/experiential/experiential-06.jpg"},
    {"src":"https://i.pinimg.com/736x/56/df/b2/56dfb2a92f740795902519df9704022e.jpg","dest":"images/experiential/experiential-07.jpg"},
    {"src":"https://i.pinimg.com/736x/eb/a9/86/eba98670efd4ecec792a0c90dbc71142.jpg","dest":"images/experiential/experiential-08.jpg"},
    {"src":"https://i.pinimg.com/736x/7e/1c/cc/7e1ccc8a3e16b2d5640f07e42d44b5a6.jpg","dest":"images/experiential/experiential-09.jpg"},
    {"src":"https://i.pinimg.com/736x/5a/e5/cb/5ae5cb2eab57bd2339544e24c81f7f14.jpg","dest":"images/experiential/experiential-10.jpg"},
    {"src":"https://i.pinimg.com/736x/d4/37/3a/d4373a3fc80a253bf401333e3a5a357d.jpg","dest":"images/experiential/experiential-11.jpg"},
    {"src":"https://i.pinimg.com/736x/6d/e3/f4/6de3f468e098c89d9c75a2d27c8459b2.jpg","dest":"images/experiential/experiential-12.jpg"},
    {"src":"https://i.pinimg.com/736x/4f/6e/bb/4f6ebb5655876f81cf99a7e999fea657.jpg","dest":"images/experiential/experiential-13.jpg"},
    {"src":"https://i.pinimg.com/736x/b8/ca/6e/b8ca6eda0345c928e84bef76c1559f5d.jpg","dest":"images/experiential/experiential-14.jpg"},
    {"src":"https://i.pinimg.com/736x/c0/8f/97/c08f9714f7dede92a0cfc751778645cd.jpg","dest":"images/experiential/experiential-15.jpg"},
    {"src":"https://i.pinimg.com/736x/73/23/89/732389a3e9bbfcd23ec2fd214e8db5ec.jpg","dest":"images/backstage/backstage-01.jpg"},
    {"src":"https://i.pinimg.com/736x/70/c7/79/70c779f1ebf06e8b54c103a7d52903f4.jpg","dest":"images/backstage/backstage-02.jpg"},
    {"src":"https://i.pinimg.com/736x/4d/84/f7/4d84f7779e1c66ea346928ce9c95c9a4.jpg","dest":"images/backstage/backstage-03.jpg"},
    {"src":"https://i.pinimg.com/736x/cf/3c/b1/cf3cb18584dc606362d62ba10ab77033.jpg","dest":"images/backstage/backstage-04.jpg"},
    {"src":"https://i.pinimg.com/736x/90/5f/94/905f94376c2b9896e2586ed1261c1936.jpg","dest":"images/backstage/backstage-05.jpg"},
    {"src":"https://i.pinimg.com/736x/0d/17/7c/0d177cadf4e0cc003c5377648a247dd4.jpg","dest":"images/backstage/backstage-06.jpg"},
    {"src":"https://i.pinimg.com/736x/92/74/91/927491fd225c8efa04166eead05cf3c5.jpg","dest":"images/backstage/backstage-07.jpg"},
    {"src":"https://i.pinimg.com/736x/c0/71/be/c071be6160afeaa54f56fa441843c022.jpg","dest":"images/backstage/backstage-08.jpg"},
    {"src":"https://i.pinimg.com/736x/c6/2a/dc/c62adc776682773afd244924fd689d77.jpg","dest":"images/backstage/backstage-09.jpg"},
    {"src":"https://i.pinimg.com/736x/15/9d/ce/159dce9f3e045f220c340a61e5e9235c.jpg","dest":"images/backstage/backstage-10.jpg"},
    {"src":"https://i.pinimg.com/736x/97/b8/7f/97b87f5d19f02c0844347afa411e874b.jpg","dest":"images/backstage/backstage-11.jpg"},
    {"src":"https://i.pinimg.com/736x/96/0c/22/960c2297fe394d6ef18b6b09fb3261ad.jpg","dest":"images/backstage/backstage-12.jpg"},
    {"src":"https://i.pinimg.com/736x/58/e4/03/58e403645de030ba0f76d34950344cc2.jpg","dest":"images/backstage/backstage-13.jpg"}
]

def download_all():
    session = requests.Session()
    session.headers.update(HEADERS)

    ok = 0
    fail = 0
    failed = []

    total = len(IMAGES)
    print(f"Starting download of {total} images...\n")

    for i, img in enumerate(IMAGES, 1):
        src  = img["src"]
        dest = img["dest"]

        os.makedirs(os.path.dirname(dest), exist_ok=True)

        # Skip if already downloaded and looks valid
        if os.path.exists(dest) and os.path.getsize(dest) > 5000:
            print(f"  [{i:3d}/{total}] SKIP  {dest}")
            ok += 1
            continue

        try:
            r = session.get(src, timeout=20)
            if r.status_code == 200 and len(r.content) > 5000:
                with open(dest, "wb") as f:
                    f.write(r.content)
                kb = len(r.content) // 1024
                print(f"  [{i:3d}/{total}] OK    {dest} ({kb}KB)")
                ok += 1
            else:
                print(f"  [{i:3d}/{total}] FAIL  {dest} (HTTP {r.status_code})")
                fail += 1
                failed.append(dest)
        except Exception as e:
            print(f"  [{i:3d}/{total}] ERR   {dest} — {e}")
            fail += 1
            failed.append(dest)

        time.sleep(0.25)  # polite pacing

    print(f"\n{'='*50}")
    print(f"Done: {ok} downloaded, {fail} failed")

    if failed:
        print("\nFailed images:")
        for f in failed:
            print(f"  {f}")

    return fail == 0


def rewrite_html():
    html_path = "index.html"
    if not os.path.exists(html_path):
        print(f"ERROR: {html_path} not found. Run from the repo root.")
        return False

    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    replaced = 0
    for img in IMAGES:
        if img["src"] in html:
            html = html.replace(img["src"], img["dest"])
            replaced += 1

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\nindex.html updated: {replaced} Pinterest URLs replaced with local paths")
    return True


if __name__ == "__main__":
    # Must be run from repo root
    if not os.path.exists("index.html"):
        print("ERROR: Run this script from the root of the ev100-vision-board repo.")
        print("  cd ev100-vision-board")
        print("  python3 scripts/download_images.py")
        sys.exit(1)

    success = download_all()
    rewrite_html()

    print("\nNext steps:")
    print("  git add images/ index.html")
    print('  git commit -m "feat: self-host all vision board images"')
    print("  git push")

    sys.exit(0 if success else 1)
