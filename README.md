# Reflex Adapt Mappings

Reflex Adapt Mappings for MiSTer

## Installation

1. Download [reflex_updater.sh](https://github.com/misteraddons/Reflex-Adapt/releases/download/latest/reflex_updater.sh) and copy it to the `Scripts` folder on your MiSTer's SD card
2. Launch the `reflex_updater` script from the Scripts menu on your MiSTer
3. When prompted, agree to have the Reflex Adapt repository added
4. Flash your Reflex Adapt with the desired firmware configuration and exit the updater
5. Launch `update_all` or `downloader` from the Scripts menu

The Reflex Adapt updater, controller mappings and core configs will now be automatically updated whenever Update All or Downloader is run, excluding those you have made changes to.

Alternatively, manually add the following to your `downloader.ini` file on the SD card:

```
[misteraddons/reflexadapt]
db_url = https://github.com/misteraddons/mappings-reflex_adapt/raw/main/reflexadapt.json.zip
```
