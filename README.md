# recursive-readme
A small tool to create aesthetically pleasing recursive READMEs

For a sample you can view [my profile](https://github.com/daankoning).

## Why this tool

Existing solutions that solve this problem have a number of flaws that this version addresses. Notably:

* They __majorly__ pollute your profile README's commit history by committing each recursive layer. This program solves this by using javascript to manipulate the HTML of your profile page in such a way that only one commit is needed to generate the image.
* Complicated set-up: most other versions require you to clone repositories, configure them, and then run them locally. This tool is a simple plug-and-play Github action.
* Asynchronicity: because this tool is a simple action it is really easy to set it up to run on a cron schedule or on pushes to your repo. This means that it will always be in sync with your stars, repositories, and other content in your profile.

## Usage

### Set-up

Pick the location in your README where you want the recursive image to go. In this spot, add the HTML tag `<img id="recursiveREADME" src="example.png?">`[^1]. Then you can create `.github/workflows/image.yml` with contents:

```yaml
name: Update Image in README

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: daankoning/recursive-readme@v1.1.0
      with:
        auto-commit: 'true'
```

### Reference

The entire usage spec is below.

```yaml
- uses: daankoning/recursive-readme@v1.1.0
  with:
    # The user for which the image is being generated. Default: the owner of the current repository.
    user: 'your_user_name'
    
    # The depth to which the image should be generated (how many recursive layers). Default: 10"
    depth: 10
    
    # Whether or not to automatically commit the generated image. For ease of use this should be set to true. If any 
    # further manipulation of the image needs to take place after it is generated this input should be set to false.
    # Default: false
    auto-commit: 'false'
    
    # The file where the recursive image is output. This does not have to be (but probably should be) the file which 
    # the `src` attribute of the img tag points to. Default: /example.png
    output-file: '/image.png'
    
    # The id of the img tag in your README. Default: recursivereadme
    tag-id: 'readme-img'
    
    # Whether or not the action should set up its own Python install. This could overwrite an existing Python install
    # before this action which is why this should be set to 'false' if you already have an install. Default: true
    set-up-python: 'true'
```

[^1]: Both the `id` and the `src` can actually be changed by simply setting those inputs in the action, but these are the defaults and thus the simplest to use.
