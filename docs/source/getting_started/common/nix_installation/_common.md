# Setting up the binary cache

Cachix allows the reproducible Nix builds to be stored on a cloud server so you do not have to build OpenLane's dependencies from scratch on every computer, which will take a long time.

First, you want to install Cachix by running the following in your terminal:

```sh
nix-env -f "<nixpkgs>" -iA cachix
```

Then set up the OpenLane binary cache as follows:

```sh
cachix use openlane
```

````{note}
If `cachix use openlane` fails, re-run it as follows:

```sh
sudo env PATH="$PATH" cachix use openlane
```

````

# Cloning OpenLane

With git installed, just run the following:

```sh
git clone https://github.com/efabless/openlane2
```

That's it. Whenever you want to use OpenLane, `nix-shell` in the repository root directory and you'll have a full OpenLane environment. The first time might take around 10 minutes while binaries are pulled from the cache.

To quickly test your installation, simply run `openlane --smoke-test` in the nix shell.