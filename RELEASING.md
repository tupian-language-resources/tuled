# Releasing TuLed

1. Update the data in `raw/` and `etc/` running
   ```shell
   cldfbench download lexibank_tuled.py
   ```
2. Re-create the CLDF data running
   ```shell
   cldfbench lexibank.makecldf lexibank_tuled.py --glottolog-version v4.5 --concepticon-version v2.6.0 --clts-version v2.1.0
   ```
3. Make sure the CLDF data is valid and consistent:
   ```shell
   pytest
   ```
4. Create the metadata for zenodo, adding the tular community:
   ```shell
   cldfbench zenodo lexibank_tuled.py --communities tular
   ```
5. Create the release commit:
   ```shell
   git commit -a -m "release <VERSION>"
   ```
6. Create a release tag:
   ```
   git tag -a v<VERSION> -m"<VERSION> release"
   ```
7. Create a release from this tag on https://github.com/tupian-language-resources/tuled/releases
8. Verify that data and metadata has been picked up by Zenodo correctly,
   and copy the citation information into the GitHub release description.

