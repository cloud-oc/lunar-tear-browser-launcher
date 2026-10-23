# Third-party components

- Lunar Tear: https://github.com/Walter-Sparrow/lunar-tear — MIT, copyright 2026 Ilya Groshev. `vendor/migrations/*.sql` is copied unchanged from v1.0.2, commit `63df7d70556a7180f04312abbafc56494cf70545`. Full license: `vendor/LUNAR-TEAR-LICENSE`. Server binaries are downloaded separately from the official release.
- scrcpy: https://github.com/Genymobile/scrcpy — Apache-2.0. Server v3.3.4 is downloaded separately and checked against its release SHA-256. Source and license: https://github.com/Genymobile/scrcpy/tree/v3.3.4 . The Python bridge implements the version-specific packet framing; it does not embed scrcpy source or binaries.
- aiohttp: https://github.com/aio-libs/aiohttp — Apache-2.0, installed through pip.
- psutil: https://github.com/giampaolo/psutil — BSD-3-Clause, installed through pip.
- MuMu, Android platform tools, and game client/resources are not distributed by this repository. Their respective licenses and terms apply.
