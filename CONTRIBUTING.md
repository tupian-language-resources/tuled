## Contributing to TuLeD

The TuLeD data is curated in a distributed way to allow using "the best tool
for the job" for each type of data. Thus, we use
- [EDICTOR](http://lingulist.de/edictor/) to curate lexical data,
- [Overleaf](https://www.overleaf.com/) (with its [GitHub integration](https://www.overleaf.com/learn/how-to/How_do_I_connect_an_Overleaf_project_with_a_repo_on_GitHub,_GitLab_or_BitBucket%3F))
  to curate the project [bibliography](https://github.com/tupian-language-resources/bibliography),
- Google spreadsheets to curate "master data", i.e. metadata about languages, concept, etc.

Data from these input sources is aggregated via [cldfbench](https://github.com/cldf/cldfbench). In particular, running `cldfbench download` will
- download the data from EDICTOR into `raw/tuled.tsv`,
- update the [git submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules) `raw/bibliography` from the respective repository,
- download the master data using the Google sheets API into `etc/`.

Thus, contributing to TuLeD data collection requires access to the tools specified
above, and recreating the CLDF dataset requires API access permissions.


### Recreating the CLDF data

- Clone this repository
  ```shell
  git clone https://github.com/tupian-language-resources/tuled.git
  ```
- and initialize the bibliography submodule
  ```shell
  cd tuled
  git submodule init
  ```
- Install the `cldfbench` requirements:
  ```shell
  pip install -e .[test]
  ```
- Clone required catalogs (Glottolog, Concepticon and CLTS) running
  ```
  cldfbench catconfig
  ```

Now you should be able to continue with the steps as described in
[RELEASING.md](RELEASING.md).

