**Table of Contents**:

- [2023-04-07](#2023-04-07)
  - [Changelog](#changelog)
  - [Notes](#notes)

---

## 2023-04-07

### Changelog
- Set up the basic structure of the project using `streamlit` and `venv`.
- Added `.gitignore` and `requirements.txt`.
- Added the home page in `About.py` with some dummy text.
- Added `load.py` with `load_brand()` and `init_page()` helper functions.
- Added some CSS and logo assets in the `assets` folder.

### Notes
- Look into the [`faker` package](https://faker.readthedocs.io/en/master) to generate test data, in particular use Filipino localization.

  ```python
  from faker import Faker
  fake = Faker('fil_PH')
  ```

- Look into using GeoJSON for the map visualization using the choropleth map in Plot.ly. Some GeoJSON data for the Philippines can be found at this [GitHub repo](https://github.com/faeldon/philippines-json-maps/).
- Remember to add "<kbd>Ctrl</kbd> + <kbd>F</kbd>" or "<kbd>Cmd</kbd> + <kbd>F</kbd>" instruction for search in DataFrames/tables.
