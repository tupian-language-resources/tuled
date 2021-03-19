# Releasing TuLed

1. Update the data in `raw/` and `etc/` running
   ```shell
   cldfbench download lexibank_tuled.py
   ```
2. Re-create the CLDF data running
   ```shell
   cldfbench lexibank.makecldf lexibank_tuled.py --glottolog-version v4.3 --concepticon-version v2.4.0 --clts-version v1.4.1
   ```
