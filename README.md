# AI for the Future Energy System

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
![AIFES project image](https://user-images.githubusercontent.com/18208480/215054857-930a1edd-0fc7-463e-9bde-8c1258f1ec75.JPG)

🧪 This repository holds all shared code for the AiNed project 'AI for the Future Energy System (AIFES)'

**Useful links**

- [Milestones](https://github.com/alliander-opensource/AIFES/milestones?direction=asc&sort=due_date&state=open)
- [Planning](https://github.com/alliander-opensource/AIFES/wiki/Planning)
- [wiki pages](https://github.com/alliander-opensource/AIFES/wiki)
- [Sharepoint (not public)](https://alliander.sharepoint.com/:f:/r/teams/PortfolioSO/Gedeelde%20documenten/Collaboration%20Allianer%20-%20TenneT%20T-Prognose?csf=1&web=1&e=t7pG8a)

## The objective of this project, in the form of a poem

```
Electricity flows through the land,
A force of nature, ever grand,
But with demand that’s on the rise,
Our grids must evolve to be wise.

Enter AI, with powers vast,
To optimize the power cast,
To manage energy supply,
And help the planet to get by.

With solar panels on the rise,
And turbines spinning to the skies,
Electric cars on every street,
We need the grid to be complete.

But variability is the bane,
Of these renewable energy trains,
The sun may hide, the wind may still,
The power may just fall to nil.

But with AI to lend a hand,
We can create a better brand,
Of grid that’s smart, that can adapt,
To any change, without mishap.

With data analyzed to a tee,
AI can optimize the energy,
Stored and released when it’s due,
To power homes and cars anew.

So let us look towards the sun,
And harness wind until we’re done,
Let AI take control of the grid,
And let clean energy take the lead.
```

### 🎁 Repo functionality

**Automated steps**

- Automatic linting of Python, Markdown, config files, etc. using [pre-commit](https://pre-commit.com/)
- Nice default GitHub settings (just install the [Probot settings app](https://github.com/apps/settings) to your repo
- IDE hints via [EditorConfig](https://editorconfig.org/) with good defaults for most languages
- [CodeMeta](https://codemeta.github.io/user-guide/) and [CITATION.cff](https://citation-file-format.github.io/)
- Nice gitignore, dockerignore, changelog, and other misc files
- Example/stub Conda environment file, Vagrantfile, and shields

### 📜 Steps to reproduce

**How to download needed data, run the code, etc.**

1. Clone this repository
1. Create virtual environment from yaml:
   `conda env create --file=environment.yml`
1. Run `pre-commit install`.
1. Create a .data folder in the root of the project, this folder is excluded by git. Then, download the data from [Sharepoint (not public)](https://alliander.sharepoint.com/:f:/r/teams/PortfolioSO/Gedeelde%20documenten/Collaboration%20Allianer%20-%20TenneT%20T-Prognose?csf=1&web=1&e=t7pG8a), and move it to the .data folder
1. Commit and push to _main_. Linting and clean-up of output cells is performed automatically. If a linter fails on commit, just re-run. It just meant the linter modified a file.

### Todos

1. Add to [Binder](https://mybinder.org/) and [Get a DOI](https://guides.github.com/activities/citable-code/) for your repo.
1. Add DOI

## License
This project is licensed under the [Apache License 2.0](https://github.com/alliander-opensource/AIFES/LICENSE.txt).

### 🍁 Contributing

Contributions and questions are welcome. For reference, refer to the [Code of Conduct](https://github.com/alliander-opensource/AIFES/CODE_OF_CONDUCT.md), [contributing guide](https://github.com/alliander-opensource/AIFES/CONTRIBUTING.md)
and [security policy](https://github.com/alliander-opensource/AIFES/SECURITY.md).

